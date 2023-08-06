from argparse import ArgumentParser

from r2.actions.record.record import RecordAction
from r2.actions.replay.replay import ReplayAction


class ActionsDispatcher:
    ACTIONS_HANDLERS = [ReplayAction, RecordAction]

    def __init__(self):
        self.parser = ArgumentParser()
        subparsers = self.parser.add_subparsers()
        self.action_handlers = {action_handler.ACTION: action_handler(subparsers) for action_handler in
                                self.ACTIONS_HANDLERS}

    def process_application(self):
        configuration = self.parser.parse_args()
        if len(configuration.__dict__) == 0:
            self.parser.print_help()
            exit(0)
        self.action_handlers[configuration.ACTION].process_action(configuration)
