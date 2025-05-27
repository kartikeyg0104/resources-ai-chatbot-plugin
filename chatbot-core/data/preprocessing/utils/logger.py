import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [PREPROCESSING] [%(levelname)s]: %(message)s',
    datefmt='%H:%M:%S'
)

def get_logger():
    return logging.getLogger()