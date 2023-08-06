from r2.actions.action_dispatcher import ActionsDispatcher
from r2.helpers.constants import record_and_replay_ascii_logo
from r2.install import Installation


def main():
    print(record_and_replay_ascii_logo)
    actions_dispatcher = ActionsDispatcher()
    actions_dispatcher.process_application()


def before_run():
    Installation()


if __name__ == '__main__':
    before_run()
    main()
