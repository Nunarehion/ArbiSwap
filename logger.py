import logging
import json
import os
from datetime import datetime


class JsonFileHandler(logging.FileHandler):
    def emit(self, record):
        directory_name = f'logs/{(record.filename)[:-3]}'
        os.makedirs(directory_name, exist_ok=True)
        label_part = f"({record.label})" if hasattr(
            record, 'label') and record.label else ""
        log_filename = f"{directory_name}/[{self.formatTime(record)}][{record.levelname.lower()}]{label_part}-{record.filename[:-3]}{record.label if hasattr(record, 'label') else ''}.json"
        log_filename = log_filename.replace(":", "").replace(" ", "_")
        detail = {
            "more": {
                "file": record.filename,
                'level': record.levelname,
                'time': self.formatTime(record),
                'name': record.name,
                'label': record.label if hasattr(record, 'label') else None
            }
        }

        if isinstance(record.msg, dict):
            message = record.msg
            detail.update(message.get("detail", {}))

        elif isinstance(record.msg, str):
            message = {'message': record.msg}
        else:
            message = {'message': repr(record.msg)}

        log_record = {
            'data': message,
            'detail': detail
        }

        with open(log_filename, 'w') as f:
            json.dump(log_record, f, indent=4)

    def formatTime(self, record, datefmt=None):
        if datefmt:
            return datetime.fromtimestamp(record.created).strftime(datefmt)
        else:
            return datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')


# Настройка логгера
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

json_file_handler = JsonFileHandler(__name__)
json_file_handler.setLevel(logging.DEBUG)

# Добавление обработчика к логгеру
logger.addHandler(json_file_handler)

if __name__ == "__main__":
    logger.debug({'event': 'user_login', 'user_id': 123,
                 'status': 'success'}, extra={'label': 'user_action'})
    logger.info({'event': 'data_update', 'data_id': 456, 'changes': {
                'field': 'value'}}, extra={'label': 'data_action'})
    logger.warning({'event': 'user_login', 'user_id': 789, 'status': 'failed',
                   'reason': 'invalid_password'}, extra={'label': 'user_action'})
    logger.error({'event': 'data_delete', 'data_id': 101, 'status': 'error',
                 'message': 'not_found'}, extra={'label': 'data_action'})
    logger.critical({'event': 'system_failure', 'error_code': 500,
                    'message': 'internal_server_error'}, extra={'label': 'system_error'})
