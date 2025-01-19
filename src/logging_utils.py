import logging

def setup_logger(log_file, log_level):
    logging.basicConfig(
        filename=log_file,
        level=getattr(logging, log_level.upper()),
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger()