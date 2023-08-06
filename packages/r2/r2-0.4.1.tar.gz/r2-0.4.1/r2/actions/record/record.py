from r2.actions.action import Action
from r2.configuration import Configuration
from r2.core.flask_server import FlaskServer


class RecordAction(Action):
    ACTION = "record"
    PARAM_NAME = "ACTION"

    def fill_parser_arguments(self):
        self.parser.add_argument("target", help="Target service URI ", type=str)
        self.parser.add_argument("--package", help="Define a package name", type=str, default='default')
        self.parser.add_argument('-s', '--save', help="Save all incoming content the package folder", default=True)
        self.parser.add_argument('-o', '--overwrite', help="Overwrite all existing files in the package folder",
                                 default=False)

    def process_action(self, configuration):
        target = configuration.target
        package = configuration.package

        self.start_logging()

        Configuration(TARGET=target, PACKAGE_NAME=package, MODE=0).save()
        FlaskServer(target=target, package=package, save=configuration.save, overwrite=configuration.overwrite,
                    mode=0).serve()
