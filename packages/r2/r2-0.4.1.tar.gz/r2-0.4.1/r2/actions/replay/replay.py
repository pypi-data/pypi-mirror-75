from r2.actions.action import Action
from r2.configuration import Configuration
from r2.core.flask_server import FlaskServer


class ReplayAction(Action):
    ACTION = "replay"
    PARAM_NAME = "ACTION"

    def fill_parser_arguments(self):
        self.parser.add_argument("--package", help="Package name for the replay", type=str, default='default')

    def process_action(self, configuration):
        package = configuration.package

        self.start_logging()

        Configuration(PACKAGE_NAME=package, MODE=1).save()
        FlaskServer(package=package, mode=1).serve()
