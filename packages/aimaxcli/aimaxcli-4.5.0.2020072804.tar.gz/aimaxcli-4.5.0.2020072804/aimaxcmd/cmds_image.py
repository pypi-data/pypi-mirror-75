from cliff.lister import Lister
from cliff.show import ShowOne
from cliff.command import Command
import aimaxcmd.cmds_base as base
import logging
import requests
import aimaxsdk.tool as tool
import json

from aimaxcmd.yml import Yml


class CommonList(Lister,Yml):

    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(CommonList, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(CommonList, self).get_parser(prog_name))
        #取 库的映射 增加如下 提示代码uri
        #parser.add_argument("restful", nargs=1, help="restful api uri key")
        parser.add_argument("p1",  nargs=1, help="restful api uri key")
        return parser

    def _build_url(self,auth_info, parsed_args):
        address = auth_info["address"]
        port = auth_info["port"]
        token = auth_info['token']
        base_url = "http://{}:{}/s".format(address, port)
        if parsed_args.p1:
            base_url = "{}{}".format(base_url,self.restMap[parsed_args.p1[0]]['reqUrl'])
        if token:
            base_url = "{}?token={}".format(base_url,token)

        reqargdef =  self.restMap[parsed_args.p1[0]]['reqargdef']
        reqarg = self.restMap[parsed_args.p1[0]]['reqarg']
        if reqargdef and reqarg :
            for index in range(len(reqarg)):

                if reqargdef[index] =="auth_username":
                    base_url = "{}&{}={}".format(base_url,reqarg[index],auth_info["username"])
                else:
                    base_url = "{}&{}={}".format(base_url,reqarg[index],reqargdef[index])
        print(base_url)
        return base_url

    def take_action(self, parsed_args):

        super(CommonList, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)

        auth_info["token"] = token
        headers = {"Content-Type": "application/json"}
        response = requests.get(self._build_url(auth_info,parsed_args), headers=headers)
        print(response)
        if parsed_args.p1:
            ok, data = tool.parse_response(response, self.restMap[parsed_args.p1[0]]['resp'],"list")

        return self._data_formats(data, ok,parsed_args)

    def _data_formats(self, datas, ok,parsed_args):
        rtn1 = []
        for data in datas:
            rtn2 = []
            #'respcolumnsMap':'name,crt,JobType'
            colArray = self.restMap[parsed_args.p1[0]]['respcolumnsMap'];
            for index in range(len(colArray)):
                rtn2.append(data[colArray[index]])
            rtn1.append(rtn2)
        return self.restMap[parsed_args.p1[0]]['respcolumns'], rtn1



class CommonShowOne(ShowOne,Yml):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(CommonShowOne, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(CommonShowOne, self).get_parser(prog_name))
        #取 库的映射 增加如下 提示代码uri
        #parser.add_argument("restful", nargs=1, help="restful api uri key")
        parser.add_argument("p1",  nargs=2, help="restful api uri key")

        return parser

    def _build_url(self,auth_info, parsed_args):
        address = auth_info["address"]
        port = auth_info["port"]
        token = auth_info['token']
        base_url = "http://{}:{}/s".format(address, port)
        if parsed_args.p1:
            base_url = "{}{}".format(base_url,self.restMap[parsed_args.p1[0]]['reqUrl'])
        if parsed_args.p1[1]:
            base_url = "{}/{}".format(base_url,parsed_args.p1[1])
        if token:
            base_url = "{}?token={}".format(base_url,token)
        return base_url

    def take_action(self, parsed_args):

        super(CommonShowOne, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)

        auth_info["token"] = token
        headers = {"Content-Type": "application/json"}
        response = requests.get(self._build_url(auth_info,parsed_args), headers=headers)

        if parsed_args.p1[1]:
            ok, data = tool.parse_response(response)
        print('-------------------------asd-----------------')
        print(data)
        return self._data_formats(data, ok,parsed_args)

    def _data_formats(self, data, ok,parsed_args):
        rtn1 = []
        rtn2 = []
        #'respcolumnsMap':'name,crt,JobType'
        colArray = self.restMap[parsed_args.p1[0]]['respcolumnsMap'];
        for index in range(len(colArray)):
            rtn2.append(data[colArray[index]])
        rtn1.append(rtn2)

        return self.restMap[parsed_args.p1[0]]['respcolumns'], rtn1



class CommonAdd(Command,Yml):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(CommonAdd, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(CommonAdd, self).get_parser(prog_name))
        parser.add_argument("p1",  nargs=1, help="restful api uri key")
        return parser

    def _build_url(self,auth_info, parsed_args):
        address = auth_info["address"]
        port = auth_info["port"]
        token = auth_info['token']
        base_url = "http://{}:{}/s".format(address, port)
        if parsed_args.p1:
            base_url = "{}{}".format(base_url,self.restMap[parsed_args.p1[0]]['addUrl'])
        if token:
            base_url = "{}?token={}".format(base_url,token)
        return base_url

    def take_action(self, parsed_args):
        super(CommonAdd, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)

        auth_info["token"] = token
        headers = {"Content-Type": "application/json"}
        body = {}
        descArray = self.restMap[parsed_args.p1[0]]['adddesc']
        adddefault =  self.restMap[parsed_args.p1[0]]['adddefault']
        addbean = self.restMap[parsed_args.p1[0]]['addbean']

        for index in range(len(addbean)):
            attr = adddefault[index]
            if attr is None:
                attr = input(descArray[index])
            body[addbean[index]] = attr
        body_data = json.dumps(body)
        print(body_data)
        response = requests.post(self._build_url(auth_info,parsed_args), data=body_data, headers=headers)
        ok = tool.parse_response(response, None)
        if ok:
            self.app.LOG.info("Succeed to add ")
        else:
            self.app.LOG.info("Failed to add {}".format(body))



class CommonDelete(Command,Yml):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(CommonDelete, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(CommonDelete, self).get_parser(prog_name))
        parser.add_argument("p1",  nargs=2, help="restful api uri key")
        return parser

    def _build_url(self,auth_info, parsed_args):
        address = auth_info["address"]
        port = auth_info["port"]
        token = auth_info['token']
        base_url = "http://{}:{}/s".format(address, port)
        if parsed_args.p1:
            base_url = "{}{}".format(base_url,self.restMap[parsed_args.p1[0]]['delUrl'])
        if parsed_args.p1[1]:
            base_url = "{}/{}".format(base_url,parsed_args.p1[1])
        if token:
            base_url = "{}?token={}".format(base_url,token)
        return base_url


    def take_action(self, parsed_args):
        super(CommonDelete, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        auth_info["token"] = token
        headers = {"Content-Type": "application/json"}
        print(parsed_args.p1[0])
        print(parsed_args.p1[0])
        print(parsed_args.p1[1])
        prompt = self.restMap[parsed_args.p1[0]]['deldesc'].format(parsed_args.p1[1])
        select = input(prompt)
        if select.upper() != "Y":
            return
        response = requests.delete(self._build_url(auth_info,parsed_args), headers=headers)
        ok = tool.parse_response(response, None)
        if ok:
            self.app.LOG.info("Succeed to remove {}".format(parsed_args.p1[1]))
        else:
            self.app.LOG.info("Failed to remove {}".format(parsed_args.p1[1]))

