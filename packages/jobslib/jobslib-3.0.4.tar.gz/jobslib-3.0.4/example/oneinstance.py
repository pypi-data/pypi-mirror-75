
import os
import sys
import time

from jobslib import BaseTask

# settings --------------------------------------------------------------------

RUN_ONCE = False

SLEEP_INTERVAL = 5

ONE_INSTANCE = {
    'backend': 'jobslib.oneinstance.consul.ConsulLock',
    'options': {
        'host': 'localhost',
        'key': 'jobs/example/oneinstance/lock',
        'ttl': 60,
        'lock_delay': 5,
    },
}

LIVENESS = {
    'backend': 'jobslib.liveness.consul.ConsulLiveness',
    'options': {
        'host': 'localhost',
        'key': 'jobs/example/oneinstance/liveness',
    },
}

METRICS = {
    'backend': 'jobslib.metrics.dummy.DummyMetrics',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(name)s %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'NOTSET',
            'formatter': 'default',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}

KEEP_LOCK = True


# task ------------------------------------------------------------------------

class OneInstance(BaseTask):

    name = 'oneinstance'
    description = 'task which is run only in one instance at the same time'
    arguments = ()

    def task(self):
        for i in range(10, 0, -1):
            if self.context.one_instance_lock.refresh():
                sys.stdout.write("\r[{}] {}\x1b[K".format(os.getpid(), i))
                sys.stdout.flush()
                time.sleep(5.0)
        sys.stdout.write("\r\x1b[K")
        sys.stdout.flush()
