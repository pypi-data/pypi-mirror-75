import argparse
import logging
from abc import abstractmethod
from datetime import datetime

from r2.install import Installation


class Action:
    ACTION = None
    PARAM_NAME = None

    def __init__(self, subparsers):
        self.parser = argparse.ArgumentParser(add_help=False)
        self.fill_parser_arguments()
        self.parser.set_defaults(**{self.PARAM_NAME: self.ACTION})
        subparsers.add_parser(self.ACTION, parents=[self.parser], formatter_class=argparse.RawTextHelpFormatter)

    def fill_parser_arguments(self):
        pass

    @abstractmethod
    def process_action(self, configuration):
        pass

    def start_logging(self):
        def replace_all(text):
            for x in (":", ".", "-"):
                text = text.replace(x, '_')
            return text

        log_filename = f"{Installation.LOGS_DIR}/r2_{self.ACTION}_{replace_all(datetime.now().isoformat())}"
        logging.basicConfig(filename=log_filename, level=logging.NOTSET)
        logging.getLogger().addHandler(logging.StreamHandler())
        logging.info(f"r2 logs will be stored at {Installation.LOGS_DIR} as {log_filename}")
