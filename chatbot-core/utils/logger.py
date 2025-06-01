"""Logger configuration for RAG scripts."""

import logging

class LoggerFactory:
    _loggers = {}
    _formatter_template = '%(asctime)s [%(name)s] [%(levelname)s] [%(filename)s]: %(message)s'

    @classmethod
    def get_logger(cls, name: str):
        name = name.upper()
        if name in cls._loggers:
            return cls._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        cls._configure_logger(logger)
        cls._loggers[name] = logger
        return logger

    @classmethod
    def _configure_logger(cls, logger: logging.Logger):
        """Attach StreamHandler with custom formatting if not already configured."""
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(cls._formatter_template, datefmt='%H:%M:%S')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.propagate = False
    
    @classmethod
    def instance(cls):
        return cls()
