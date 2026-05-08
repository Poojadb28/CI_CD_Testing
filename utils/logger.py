import os
import logging


# ==========================================================
# LOG DIRECTORY
# ==========================================================

LOG_DIR = os.path.abspath("logs")

os.makedirs(
    LOG_DIR,
    exist_ok=True
)

LOG_FILE = os.path.join(
    LOG_DIR,
    "framework.log"
)


# ==========================================================
# LOG FORMAT
# ==========================================================

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ==========================================================
# ROOT LOGGER CONFIGURATION
# ==========================================================

logging.basicConfig(

    level=logging.INFO,

    format=LOG_FORMAT,

    datefmt=DATE_FORMAT,

    handlers=[

        # Console Logs
        logging.StreamHandler(),

        # File Logs
        logging.FileHandler(
            LOG_FILE,
            mode="a",
            encoding="utf-8"
        )
    ]
)


# ==========================================================
# LOGGER FACTORY
# ==========================================================

def get_logger(name):

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)

    return logger


# ==========================================================
# FRAMEWORK LOGGER
# ==========================================================

framework_logger = get_logger(
    "automation_framework"
)


# ==========================================================
# INFO LOG
# ==========================================================

def log_info(message):

    framework_logger.info(message)


# ==========================================================
# ERROR LOG
# ==========================================================

def log_error(message):

    framework_logger.error(message)


# ==========================================================
# WARNING LOG
# ==========================================================

def log_warning(message):

    framework_logger.warning(message)


# ==========================================================
# DEBUG LOG
# ==========================================================

def log_debug(message):

    framework_logger.debug(message)


# ==========================================================
# EXCEPTION LOG
# ==========================================================

def log_exception(message):

    framework_logger.exception(message)