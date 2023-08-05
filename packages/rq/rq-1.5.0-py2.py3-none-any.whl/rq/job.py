# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import inspect
import json
import pickle
import warnings
import zlib

from collections.abc import Iterable
from distutils.version import StrictVersion
from functools import partial
from uuid import uuid4

from rq.compat import as_text, decode_redis_hash, string_types
from .connections import resolve_connection
from .exceptions import NoSuchJobError
from .local import LocalStack
from .serializers import resolve_serializer
from .utils import (enum, import_attribute, parse_timeout, str_to_date,
                    utcformat, utcnow)

# Serialize pickle dumps using the highest pickle protocol (binary, default
# uses ascii)
dumps = partial(pickle.dumps, protocol=pickle.HIGHEST_PROTOCOL)
loads = pickle.loads

JobStatus = enum(
    'JobStatus',
    QUEUED='queued',
    FINISHED='finished',
    FAILED='failed',
    STARTED='started',
    DEFERRED='deferred',
    SCHEDULED='scheduled',
)

# Sentinel value to mark that some of our lazily evaluated properties have not
# yet been evaluated.
UNEVALUATED = object()


def truncate_long_string(data, maxlen=75):
    """ Truncates strings longer than maxlen
    """
    return (data[:maxlen] + '...') if len(data) > maxlen else data
	
def cancel_job(job_id, connection=None):
    """Cancels the job with the given job ID, preventing execution.  Discards
    any job info (i.e. it can't be requeued later).
    """
    Job.fetch(job_id, connection=connection).cancel()


def get_current_job(connection=None, job_class=None):
    """Returns the Job instance that is currently being executed.  If this
    function is invoked from outside a job context, None is returned.
    """
    if job_class:
        warnings.warn("job_class argument for get_current_job is deprecated.",
                      DeprecationWarning)
    return _job_stack.top


def requeue_job(job_id, connection):
    job = Job.fetch(job_id, connection=connection)
    return job.requeue()


class Job(object):
    """A Job is just a convenient datastructure to pass around job (meta) data.
    """
    redis_job_namespace_prefix = 'rq:job:'

    # Job construction
    @classmethod
    def create(cls, func, args=None, kwargs=None, connection=None,
               result_ttl=None, ttl=None, status=None, description=None,
               depends_on=None, timeout=None, id=None, origin=None, meta=None,
               failure_ttl=None, serializer=None):
        """Creates a new Job instance for the given function, arguments, and
        keyword arguments.
        """
        if args is None:
            args = ()
        if kwargs is None:
            kwargs = {}

        if not isinstance(args, (tuple, list)):
            raise TypeError('{0!r} is not a valid args list'.format(args))
        if not isinstance(kwargs, dict):
            raise TypeError('{0!r} is not a valid kwargs dict'.format(kwargs))

        job = cls(connection=connection, serializer=serializer)
        if id is not None:
            job.set_id(id)

        if origin is not None:
            job.origin = origin

        # Set the core job tuple properties
        job._instance = None
        if inspect.ismethod(func):
            job._instance = func.__self__
            job._func_name = func.__name__
        elif inspect.isfunction(func) or inspect.isbuiltin(func):
            job._func_name = '{0}.{1}'.format(func.__module__, func.__name__)
        elif isinstance(func, string_types):
            job._func_name = as_text(func)
        elif not inspect.isclass(func) and hasattr(func, '__call__'):  # a callable class instance
            job._instance = func
            job._func_name = '__call__'
        else:
            raise TypeError('Expected a callable or a string, but got: {0}'.format(func))
        job._args = args
        job._kwargs = kwargs

        # Extra meta data
        job.description = description or job.get_call_string()
        job.result_ttl = parse_timeout(result_ttl)
        job.failure_ttl = parse_timeout(failure_ttl)
        job.ttl = parse_timeout(ttl)
        job.timeout = parse_timeout(timeout)
        job._status = status
        job.meta = meta or {}

        # dependency could be job instance or id
        if depends_on is not None:
            job._dependency_ids = [depends_on.id if isinstance(depends_on, Job) else depends_on]
        return job

    def get_position(self):
        from .queue import Queue
        if self.origin:
            q = Queue(name=self.origin, connection=self.connection)
            return q.get_job_position(self._id)
        return None

    def get_status(self, refresh=True):
        if refresh:
            self._status = as_text(self.connection.hget(self.key, 'status'))

        return self._status

    def set_status(self, status, pipeline=None):
        self._status = status
        connection = pipeline if pipeline is not None else self.connection
        connection.hset(self.key, 'status', self._status)

    @property
    def is_finished(self):
        return self.get_status() == JobStatus.FINISHED

    @property
    def is_queued(self):
        return self.get_status() == JobStatus.QUEUED

    @property
    def is_failed(self):
        return self.get_status() == JobStatus.FAILED

    @property
    def is_started(self):
        return self.get_status() == JobStatus.STARTED

    @property
    def is_deferred(self):
        return self.get_status() == JobStatus.DEFERRED

    @property
    def is_scheduled(self):
        return self.get_status() == JobStatus.SCHEDULED

    @property
    def _dependency_id(self):
        """Returns the first item in self._dependency_ids. Present
        preserve compatibility with third party packages..
        """
        if self._dependency_ids:
            return self._dependency_ids[0]

    @property
    def dependency(self):
        """Returns a job's dependency. To avoid repeated Redis fetches, we cache
        job.dependency as job._dependency.
        """
        if not self._dependency_ids:
            return None
        if hasattr(self, '_dependency'):
            return self._dependency
        job = self.fetch(self._dependency_ids[0], connection=self.connection)
        self._dependency = job
        return job

    @property
    def dependent_ids(self):
        """Returns a list of ids of jobs whose execution depends on this
        job's successful execution."""
        return list(map(as_text, self.connection.smembers(self.dependents_key)))

    @property
    def func(self):
        func_name = self.func_name
        if func_name is None:
            return None

        if self.instance:
            return getattr(self.instance, func_name)

        return import_attribute(self.func_name)

    def _deserialize_data(self):
        self._func_name, self._instance, self._args, self._kwargs = self.serializer.loads(self.data)

    @property
    def data(self):
        if self._data is UNEVALUATED:
            if self._func_name is UNEVALUATED:
                raise ValueError('Cannot build the job data')

            if self._instance is UNEVALUATED:
                self._instance = None

            if self._args is UNEVALUATED:
                self._args = ()

            if self._kwargs is UNEVALUATED:
                self._kwargs = {}

            job_tuple = self._func_name, self._instance, self._args, self._kwargs
            self._data = self.serializer.dumps(job_tuple)
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self._func_name = UNEVALUATED
        self._instance = UNEVALUATED
        self._args = UNEVALUATED
        self._kwargs = UNEVALUATED

    @property
    def func_name(self):
        if self._func_name is UNEVALUATED:
            self._deserialize_data()
        return self._func_name

    @func_name.setter
    def func_name(self, value):
        self._func_name = value
        self._data = UNEVALUATED

    @property
    def instance(self):
        if self._instance is UNEVALUATED:
            self._deserialize_data()
        return self._instance

    @instance.setter
    def instance(self, value):
        self._instance = value
        self._data = UNEVALUATED

    @property
    def args(self):
        if self._args is UNEVALUATED:
            self._deserialize_data()
        return self._args

    @args.setter
    def args(self, value):
        self._args = value
        self._data = UNEVALUATED

    @property
    def kwargs(self):
        if self._kwargs is UNEVALUATED:
            self._deserialize_data()
        return self._kwargs

    @kwargs.setter
    def kwargs(self, value):
        self._kwargs = value
        self._data = UNEVALUATED

    @classmethod
    def exists(cls, job_id, connection=None):
        """Returns whether a job hash exists for the given job ID."""
        conn = resolve_connection(connection)
        return conn.exists(cls.key_for(job_id))

    @classmethod
    def fetch(cls, id, connection=None, serializer=None):
        """Fetches a persisted job from its corresponding Redis key and
        instantiates it.
        """
        job = cls(id, connection=connection, serializer=serializer)
        job.refresh()
        return job

    @classmethod
    def fetch_many(cls, job_ids, connection):
        """
        Bulk version of Job.fetch

        For any job_ids which a job does not exist, the corresponding item in
        the returned list will be None.
        """
        with connection.pipeline() as pipeline:
            for job_id in job_ids:
                pipeline.hgetall(cls.key_for(job_id))
            results = pipeline.execute()

        jobs = []
        for i, job_id in enumerate(job_ids):
            if results[i]:
                job = cls(job_id, connection=connection)
                job.restore(results[i])
                jobs.append(job)
            else:
                jobs.append(None)

        return jobs

    def __init__(self, id=None, connection=None, serializer=None):
        self.connection = resolve_connection(connection)
        self._id = id
        self.created_at = utcnow()
        self._data = UNEVALUATED
        self._func_name = UNEVALUATED
        self._instance = UNEVALUATED
        self._args = UNEVALUATED
        self._kwargs = UNEVALUATED
        self.description = None
        self.origin = None
        self.enqueued_at = None
        self.started_at = None
        self.ended_at = None
        self._result = None
        self.exc_info = None
        self.timeout = None
        self.result_ttl = None
        self.failure_ttl = None
        self.ttl = None
        self._status = None
        self._dependency_ids = []        
        self.meta = {}
        self.serializer = resolve_serializer(serializer)
        self.retries_left = None
        # retry_intervals is a list of int e.g [60, 120, 240]
        self.retry_intervals = None
        self.redis_server_version = None

    def __repr__(self):  # noqa  # pragma: no cover
        return '{0}({1!r}, enqueued_at={2!r})'.format(self.__class__.__name__,
                                                      self._id,
                                                      self.enqueued_at)

    def __str__(self):
        return '<{0} {1}: {2}>'.format(self.__class__.__name__,
                                       self.id,
                                       self.description)

    # Job equality
    def __eq__(self, other):  # noqa
        return isinstance(other, self.__class__) and self.id == other.id

    def __hash__(self):  # pragma: no cover
        return hash(self.id)

    # Data access
    def get_id(self):  # noqa
        """The job ID for this job instance. Generates an ID lazily the
        first time the ID is requested.
        """
        if self._id is None:
            self._id = str(uuid4())
        return self._id

    def set_id(self, value):
        """Sets a job ID for the given job."""
        if not isinstance(value, string_types):
            raise TypeError('id must be a string, not {0}'.format(type(value)))
        self._id = value

    id = property(get_id, set_id)

    @classmethod
    def key_for(cls, job_id):
        """The Redis key that is used to store job hash under."""
        return (cls.redis_job_namespace_prefix + job_id).encode('utf-8')

    @classmethod
    def dependents_key_for(cls, job_id):
        """The Redis key that is used to store job dependents hash under."""
        return '{0}{1}:dependents'.format(cls.redis_job_namespace_prefix, job_id)

    @property
    def key(self):
        """The Redis key that is used to store job hash under."""
        return self.key_for(self.id)

    @property
    def dependents_key(self):
        """The Redis key that is used to store job dependents hash under."""
        return self.dependents_key_for(self.id)

    @property
    def dependencies_key(self):
        return '{0}:{1}:dependencies'.format(self.redis_job_namespace_prefix, self.id)

    def fetch_dependencies(self, watch=False, pipeline=None):
        """
        Fetch all of a job's dependencies. If a pipeline is supplied, and
        watch is true, then set WATCH on all the keys of all dependencies.

        Returned jobs will use self's connection, not the pipeline supplied.

        If a job has been deleted from redis, it is not returned.
        """
        connection = pipeline if pipeline is not None else self.connection

        if watch and self._dependency_ids:
            connection.watch(*self._dependency_ids)

        jobs = [job
                for job in self.fetch_many(self._dependency_ids, connection=self.connection)
                if job]

        return jobs

    @property
    def result(self):
        """Returns the return value of the job.

        Initially, right after enqueueing a job, the return value will be
        None.  But when the job has been executed, and had a return value or
        exception, this will return that value or exception.

        Note that, when the job has no return value (i.e. returns None), the
        ReadOnlyJob object is useless, as the result won't be written back to
        Redis.

        Also note that you cannot draw the conclusion that a job has _not_
        been executed when its return value is None, since return values
        written back to Redis will expire after a given amount of time (500
        seconds by default).
        """
        if self._result is None:
            rv = self.connection.hget(self.key, 'result')
            if rv is not None:
                # cache the result
                self._result = self.serializer.loads(rv)
        return self._result

    """Backwards-compatibility accessor property `return_value`."""
    return_value = result

    def restore(self, raw_data):
        """Overwrite properties with the provided values stored in Redis"""
        obj = decode_redis_hash(raw_data)
        try:
            raw_data = obj['data']
        except KeyError:
            raise NoSuchJobError('Unexpected job format: {0}'.format(obj))

        try:
            self.data = zlib.decompress(raw_data)
        except zlib.error:
            # Fallback to uncompressed string
            self.data = raw_data

        self.created_at = str_to_date(obj.get('created_at'))
        self.origin = as_text(obj.get('origin'))
        self.description = as_text(obj.get('description'))
        self.enqueued_at = str_to_date(obj.get('enqueued_at'))
        self.started_at = str_to_date(obj.get('started_at'))
        self.ended_at = str_to_date(obj.get('ended_at'))
        result = obj.get('result')
        if result:
            try:
                self._result = self.serializer.loads(obj.get('result'))
            except Exception as e:
                self._result = "Unserializable return value"
        self.timeout = parse_timeout(obj.get('timeout')) if obj.get('timeout') else None
        self.result_ttl = int(obj.get('result_ttl')) if obj.get('result_ttl') else None  # noqa
        self.failure_ttl = int(obj.get('failure_ttl')) if obj.get('failure_ttl') else None  # noqa
        self._status = obj.get('status').decode() if obj.get('status') else None

        dependency_id = obj.get('dependency_id', None)
        self._dependency_ids = [as_text(dependency_id)] if dependency_id else []

        self.ttl = int(obj.get('ttl')) if obj.get('ttl') else None
        self.meta = self.serializer.loads(obj.get('meta')) if obj.get('meta') else {}
        
        self.retries_left = int(obj.get('retries_left')) if obj.get('retries_left') else None
        if obj.get('retry_intervals'):
            self.retry_intervals = json.loads(obj.get('retry_intervals').decode())

        raw_exc_info = obj.get('exc_info')
        if raw_exc_info:
            try:
                self.exc_info = as_text(zlib.decompress(raw_exc_info))
            except zlib.error:
                # Fallback to uncompressed string
                self.exc_info = as_text(raw_exc_info)

    # Persistence
    def refresh(self):  # noqa
        """Overwrite the current instance's properties with the values in the
        corresponding Redis key.

        Will raise a NoSuchJobError if no corresponding Redis key exists.
        """
        data = self.connection.hgetall(self.key)
        if not data:
            raise NoSuchJobError('No such job: {0}'.format(self.key))
        self.restore(data)

    def to_dict(self, include_meta=True):
        """
        Returns a serialization of the current job instance

        You can exclude serializing the `meta` dictionary by setting
        `include_meta=False`.
        """
        obj = {
            'created_at': utcformat(self.created_at or utcnow()),
            'data': zlib.compress(self.data),
            'started_at': utcformat(self.started_at) if self.started_at else '',
            'ended_at': utcformat(self.ended_at) if self.ended_at else '',
        }
        
        if self.retries_left is not None:
            obj['retries_left'] = self.retries_left
        if self.retry_intervals is not None:
            obj['retry_intervals'] = json.dumps(self.retry_intervals)
        if self.origin is not None:
            obj['origin'] = self.origin
        if self.description is not None:
            obj['description'] = self.description
        if self.enqueued_at is not None:
            obj['enqueued_at'] = utcformat(self.enqueued_at)

        if self._result is not None:
            try:
                obj['result'] = self.serializer.dumps(self._result)
            except Exception as e:
                obj['result'] = "Unserializable return value"
        if self.exc_info is not None:
            obj['exc_info'] = zlib.compress(str(self.exc_info).encode('utf-8'))
        if self.timeout is not None:
            obj['timeout'] = self.timeout
        if self.result_ttl is not None:
            obj['result_ttl'] = self.result_ttl
        if self.failure_ttl is not None:
            obj['failure_ttl'] = self.failure_ttl
        if self._status is not None:
            obj['status'] = self._status
        if self._dependency_ids:
            obj['dependency_id'] = self._dependency_ids[0]
        if self.meta and include_meta:
            obj['meta'] = self.serializer.dumps(self.meta)
        if self.ttl:
            obj['ttl'] = self.ttl

        return obj

    def save(self, pipeline=None, include_meta=True):
        """
        Dumps the current job instance to its corresponding Redis key.

        Exclude saving the `meta` dictionary by setting
        `include_meta=False`. This is useful to prevent clobbering
        user metadata without an expensive `refresh()` call first.

        Redis key persistence may be altered by `cleanup()` method.
        """
        key = self.key
        connection = pipeline if pipeline is not None else self.connection

        mapping = self.to_dict(include_meta=include_meta)

        if self.get_redis_server_version() >= StrictVersion("4.0.0"):
            connection.hset(key, mapping=mapping)
        else:
            connection.hmset(key, mapping)

    def get_redis_server_version(self):
        """Return Redis server version of connection"""
        if not self.redis_server_version:
            self.redis_server_version = StrictVersion(
                self.connection.info("server")["redis_version"]
            )

        return self.redis_server_version

    def save_meta(self):
        """Stores job meta from the job instance to the corresponding Redis key."""
        meta = self.serializer.dumps(self.meta)
        self.connection.hset(self.key, 'meta', meta)

    def cancel(self, pipeline=None):
        """Cancels the given job, which will prevent the job from ever being
        ran (or inspected).

        This method merely exists as a high-level API call to cancel jobs
        without worrying about the internals required to implement job
        cancellation.
        """
        from .queue import Queue
        pipeline = pipeline or self.connection.pipeline()
        if self.origin:
            q = Queue(name=self.origin, connection=self.connection)
            q.remove(self, pipeline=pipeline)
        pipeline.execute()

    def requeue(self):
        """Requeues job."""
        return self.failed_job_registry.requeue(self)

    def delete(self, pipeline=None, remove_from_queue=True,
               delete_dependents=False):
        """Cancels the job and deletes the job hash from Redis. Jobs depending
        on this job can optionally be deleted as well."""
        if remove_from_queue:
            self.cancel(pipeline=pipeline)
        connection = pipeline if pipeline is not None else self.connection

        if self.is_finished:
            from .registry import FinishedJobRegistry
            registry = FinishedJobRegistry(self.origin,
                                           connection=self.connection,
                                           job_class=self.__class__)
            registry.remove(self, pipeline=pipeline)

        elif self.is_deferred:
            from .registry import DeferredJobRegistry
            registry = DeferredJobRegistry(self.origin,
                                           connection=self.connection,
                                           job_class=self.__class__)
            registry.remove(self, pipeline=pipeline)

        elif self.is_started:
            from .registry import StartedJobRegistry
            registry = StartedJobRegistry(self.origin,
                                          connection=self.connection,
                                          job_class=self.__class__)
            registry.remove(self, pipeline=pipeline)

        elif self.is_scheduled:
            from .registry import ScheduledJobRegistry
            registry = ScheduledJobRegistry(self.origin,
                                            connection=self.connection,
                                            job_class=self.__class__)
            registry.remove(self, pipeline=pipeline)

        elif self.is_failed:
            self.failed_job_registry.remove(self, pipeline=pipeline)

        if delete_dependents:
            self.delete_dependents(pipeline=pipeline)

        connection.delete(self.key, self.dependents_key, self.dependencies_key)

    def delete_dependents(self, pipeline=None):
        """Delete jobs depending on this job."""
        connection = pipeline if pipeline is not None else self.connection
        for dependent_id in self.dependent_ids:
            try:
                job = Job.fetch(dependent_id, connection=self.connection)
                job.delete(pipeline=pipeline,
                           remove_from_queue=False)
            except NoSuchJobError:
                # It could be that the dependent job was never saved to redis
                pass
        connection.delete(self.dependents_key)

    # Job execution
    def perform(self):  # noqa
        """Invokes the job function with the job arguments."""
        self.connection.persist(self.key)
        _job_stack.push(self)
        try:
            self._result = self._execute()
        finally:
            assert self is _job_stack.pop()
        return self._result

    def _execute(self):
        return self.func(*self.args, **self.kwargs)

    def get_ttl(self, default_ttl=None):
        """Returns ttl for a job that determines how long a job will be
        persisted. In the future, this method will also be responsible
        for determining ttl for repeated jobs.
        """
        return default_ttl if self.ttl is None else self.ttl

    def get_result_ttl(self, default_ttl=None):
        """Returns ttl for a job that determines how long a jobs result will
        be persisted. In the future, this method will also be responsible
        for determining ttl for repeated jobs.
        """
        return default_ttl if self.result_ttl is None else self.result_ttl

    # Representation
    def get_call_string(self):  # noqa
        """Returns a string representation of the call, formatted as a regular
        Python function invocation statement.
        """
        if self.func_name is None:
            return None

        arg_list = [as_text(truncate_long_string(repr(arg))) for arg in self.args]

        kwargs = ['{0}={1}'.format(k, as_text(truncate_long_string(repr(v)))) for k, v in self.kwargs.items()]
        # Sort here because python 3.3 & 3.4 makes different call_string
        arg_list += sorted(kwargs)
        args = ', '.join(arg_list)

        return '{0}({1})'.format(self.func_name, args)

    def cleanup(self, ttl=None, pipeline=None, remove_from_queue=True):
        """Prepare job for eventual deletion (if needed). This method is usually
        called after successful execution. How long we persist the job and its
        result depends on the value of ttl:
        - If ttl is 0, cleanup the job immediately.
        - If it's a positive number, set the job to expire in X seconds.
        - If ttl is negative, don't set an expiry to it (persist
          forever)
        """
        if ttl == 0:
            self.delete(pipeline=pipeline, remove_from_queue=remove_from_queue)
        elif not ttl:
            return
        elif ttl > 0:
            connection = pipeline if pipeline is not None else self.connection
            connection.expire(self.key, ttl)
            connection.expire(self.dependents_key, ttl)
            connection.expire(self.dependencies_key, ttl)

    @property
    def failed_job_registry(self):
        from .registry import FailedJobRegistry
        return FailedJobRegistry(self.origin, connection=self.connection,
                                 job_class=self.__class__)
    
    def get_retry_interval(self):
        """Returns the desired retry interval.
        If number of retries is bigger than length of intervals, the first
        value in the list will be used multiple times.
        """
        if self.retry_intervals is None:
            return 0
        number_of_intervals = len(self.retry_intervals)
        index = max(number_of_intervals - self.retries_left, 0)
        return self.retry_intervals[index]

    def register_dependency(self, pipeline=None):
        """Jobs may have dependencies. Jobs are enqueued only if the job they
        depend on is successfully performed. We record this relation as
        a reverse dependency (a Redis set), with a key that looks something
        like:

            rq:job:job_id:dependents = {'job_id_1', 'job_id_2'}

        This method adds the job in its dependency's dependents set
        and adds the job to DeferredJobRegistry.
        """
        from .registry import DeferredJobRegistry

        registry = DeferredJobRegistry(self.origin,
                                       connection=self.connection,
                                       job_class=self.__class__)
        registry.add(self, pipeline=pipeline)

        connection = pipeline if pipeline is not None else self.connection

        for dependency_id in self._dependency_ids:
            dependents_key = self.dependents_key_for(dependency_id)
            connection.sadd(dependents_key, self.id)
            connection.sadd(self.dependencies_key, dependency_id)

    @property
    def dependency_ids(self):
        dependencies = self.connection.smembers(self.dependencies_key)
        return [Job.key_for(_id.decode())
                for _id in dependencies]

    def dependencies_are_met(self, exclude_job_id=None, pipeline=None):
        """Returns a boolean indicating if all of this jobs dependencies are _FINISHED_

        If a pipeline is passed, all dependencies are WATCHed.

        `exclude` allows us to exclude some job id from the status check. This is useful
        when enqueueing the dependents of a _successful_ job -- that status of
        `FINISHED` may not be yet set in redis, but said job is indeed _done_ and this
        method is _called_ in the _stack_ of it's dependents are being enqueued.
        """

        connection = pipeline if pipeline is not None else self.connection

        if pipeline is not None:
            connection.watch(*self.dependency_ids)

        dependencies_ids = {_id.decode()
                            for _id in connection.smembers(self.dependencies_key)}

        if exclude_job_id:
            dependencies_ids.discard(exclude_job_id)

        with connection.pipeline() as pipeline:
            for key in dependencies_ids:
                pipeline.hget(self.key_for(key), 'status')

            dependencies_statuses = pipeline.execute()

        return all(
            status.decode() == JobStatus.FINISHED
            for status
            in dependencies_statuses
            if status
        )

_job_stack = LocalStack()


class Retry(object):
    def __init__(self, max, interval=0):
        """`interval` can be a positive number or a list of ints"""
        super().__init__()
        if max < 1:
            raise ValueError('max: please enter a value greater than 0')
        
        if isinstance(interval, int):
            if interval < 0:
                raise ValueError('interval: negative numbers are not allowed')
            intervals = [interval]
        elif isinstance(interval, Iterable):
            for i in interval:
                if i < 0:
                    raise ValueError('interval: negative numbers are not allowed')
            intervals = interval
        
        self.max = max
        self.intervals = intervals
