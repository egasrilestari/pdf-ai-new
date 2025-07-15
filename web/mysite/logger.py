import os
import datetime
import logging
import time
import pytz
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(LOG_DIR, exist_ok=True)  # Bikin folder kalau belum ada

NOW = datetime.datetime.now()
DAY_NAME = NOW.strftime("%A").lower()

MAXIMUM_FILE_LOGS = 1024 * 1024 * 10  # 10 MB
BACKUP_COUNT = 5


class JakartaFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        jakarta_tz = pytz.timezone("Asia/Jakarta")
        dt = datetime.datetime.fromtimestamp(record.created, tz=jakarta_tz)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "()": JakartaFormatter,
            "format": "[%(levelname)s] %(asctime)s %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "default.log"),
            "maxBytes": MAXIMUM_FILE_LOGS,
            "backupCount": BACKUP_COUNT,
            "formatter": "standard",
        },
        "request_debug_handler": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "request_debug.log"),
            "maxBytes": MAXIMUM_FILE_LOGS,
            "backupCount": BACKUP_COUNT,
            "formatter": "standard",
        },
        "request_error_handler": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "request_error.log"),
            "maxBytes": MAXIMUM_FILE_LOGS,
            "backupCount": BACKUP_COUNT,
            "formatter": "standard",
        },
        "mail_admins_handler": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "email_backend": "django.core.mail.backends.smtp.EmailBackend",
        },
    },
    "root": {"handlers": ["default"], "level": "DEBUG"},
    "loggers": {
        "django.request": {
            "handlers": [
                "request_debug_handler",
                "request_error_handler",
                "mail_admins_handler",
            ],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
