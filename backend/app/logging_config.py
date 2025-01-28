import logging

def setup_logger():
    logger = logging.getLogger("flask_app")
    if not logger.hasHandlers():  
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s() - Line %(lineno)d - %(message)s')


        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler("app.log")
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
