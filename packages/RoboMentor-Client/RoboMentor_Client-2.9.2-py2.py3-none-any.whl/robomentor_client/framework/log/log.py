import logging

class Log:

    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s][%(filename)s(line:%(lineno)d)][%(levelname)s]: %(message)s"
    )

    @staticmethod
    def debug(content):
        logging.debug("\033[37m" + str(content) + "\033[0m")

    @staticmethod
    def info(content):
        logging.info("\033[34m" + str(content) + "\033[0m")

    @staticmethod
    def warning(content):
        logging.warning("\033[33m" + str(content) + "\033[0m")

    @staticmethod
    def error(content):
        logging.error("\033[31m" + str(content) + "\033[0m")