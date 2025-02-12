import logging
import json
from datetime import datetime
import os

from dataclasses import asdict, is_dataclass
from typing import Any, Dict
from pprint import pprint


def dataclass_to_dict(obj: Any) -> Dict[str, Any]:
    if is_dataclass(obj):
        return {k: dataclass_to_dict(v) for k, v in asdict(obj).items()}
    elif isinstance(obj, list):
        return [dataclass_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: dataclass_to_dict(v) for k, v in obj.items()}
    else:
        return obj


class JsonFileHandler(logging.FileHandler):
    def emit(self,  record):
        directory_name = f'logs/{(record.filename)[:-3]}'
        os.makedirs(directory_name, exist_ok=True)
        label_part = f"({record.label})" if hasattr(
            record, 'label') and record.label else ""
        log_filename = f"{directory_name}/[{self.formatTime(record)}][{record.levelname.lower()}]{label_part}-{record.filename[:-3]}.json"
        log_filename = log_filename.replace(":", "")
        log_filename = log_filename.replace(" ", "_")
        if isinstance(record.msg, dict):
            message = record.msg
        elif is_dataclass(record.msg):
            message = dataclass_to_dict({**record.msg})
        elif isinstance(record.msg, str):
            message = {'message': record.msg}
        else:
            message = {'message': repr(record.msg)}

        log_record = {
            "file": record.filename,
            'level': record.levelname,
            'time': self.formatTime(record),
            'name': record.name,
            'message': message
        }
        print(log_record)

        with open(log_filename, 'w') as f:
            json.dump(log_record, f, indent=4)

    def formatTime(self, record, datefmt=None):
        if datefmt:
            return datetime.fromtimestamp(record.created).strftime(datefmt)
        else:
            return datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')


class CustomLogger(logging.Logger):
    def info(self, msg, *args, label=None, **kwargs):
        if label is not None:
            extra = kwargs.get('extra', {})
            extra['label'] = label
            kwargs['extra'] = extra
        super().info(msg, *args, **kwargs)


# Настройка логгера
logging.setLoggerClass(CustomLogger)
# Настройка логирования
logger = logging.getLogger("LOGGER")
logger.setLevel(logging.DEBUG)

json_file_handler = JsonFileHandler(__name__)
json_file_handler.setLevel(logging.DEBUG)

# Добавление обработчика к логгеру
logger.addHandler(json_file_handler)

if __name__ == "__main__":
    logger.debug({'event': 'user_login', 'user_id': 123, 'status': 'success'})
    logger.info({'event': 'data_update', 'data_id': 456,
                'changes': {'field': 'value'}})
    logger.warning({'event': 'user_login', 'user_id': 789,
                    'status': 'failed', 'reason': 'invalid_password'})
    logger.error({'event': 'data_delete', 'data_id': 101,
                  'status': 'error', 'message': 'not_found'})
    logger.critical({'event': 'system_failure', 'error_code': 500,
                    'message': 'internal_server_error'})
