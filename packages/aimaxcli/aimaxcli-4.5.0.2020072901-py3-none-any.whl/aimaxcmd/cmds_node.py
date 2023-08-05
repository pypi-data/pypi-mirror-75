from cliff.lister import Lister
from cliff.show import ShowOne
from cliff.command import Command
import aimaxcmd.cmds_base as base
import logging
import requests
import aimaxsdk.tool as tool
import json


class NodeList(Lister):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(NodeList, self).__init__(app, app_args)
        #app.interactive_mode = True
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(NodeList, self).get_parser(prog_name))
        parser.add_argument("--latest", "-lt", action="store_true", help="Only show the two latest added nodes")
        parser.add_argument("--discovered", "-d", action="store_true", help="Show nodes discovered")
        parser.add_argument("--provisioning", "-pg", action="store_true", help="Show nodes are provisioning")
        return parser

    def _build_url(self, base_url, parsed_args):
        if parsed_args.latest:
            base_url = "{}&latest=2".format(base_url)
        if parsed_args.discovered:
            base_url = "{}&status=discovered".format(base_url)
        if parsed_args.provisioning:
            base_url = "{}&timer=AAA".format(base_url)
        return base_url

    def take_action(self, parsed_args):
        super(NodeList, self).take_action(parsed_args)

        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)

        url = "http://{}:{}/s/api/node/nodes?token={}&pageNum=1&pageSize=100".format(auth_info["address"],
                                                                                     auth_info["port"], token)
        headers = {"Content-Type": "application/json"}
        response = requests.get(self._build_url(url, parsed_args), headers=headers)
        ok, nodes = tool.parse_response(response, "obj", "results")
        return self._data_format(auth_info, nodes, ok, token, parsed_args)

    def _data_format(self, auth_info, nodes, ok, token, parsed_args):
        data = []
        if not parsed_args.provisioning:
            if ok:
                health_items = self.nodes_status(auth_info, token, nodes)
                for node_info in nodes:
                    data.append((node_info["nodeName"], node_info["ip"], node_info["cpucount"], node_info["memory"],
                                 node_info["gpucount"], node_info["disksize"], node_info["nodeFlag"],
                                 node_info["power"]))
                #,health_items[node_info["nodeName"]]
                return ("Name", "IP", "CPU Core", "Mem", "GPU", "Disk", "Tag", "Power"), data
            else:
                return ("Name", "IP", "CPU Core", "Mem", "GPU", "Disk", "Tag", "Power"), data #, "Health"
        else:
            if ok:
                for node_info in nodes:
                    state = ""
                    if node_info["currstate"] == "1":
                        state = "Finished"
                    elif node_info["currstate"] == "0":
                        state = "Installing"
                    elif node_info["currstate"] == "0":
                        state = "Failed"
                    data.append((node_info["nodeName"], state))
                return ("Name", "Provision State"), data
            else:
                return ("Name", "Provision State"), data

    def nodes_status(self, auth_info, token, nodes):
        nodes_str = ""
        values = {}
        print(nodes)
        for node in nodes:
            print(node)
            values[node['nodeName']] = ""
            nodes_str = nodes_str + node["nodeName"] + ","
        health_url = "http://{}:{}/s/api/monitor/node/item?token={}&hostname={}&keys=amax.allDockerhealth".format(
            auth_info["address"], auth_info["port"], token, nodes_str[:-1])
        headers = {"Content-Type": "application/json"}
        response = requests.get(health_url, headers=headers)
        ok, items = tool.parse_response(response, "item")
        if ok:
            for node_name in items:
                if items[node_name] == "1":
                    values[node_name] = "ok"
                else:
                    values[node_name] = "err"
        return values


class NodeInfo(ShowOne):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(NodeInfo, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=False)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(NodeInfo, self).get_parser(prog_name))
        parser.add_argument("node", nargs=1, help="Node name")
        return parser

    def take_action(self, parsed_args):
        super(NodeInfo, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        url = "http://{}:{}/s/api/node/nodes/{}?token={}".format(auth_info["address"], auth_info["port"],
                                                                 parsed_args.node[0], token)
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        ok, node = tool.parse_response(response, "obj")
        if ok:
            columns = ("Name", "IP", "CPU Core", "Mem", "GPU", "Disk", "Tag", "Power", "Health", "Online")
            data = (node["nodeName"], node["ip"], node["cpucount"], node["memory"], node["gpucount"], node["disksize"],
                    node["nodeFlag"], node["power"], self.health_status(auth_info, token, node["nodeName"]),
                    self.online_status(auth_info, token, node["ip"]))
            return columns, data
        else:
            return ("Name", "IP", "CPU Core", "Mem", "GPU", "Disk", "Tag", "Power", "Health", "Online"), ()

    def online_status(self, auth_info, token, node_name):
        health_url = "http://{}:{}/s/api/monitor/node/item?token={}&hostname={}&keys=amax.isOnline".format(
            auth_info["address"], auth_info["port"], token, node_name)
        headers = {"Content-Type": "application/json"}
        response = requests.get(health_url, headers=headers)
        ok, items = tool.parse_response(response, "items")
        if ok:
            value = items[0]["lastvalue"]
            if value == "1":
                return "yes"
            else:
                return "no"
        else:
            return ""

    def health_status(self, auth_info, token, node_name):
        health_url = "http://{}:{}/s/api/monitor/node/item?token={}&hostname={}&keys=amax.dockerhealth".format(
            auth_info["address"], auth_info["port"], token, node_name)
        headers = {"Content-Type": "application/json"}
        response = requests.get(health_url, headers=headers)
        ok, items = tool.parse_response(response, "items")
        value = items[0]["lastvalue"]
        if ok:
            if value == "1":
                return "ok"
            else:
                return "err"
        else:
            return ""


class NodeOverview(ShowOne):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(NodeOverview, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(NodeOverview, self).get_parser(prog_name))
        return parser

    def take_action(self, parsed_args):
        super(NodeOverview, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        url = "http://{}:{}/s/api/node?token={}".format(auth_info["address"], auth_info["port"], token)
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        ok, view = tool.parse_response(response, "obj")
        if ok:
            columns = ("Online", "Offline")
            return columns, (view["onlinecount"], view["offlinecount"])
        else:
            return ("Online", "Offline"), ()


class PowerOn(Command):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(PowerOn, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(PowerOn, self).get_parser(prog_name))
        parser.add_argument("node", nargs=1, help="Node name")
        return parser

    def take_action(self, parsed_args):
        super(PowerOn, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        node = parsed_args.node[0]
        url = "http://{}:{}/s/api/node/nodes/{}/poweron?token={}".format(auth_info["address"], auth_info["port"],
                                                                         node, token)
        headers = {"Content-Type": "application/json"}
        response = requests.put(url, headers=headers)
        ok = tool.parse_response(response, None)
        if ok:
            self.app.LOG.info("Succeed to power on {}".format(node))
        else:
            self.app.LOG.info("Failed to power on {}".format(node))


class PowerOff(Command):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(PowerOff, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(PowerOff, self).get_parser(prog_name))
        parser.add_argument("node", nargs=1, help="Node name")
        return parser

    def take_action(self, parsed_args):
        super(PowerOff, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        node = parsed_args.node[0]
        url = "http://{}:{}/s/api/node/nodes/{}/poweroff?token={}".format(auth_info["address"], auth_info["port"],
                                                                          node, token)
        headers = {"Content-Type": "application/json"}
        response = requests.put(url, headers=headers)
        ok = tool.parse_response(response, None)
        if ok:
            self.app.LOG.info("Succeed to power off {}".format(node))
        else:
            self.app.LOG.info("Failed to power off {}".format(node))


class PowerReset(Command):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(PowerReset, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(PowerReset, self).get_parser(prog_name))
        parser.add_argument("node", nargs=1, help="Node name")
        return parser

    def take_action(self, parsed_args):
        super(PowerReset, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        node = parsed_args.node[0]
        url = "http://{}:{}/s/api/node/nodes/{}/powerreset?token={}".format(auth_info["address"], auth_info["port"],
                                                                            node, token)
        headers = {"Content-Type": "application/json"}
        response = requests.put(url, headers=headers)
        ok = tool.parse_response(response, None)
        if ok:
            self.app.LOG.info("Succeed to reset {}".format(node))
        else:
            self.app.LOG.info("Failed to reset {}".format(node))


class NodeTag(Command):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(NodeTag, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(NodeTag, self).get_parser(prog_name))
        parser.add_argument("node", nargs=1, help="Node name")
        parser.add_argument("value", nargs=1, help="Node tag value")
        return parser

    def take_action(self, parsed_args):
        super(NodeTag, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        node = parsed_args.node[0]
        value = parsed_args.value[0]
        url = "http://{}:{}/s/api/node/nodes/{}/{}?token={}".format(auth_info["address"], auth_info["port"],
                                                                    node, value, token)
        headers = {"Content-Type": "application/json"}
        response = requests.put(url, headers=headers)
        ok = tool.parse_response(response, None)
        if ok:
            self.app.LOG.info("Succeed to set tag of {}".format(node))
        else:
            self.app.LOG.info("Failed to set tag of {}".format(node))


class NodeDelete(Command):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(NodeDelete, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(NodeDelete, self).get_parser(prog_name))
        parser.add_argument("node", nargs=1, help="Node name")
        return parser

    def take_action(self, parsed_args):
        super(NodeDelete, self).take_action(parsed_args)
        node = parsed_args.node[0]
        prompt = "The node will be removed from cluster, are you sure?\n 'Y': Continue, 'Others': Cancel\n".format(node)
        select = input(prompt)
        if select.upper() != "Y":
            return
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        url = "http://{}:{}/s/api/node/nodes/{}?token={}".format(auth_info["address"], auth_info["port"],
                                                                 node, token)
        headers = {"Content-Type": "application/json"}
        response = requests.delete(url, headers=headers)
        ok = tool.parse_response(response, None)
        if ok:
            self.app.LOG.info("Succeed to remove {}".format(node))
        else:
            self.app.LOG.info("Failed to remove {}".format(node))


class NodeAdd(Command):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(NodeAdd, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(NodeAdd, self).get_parser(prog_name))
        parser.add_argument("node", nargs=1, help="Node name")
        parser.add_argument("ip", nargs=1, help="Node ip")
        return parser

    def take_action(self, parsed_args):
        super(NodeAdd, self).take_action(parsed_args)
        node = parsed_args.node[0]
        ip = parsed_args.ip[0]
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        url = "http://{}:{}/s/api/node/nodes?token={}".format(auth_info["address"], auth_info["port"], token)
        headers = {"Content-Type": "application/json"}
        data = [{"nodeName": node, "ip": ip}]
        response = requests.post(url, data=json.dumps(data), headers=headers)
        ok = tool.parse_response(response, None)
        if ok:
            self.app.LOG.info("Succeed to add {}".format(node))
        else:
            self.app.LOG.info("Failed to add {}".format(node))
