import os
import logging



def setup_logger(log_file, log_level):
    
    # Ensure logs/ directory exists
    log_dir = "logs"
    
    
    # Create the logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Created directory: {log_dir}")
        
    """
    Setup logger to log into a file within the logs/ directory.
    The log file will be stored in the logs/ folder.
    """
    log_path = os.path.join(log_dir, log_file)  # Log file will be stored inside the logs/ folder
    
    
    # Create a custom logger
    logger = logging.getLogger(log_file)

    # Set the log level for this specific logger
    logger.setLevel(getattr(logging, log_level.upper()))

    # Create a file handler to write logs to the specified file
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(getattr(logging, log_level.upper()))

    # Create a log format
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Prevent the logger from propagating messages to the root logger
    logger.propagate = False

    return logger
    
