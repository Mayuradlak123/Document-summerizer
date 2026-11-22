import logging
from logging.config import dictConfig
import os
import sys

# Determine if file logging should be enabled
# Serverless environments (Vercel, AWS Lambda, Cloud Functions) have read-only filesystems at /var/task.
is_serverless = bool(
    os.getenv("VERCEL")
    or os.getenv("AWS_LAMBDA_FUNCTION_NAME")
    or os.getenv("K_SERVICE")
    or os.getenv("DISABLE_FILE_LOGGING", "").lower() in ("true", "1", "yes")
)

# Test whether file logging is possible and writable
enable_file_handler = False
log_file_path = None

if not is_serverless:
    try:
        CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT = os.path.dirname(os.path.dirname(CONFIG_DIR))
        logs_dir = os.path.join(PROJECT_ROOT, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        log_file_path = os.path.join(logs_dir, "application.log")
        # Test write access
        with open(log_file_path, "a", encoding="utf-8"):
            pass
        enable_file_handler = True
    except (OSError, PermissionError):
        enable_file_handler = False

# Build formatters and handlers
formatters = {
    "console": {
        "()": "uvicorn.logging.DefaultFormatter",
        "fmt": "%(levelprefix)s %(asctime)s - %(message)s",
    }
}

handlers = {
    "console": {
        "formatter": "console",
        "class": "logging.StreamHandler",
        "stream": "ext://sys.stderr",
    }
}

active_handlers = ["console"]

if enable_file_handler and log_file_path:
    formatters["file"] = {
        "format": "%(levelname)s: %(asctime)s - %(name)s - %(message)s",
        "datefmt": "%Y-%m-%d %H:%M:%S",
    }
    handlers["file"] = {
        "formatter": "file",
        "class": "logging.FileHandler",
        "filename": log_file_path,
        "mode": "a",
        "encoding": "utf-8",
    }
    active_handlers.append("file")

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": formatters,
    "handlers": handlers,
    "loggers": {
        "agent_system": {
            "handlers": active_handlers,
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn": {
            "handlers": active_handlers,
            "level": "INFO",
            "propagate": False,
        },
        "watchfiles": {
            "handlers": active_handlers,
            "level": "WARNING",
            "propagate": False,
        },
    },
    "root": {
        "handlers": active_handlers,
        "level": "INFO",
    },
}

try:
    dictConfig(log_config)
except Exception as e:
    # Fail-safe: ensure console logging works even if dictConfig encounters an environment issue
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(asctime)s - %(name)s - %(message)s",
        stream=sys.stderr,
    )
    logging.getLogger("agent_system").warning(f"dictConfig fallback triggered: {str(e)}")

logger = logging.getLogger("agent_system")
