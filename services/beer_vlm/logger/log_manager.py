import os
import logging
from logging.handlers import RotatingFileHandler
from beer_vlm.configs import LOG_PATH

class LogManager(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # relationship mapping

    def __init__(self, filename, level='info', backupCount=4):
        log_file_path = os.path.join(LOG_PATH, filename)
        print(f"Log file path: {log_file_path}")  # Debug print
        if not os.path.exists(LOG_PATH):
            print(f"Creating log directory: {LOG_PATH}")  # Debug print
            os.makedirs(LOG_PATH)
        
        # Configure the rotating file handler
        handler = RotatingFileHandler(
            filename=log_file_path,
            mode='a',  # Append mode to avoid overwriting logs on each run
            maxBytes=512000,  # 500 KB
            backupCount=backupCount
        )
        handler.setFormatter(logging.Formatter(
            fmt='%(levelname)s %(asctime)s %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p'
        ))

        # Configure the logging
        self.logger = logging.getLogger(filename)
        self.logger.setLevel(self.level_relations.get(level, logging.INFO))
        self.logger.addHandler(handler)
