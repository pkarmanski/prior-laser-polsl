import logging
from logging.config import fileConfig
from app.presentation.window_controller import WindowController
import os


version = "1.0.19"

if not os.path.exists("logs"):
    os.makedirs("logs")

fileConfig('logging.conf')

if __name__ == "__main__":
    logging.info("***********************")
    logging.info("Application start")
    try:
        WindowController().run()
    except Exception as e:
        logging.error(e)
