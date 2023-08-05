# Lightweight, opinionated logging module for python.
import woodchuck

import os
from datetime import date, datetime

LOG_DIR = 'logs'  # The default behavior is to store logs in the 'logs/' directory.
FILE_EXTENSION = 'log'  # The default file extension is '.log', although this can be changed freely.

# Set of log levels. Update this before calling 'initialize_logs' to add custom levels.
levels = {
    'INFO',  # Default level. Should be used for most things.
    'WARNING',  # Should be used for minor errors that can be automatically dealt with.
    'ERROR',  # Should be used for errors that likely require a human to fix.
    'CRITICAL',  # Should be used for errors that need to be fixed immediately.
    'DEBUG',  # Should be used in development for debugging.
}

# Dictionary of current log file strings. Created during initialization.
log_paths = {}

# Boolean storing whether or not woodchuck has been initialized
initialized = False


def initialize_logs():
    # Ensure we haven't already initialized.
    if woodchuck.initialized:
        return
    else:
        woodchuck.initialized = True

    # Ensure the logging directory exists.
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)

    # Ensure the directory for the current day exists.
    path = LOG_DIR + '/' + today()
    if not os.path.exists(path):
        os.mkdir(path)

    # Loop through each level, checking to see if a corresponding log file exists.
    for level in levels:
        path = LOG_DIR + '/' + today() + '/' + level + '.' + FILE_EXTENSION
        if not os.path.exists(path):
            open(path, 'a+').close()
        log_paths[level] = path
    woodchuck._initialized = True

    # Writes to a given level of log, defaulting to INFO.


def log(message, level='INFO', sep='|'):
    if not woodchuck.initialized:
        raise LoggingException('Attempted to write to log before initializing.')

    if level not in levels:
        raise LoggingException('Attempted to write to an invalid log.')

    log_msg = now_iso() + ' ' + sep + ' ' + level + ' ' + sep + ' ' + message
    log_path = log_paths[level]

    with open(log_path, 'a+') as file:
        file.write(log_msg + '\n')


# Returns the current date, formatted in the human-readable, iso-like YYYY-MM-DD.
def today():
    return date.today().strftime('%Y-%m-%d')

    # Returns the current date and time, formatted according to ISO 8601.


def now_iso():
    # I prefer to use a space as the separator.
    return datetime.now().isoformat(sep=' ')

    # Thrown when an error occurs with logging.


class LoggingException(Exception):
    pass
