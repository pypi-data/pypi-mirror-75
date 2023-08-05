import os
import sys
import json
import datetime

_LOG_LEVEL_MAP = {
    'debug': 10,
    'info': 20,
    'warning': 30,
    'error': 40,
}

_LOG_DEFAULT_FORMAT_STRING = '{level} {created_at} {message}'


class CloudLogger:
    class Internal:
        @classmethod
        def logger_decorator(cls, method):
            def _logger_decorator(obj, *args, **kwargs):
                level_name = method.__name__
                if _LOG_LEVEL_MAP[level_name] >= obj.log_level:
                    writer = sys.stdout if level_name != 'error' else sys.stderr
                    context = {
                        'level_name': level_name,
                        'message_parts': args,
                    }

                    log_record = {
                        key: value(context) if callable(value) else value
                        for key, value in obj.log_bindings.items()
                    }
                    log_record.update(kwargs)

                    if obj.log_json:
                        if obj.log_json_fields:
                            log_record = {
                                key: value for key, value in log_record.items() if key in obj.log_json_fields}

                        output_string = json.dumps(log_record, default=str, separators=(',', ':'))
                    elif obj.log_format:
                        output_string = obj.log_format.format(**log_record)
                    else:
                        output_string = ' '.join('{}="{}"'.format(key, value) for key, value in log_record.items())

                    writer.write('{}\n'.format(output_string))

            return _logger_decorator

    def __init__(self, log_level='info', log_format=None, log_json=False, log_json_fields=''):
        self.log_json = bool(os.environ.get('CLOUD_LOG_JSON', log_json))
        self.log_level = _LOG_LEVEL_MAP.get(os.environ.get('CLOUD_LOG_LEVEL', log_level), 1000)
        self.log_format = os.environ.get('CLOUD_LOG_FORMAT', log_format)
        self.log_json_fields = os.environ.get('CLOUD_LOG_JSON_FIELDS', log_json_fields).split(',')
        if '' in self.log_json_fields:
            self.log_json_fields.remove('')

        self.log_bindings = {}
        self.bind('level', lambda context: context.get('level_name'))
        self.bind('message', lambda context: ' '.join(str(part) for part in context.get('message_parts')))
        self.bind('created_at', lambda context: datetime.datetime.utcnow().isoformat())

    def bind(self, key, value):
        self.log_bindings[key] = value

    def unbind(self, key):
        del self.log_bindings[key]

    @Internal.logger_decorator
    def debug(self, *args, **kwargs):
        pass

    @Internal.logger_decorator
    def info(self, *args, **kwargs):
        pass

    @Internal.logger_decorator
    def warning(self, *args, **kwargs):
        pass

    @Internal.logger_decorator
    def error(self, *args, **kwargs):
        pass


# Default singleton logger
logger = CloudLogger()

# Define shortcuts
bind = logger.bind
unbind = logger.unbind
debug = logger.debug
info = logger.info
warning = logger.warning
error = logger.error
