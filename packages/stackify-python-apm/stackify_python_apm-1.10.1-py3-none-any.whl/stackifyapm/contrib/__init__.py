import inspect
import json
import os
import sys
from functools import wraps

from stackifyapm.base import Client
from stackifyapm.conf import constants
from stackifyapm.handlers.exceptions import get_exception_context
from stackifyapm.instrumentation.control import instrument


def make_client(**defaults):
    config = defaults.get("STACKIFY_APM", {})
    defaults['base_dir'] = defaults.get("BASE_DIR") or defaults.get("base_dir") or os.getcwd()
    config_file = defaults.get("CONFIG_FILE") or defaults.get("config_file") or constants.DEFAULT_CONFIG_FILE

    try:
        with open(config_file) as json_file:
            data = json.load(json_file)
            defaults.update(data)
            defaults['base_dir'] = data.get('base_dir') or defaults['base_dir']
    except Exception:
        pass

    defaults['config_file'] = config_file

    frame = inspect.stack()[-1]
    module = inspect.getmodule(frame[0])
    main_file = module.__file__.split('/')[-1].split('.')[0]

    instrument_all_exclude = defaults.get('instrument_all_exclude', "")
    excludes = instrument_all_exclude and instrument_all_exclude.split(',') or []
    excludes.append(main_file or 'app')
    defaults['instrument_all_exclude'] = ','.join(excludes)

    return Client(config, **defaults)


class _BaseStackifyAPM(object):
    """
    Base application for StackifyAPM.
    """
    def __init__(self, **defaults):
        self.func_name = None
        self.context = None
        self.client = make_client(**defaults)

    def clean_up(self):
        self.client.transport.send_all()

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.func_name = func.__name__

            with self:
                return func(*args, **kwargs)

        return wrapper

    def __enter__(self):
        self.client.begin_transaction("custom", client=self.client)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            exc_info = sys.exc_info()
            if exc_info:
                exception = exc_info[1]
                traceback = exc_info[2]
                self.client.capture_exception(
                    exception=get_exception_context(exception, traceback)
                )

        self.client.end_transaction(name=self.func_name)
        self.clean_up()


class _BaseServerlessStackifyAPM(_BaseStackifyAPM):
    """
    Base application for serverless StackifyAPM.
    """
    def __init__(self, **defaults):
        defaults.update({
            'TRANSPORT': constants.TRANSPORT_LOGGING,
            'QUEUE': False,
        })
        super(_BaseServerlessStackifyAPM, self).__init__(**defaults)


class StackifyAPM(_BaseStackifyAPM):
    """
    Generic application for StackifyAPM.
    """
    def __init__(self, **defaults):
        super(StackifyAPM, self).__init__(**defaults)
        instrument(self.client)
