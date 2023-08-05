from cliff.app import App
from cliff.commandmanager import CommandManager
import sys
from aimaxsdk import auth
import traceback
import logging


class AIMaxApp(App):

    def __init__(self):
        super(AIMaxApp, self).__init__(
            description="AIMax python commands client",
            version="4.5.0.2020072901",
            command_manager=CommandManager('aimax.client'),
            deferred_help=True
        )
        self.connections = auth.Connections()
        self.auth_info = {}

    def initialize_app(self, argv):
        super().initialize_app(argv)
        self.LOG.setLevel(logging.DEBUG)
        self.LOG.debug("Initializing AIMax python commands client......")
        print("Initializing AIMax python commands client......")
        self.connections.load()
        self.LOG.debug("Initialized AIMax python commands client")

    def prepare_to_run_command(self, cmd):
        super().prepare_to_run_command(cmd)
        self.LOG.debug("prepare to run command %s", cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        super().clean_up(cmd, result, err)
        self.LOG.debug("clean up %s", cmd.__class__.__name__)
        if err:
            self.LOG.error(traceback.format_exc())
            self.LOG.error("got an error, {}".format(err))


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    myapp = AIMaxApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
