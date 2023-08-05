import sys

from cliff.app import App
from cliff.commandmanager import CommandManager
from aimaxsdk import auth

class DemoApp(App):

    def __init__(self):
        super(DemoApp, self).__init__(
            description='cliff demo app',
            version='0.1',
            command_manager=CommandManager('amx.client'),
            deferred_help=True,
            )
        self.connections = auth.Connections()
        self.auth_info = {}

    def initialize_app(self, argv):
        super().initialize_app(argv)
        self.LOG.debug('initialize_app')
        self.connections.load()

    def prepare_to_run_command(self, cmd):
        super().prepare_to_run_command(cmd)
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        super().clean_up(cmd, result, err)
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = DemoApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
