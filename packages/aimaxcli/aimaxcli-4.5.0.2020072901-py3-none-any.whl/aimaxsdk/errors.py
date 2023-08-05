import json
import os

file_path = os.path.abspath(__file__)
folder_path = file_path[0:file_path.rindex("/")]
parent_package_path = folder_path[0:folder_path.rindex("/")]
with open("{}/aimaxsdk/errors.json".format(parent_package_path)) as fp:
    all_errors = json.load(fp)


class ClientException(Exception):

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs


class NotSignedInException(ClientException):
    pass


class ParamMissingException(ClientException):
    pass


class InvalidPasswordException(ClientException):
    pass


class AIMaxServerException(ClientException):
    pass