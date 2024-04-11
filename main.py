import logging
from logging.config import fileConfig
from app.presentation.window_controller import WindowController

version = "1.0.2"

fileConfig('logging.conf')

if __name__ == "__main__":
    logging.info("***********************")
    logging.info("Application start")
    WindowController().run()
