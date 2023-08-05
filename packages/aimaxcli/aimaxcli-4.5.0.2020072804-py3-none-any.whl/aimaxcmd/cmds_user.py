from cliff.lister import Lister
from cliff.show import ShowOne
from cliff.command import Command
import aimaxcmd.cmds_base as base
import logging
import requests
import aimaxsdk.tool as tool
import json
import aimaxsdk.errors as errors
import configparser


def get_groupid(auth_info, token, group_name):
    url = "http://{}:{}/s/api/auth/groups/{}?token={}".format(auth_info["address"], auth_info["port"], group_name,
                                                              token)
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    ok, group = tool.parse_response(response, "obj")
    if ok:
        return group["id"]
    else:
        raise errors.AIMaxServerException("Failed to get group id")


def load_roles(auth_info, token):
    url = "http://{}:{}/s/api/auth/roles?token={}".format(auth_info["address"], auth_info["port"], token)
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    ok, roles = tool.parse_response(response, "obj", "list")
    if ok:
        data = {}
        for role in roles:
            service = role["roleName"].split("_")[0]
            role_type = role["roleName"].split("_")[1]
            if service not in data:
                data[service] = {}
            data[service][role_type] = {"roleName": role["roleName"], "id": role["id"]}
        return data
    else:
        raise errors.AIMaxServerException("Failed to load AIMax roles")


def load_zones(auth_info, token):
    data = {}
    url = "http://{}:{}/s/api/job/zones?token={}".format(auth_info["address"], auth_info["port"], token)
    headers = {"Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    ok, zones = tool.parse_response(response, "zones")
    if ok:
        for zone in zones:
            data_item = {"name": zone["name"]}
            for quota in zone["quotas"]:
                if quota == "JOBS":
                    data_item["jobs"] = int(zone["quotas"]["JOBS"]["amount"])
                elif quota == "GPU":
                    data_item["gpu"] = int(zone["quotas"]["GPU"]["amount"])
                elif quota == "CPU":
                    data_item["cpu"] = int(zone["quotas"]["CPU"]["amount"])
                elif quota == "MEM":
                    mem_value = int(zone["quotas"]["MEM"]["amount"])
                    mem_unit = zone["quotas"]["MEM"]["unit"]
                    data_item["mem"] = "{}{}".format(mem_value, mem_unit)
            data[zone["name"]] = data_item
        return data
    else:
        raise errors.AIMaxServerException("Failed to load AIMax zones")


def load_volumes(auth_info, token):
    pass


class GroupList(Lister):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(GroupList, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        return self.auth_info_loader.filter_parser(super(GroupList, self).get_parser(prog_name))

    def take_action(self, parsed_args):
        super(GroupList, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        url = "http://{}:{}/s/api/auth/groups?token={}".format(auth_info["address"], auth_info["port"], token)
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        ok, groups = tool.parse_response(response, "obj", "list")
        data = []
        if ok:
            for group in groups:
                data.append((group["id"],group["groupname"], group["userCount"], group["createTime"], group["creator"],
                             group["updateTime"]))
            return ("Group ID","Group Name", "User Count", "Created At", "Created By", "Modified At"), data
        else:
            return ("Group ID","Group Name", "User Count", "Created At", "Created By", "Modified At"), data


class GroupInfo(ShowOne):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(GroupInfo, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(GroupInfo, self).get_parser(prog_name))
        parser.add_argument("group", nargs=1, help="Group name")
        return parser

    def take_action(self, parsed_args):
        super(GroupInfo, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        group_name = parsed_args.group[0]
        url = "http://{}:{}/s/api/auth/groups/{}?token={}".format(auth_info["address"], auth_info["port"], group_name,
                                                                  token)
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        ok, group = tool.parse_response(response, "obj")
        if ok:
            return ("Group ID","Group Name", "User Count", "Created At", "Created By", "Modified At", "Roles"), (
                group["id"],group["groupname"], group["userCount"], group["createTime"], group["creator"], group["updateTime"], "")
        else:
            return ("Group ID","Group Name", "User Count", "Created At", "Created By", "Modified At", "Roles"), ()


class GroupAdd(Command):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(GroupAdd, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        return self.auth_info_loader.filter_parser(super(GroupAdd, self).get_parser(prog_name))

    def take_action(self, parsed_args):
        super(GroupAdd, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        roles = load_roles(auth_info, token)
        group_name = input("Please input group name: ")
        role_data = []
        for role in roles:
            prompt = "Please select role of {}   0: admin, others: viewer ".format(role)
            role_type = input(prompt)
            if role_type == "0":
                role_data.append(roles[role]["admin"])
            else:
                role_data.append(roles[role]["viewer"])
        url = "http://{}:{}/s/api/auth/groups?token={}".format(auth_info["address"], auth_info["port"], token)
        headers = {"Content-Type": "application/json"}
        body_data = json.dumps({"groupname": group_name, "creator": auth_info["username"], "roles": role_data})
        response = requests.post(url, data=body_data, headers=headers)
        ok = tool.parse_response(response, None)
        if ok:
            self.app.LOG.info("Succeed to add group {}".format(group_name))
        else:
            self.app.LOG.info("Failed to add group {}".format(group_name))


class GroupDelete(Command):
    og = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(GroupDelete, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(GroupDelete, self).get_parser(prog_name))
        parser.add_argument("group", nargs=1, help="Group name")
        return parser

    def take_action(self, parsed_args):
        super(GroupDelete, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        group_name = parsed_args.group[0]
        group_id = get_groupid(auth_info, token, group_name)
        url = "http://{}:{}/s/api/auth/groups/{}?token={}".format(auth_info["address"], auth_info["port"], group_id,
                                                                  token)
        headers = {"Content-Type": "application/json"}
        response = requests.delete(url, headers=headers)
        ok = tool.parse_response(response, None)
        if ok:
            self.app.LOG.info("Succeed to delete group {}".format(group_name))
        else:
            self.app.LOG.info("Failed to delete group {}".format(group_name))


class UserList(Lister):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(UserList, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(UserList, self).get_parser(prog_name))
        parser.add_argument("--group", "-g", nargs=1, help="Group name")
        return parser

    def take_action(self, parsed_args):
        super(UserList, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        if parsed_args.group is not None:
            group_id = get_groupid(auth_info, token, parsed_args.group[0])
            url = "http://{}:{}/s/api/auth/user?token={}&groupId={}".format(auth_info["address"], auth_info["port"],
                                                                            token, group_id)
        else:
            url = "http://{}:{}/s/api/auth/user?token={}&groupId=0".format(auth_info["address"], auth_info["port"],
                                                                           token)
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        ok, users = tool.parse_response(response, "obj", "list")
        data = []
        if ok:
            for user in users:
                data.append((user["id"],user["username"], user["mobile"], user["email"], user["createTime"], user["creator"],
                             user["mender"], user["updateTime"], user["zoneName"], user["volumeName"],
                             user["usergroup"]["groupname"]))
            return ("UserId","User Name", "Mobile Phone", "Email", "Created At", "Created By", "Modified At", "Modified By",
                    "Zone", "Volume", "Group"), data
        else:
            return ("UserId","User Name", "Mobile Phone", "Email", "Created At", "Created By", "Modified At", "Modified By",
                    "Zone", "Volume", "Group"), data


class UserInfo(ShowOne):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(UserInfo, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(UserInfo, self).get_parser(prog_name))
        parser.add_argument("user", nargs=1, help="User name")
        return parser

    def take_action(self, parsed_args):
        super(UserInfo, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        user_name = parsed_args.user[0]
        url = "http://{}:{}/s/api/auth/user/{}?token={}&groupId=0".format(auth_info["address"], auth_info["port"],
                                                                          user_name, token)
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        ok, user = tool.parse_response(response, "obj")
        if ok:
            return ("UserId","User Name", "Mobile Phone", "Email", "Created At", "Created By", "Modified At", "Modified By",
                    "Zone", "Volume", "Group", "GPU Quota", "CPU Quota", "Memory Quota", "Storage Quota",
                    "Job Quota"), (user["id"],user["username"], user["mobile"], user["email"], user["createTime"], user["creator"],
                                   user["mender"], user["updateTime"], user["zoneName"], user["volumeName"],
                                   user["usergroup"]["groupname"], user["quota"]["gpu"], user["quota"]["cpu"],
                                   user["quota"]["internalMemory"], user["quota"]["dataStorage"],
                                   user["quota"]["taskNumber"])
        else:
            return ("UserId","User Name", "Mobile Phone", "Email", "Created At", "Created By", "Modified At", "Modified By",
                    "Zone", "Volume", "Group", "GPU Quota", "CPU Quota", "Memory Quota", "Storage Quota",
                    "Job Quota"), ()


class UserAdd(Command):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(UserAdd, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(UserAdd, self).get_parser(prog_name))
        parser.add_argument("--data-file", "-df", nargs=1, help="User data file")
        return parser

    def _read_data_file(self, filepath):
        user_info = {}
        config = configparser.ConfigParser()
        config.read(filepath, encoding="utf-8")
        user_info["username"] = config.get("default", "username")
        user_info["password"] = config.get("default", "password")
        user_info["group"] = config.get("default", "group")
        user_info["mobile"] = config.get("default", "mobile")
        user_info["email"] = config.get("default", "email")
        user_info["volume"] = config.get("default", "volume")
        user_info["zone"] = config.get("default", "zone")
        user_info["cpu"] = config.get("default", "cpu")
        user_info["gpu"] = config.get("default", "gpu")
        user_info["mem"] = config.get("default", "mem")
        user_info["storage"] = config.get("default", "storage")
        user_info["jobs"] = config.get("default", "jobs")
        return user_info

    def take_action(self, parsed_args):
        super(UserAdd, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        if parsed_args.data_file is not None:
            user_info = self._read_data_file(parsed_args.data_file[0])
        else:
            zones = load_zones(auth_info, token)
            print("Please select a zone from the following list:")
            for zone in zones:
                print("     {}".format(zone))

    # url = "http://{}:{}/s/api/auth/user/{}?token={}&groupId=0".format(auth_info["address"], auth_info["port"],
    #                                                                   user_name, token)
    # headers = {"Content-Type": "application/json"}
    # response = requests.get(url, headers=headers)
    # ok, user = tool.parse_response(response, "obj")
