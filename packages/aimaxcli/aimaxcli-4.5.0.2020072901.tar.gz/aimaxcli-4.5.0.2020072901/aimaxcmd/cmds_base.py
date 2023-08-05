import abc
import six
from cliff.command import Command
import logging
import configparser
from aimaxsdk import errors
from aimaxsdk.errors import InvalidPasswordException


def _get_auth_info(parsed_args):
    auth_info = {}
    if parsed_args.config_file:
        config = configparser.ConfigParser()
        config.read(parsed_args.config_file[0], encoding="utf-8")
        auth_info["address"] = config.get("default", "address")
        auth_info["port"] = config.get("default", "port")
        auth_info["username"] = config.get("default", "username")
        auth_info["password"] = config.get("default", "password")
    else:
        if parsed_args.host is None:
            raise errors.ParamMissingException("AIMax server address is missing")
        auth_info["address"] = parsed_args.host[0]
        if parsed_args.port is None:
            raise errors.ParamMissingException("AIMax server port is missing")
        auth_info["port"] = parsed_args.port[0]
        if parsed_args.username is None:
            raise errors.ParamMissingException("AIMax username is missing")
        auth_info["username"] = parsed_args.username[0]
        if parsed_args.password is None:
            raise errors.ParamMissingException("AIMax password is missing")
        auth_info["password"] = parsed_args.password[0]
    return auth_info


def create_auth_info_builder(app, signed_in):
    if app.interactive_mode:
        return InteractiveAuthInfoLoader(app, signed_in)
    else:
        return NonInteractiveAuthInfoLoader(app, signed_in)


def get_token(auth_info, connections):
    if connections.check_password(auth_info["address"], auth_info["port"], auth_info["username"],
                                  auth_info["password"]):
        return connections.token(auth_info["address"], auth_info["port"], auth_info["username"])
    else:
        raise InvalidPasswordException("Password provided is invalid")


@six.add_metaclass(abc.ABCMeta)
class AuthInfoLoader(object):

    def __init__(self, app, signed_in=True):
        self.signed_in = signed_in
        self.app = app

    def load_auth_info(self, parsed_args):
        pass

    def filter_parser(self, parser):
        pass


class InteractiveAuthInfoLoader(AuthInfoLoader):

    def __init__(self, app, signed_in=True):
        super().__init__(app, signed_in)

    def load_auth_info(self, parsed_args):
        if self.signed_in and parsed_args.config_file is None:
            return self.app.auth_info
        else:
            return _get_auth_info(parsed_args)

    def filter_parser(self, parser):
        if not self.signed_in:
            parser.add_argument("--host", nargs=1, help="AIMax server address")
            parser.add_argument("--port", "-p", nargs=1, help="AIMax server port")
            parser.add_argument("--password", "-P", nargs=1, help="AIMax username")
            parser.add_argument("--username", "-u", nargs=1, help="AIMax password")
        parser.add_argument("--config-file", "-F", nargs=1, help="Config file "
                                                                 "containing AIMax authentication info")
        return parser


class NonInteractiveAuthInfoLoader(AuthInfoLoader):

    def __init__(self, app, signed_in=True):
        super().__init__(app, signed_in)

    def load_auth_info(self, parsed_args):
        return _get_auth_info(parsed_args)

    def filter_parser(self, parser):
        parser.add_argument("--host", nargs=1, help="AIMax server address")
        parser.add_argument("--port", "-p", nargs=1, help="AIMax server port")
        parser.add_argument("--password", "-P", nargs=1, help="AIMax username")
        parser.add_argument("--username", "-u", nargs=1, help="AIMax password")
        parser.add_argument("--config-file", "-F", nargs=1, help="Config file "
                                                                 "containing AIMax authentication info")
        return parser


class Connect(Command):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(Connect, self).__init__(app, app_args)
        self.auth_info_loader = create_auth_info_builder(app, signed_in=False)

    def get_parser(self, prog_name):
        return self.auth_info_loader.filter_parser(super(Connect, self).get_parser(prog_name))

    def take_action(self, parsed_args):
        super(Connect, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        connections.connect(auth_info["address"], auth_info["port"], auth_info["username"], auth_info["password"])
        #self.log.info("Succeed to connect a2")
        self.app.auth_info = auth_info



class Disconnect(Command):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(Disconnect, self).__init__(app, app_args)
        self.auth_info_loader = create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        return self.auth_info_loader.filter_parser(super(Disconnect, self).get_parser(prog_name))

    def take_action(self, parsed_args):
        super(Disconnect, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        connections.disconnect(auth_info["address"], auth_info["port"], auth_info["username"])
        self.log.info("Succeed to disconnect")
