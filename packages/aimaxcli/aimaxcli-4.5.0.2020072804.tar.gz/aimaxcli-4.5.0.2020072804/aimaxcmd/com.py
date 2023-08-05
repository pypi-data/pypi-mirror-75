import os

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
        #parser = super(CommonList, self).get_parser(prog_name)
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
        if 'reqUrlReplaceAttr' in self.restMap[parsed_args.p1[0]] :

            getUrlReplaceAttr = self.restMap[parsed_args.p1[0]]['reqUrlReplaceAttr']

            if type(getUrlReplaceAttr) is str:
                getUrlReplace = self.restMap[parsed_args.p1[0]]['reqUrlReplace']
                if 'reqUrlReplacedef' in self.restMap[parsed_args.p1[0]]:
                    base_url = base_url.replace(getUrlReplace,self.restMap[parsed_args.p1[0]]['reqUrlReplacedef'])
                else:
                    attr = input(getUrlReplaceAttr)
                    #print(base_url)
                    base_url = base_url.replace(getUrlReplace,attr)
                    #print(base_url)
            else:
                getUrlReplace = self.restMap[parsed_args.p1[0]]['reqUrlReplace']
                for index in range(len(getUrlReplaceAttr)):
                    if 'reqUrlReplacedef' in self.restMap[parsed_args.p1[0]]:
                        base_url = base_url.replace(getUrlReplace[index],
                                                    self.restMap[parsed_args.p1[0]]['reqUrlReplacedef'][index])
                    else:
                        attr = input(getUrlReplaceAttr[index])
                        #print(base_url)
                        base_url = base_url.replace(getUrlReplace[index],attr)
                        #print(base_url)

        if 'reqUrldesc' in self.restMap[parsed_args.p1[0]]:
            reqUrldesc = self.restMap[parsed_args.p1[0]]['reqUrldesc']
            attr = input(reqUrldesc)
            base_url = "{}/{}".format(base_url,attr)
        if 'reqUrlappend' in self.restMap[parsed_args.p1[0]] :
            base_url = "{}/{}".format(base_url,self.restMap[parsed_args.p1[0]]['reqUrlappend'])
        if token:
            base_url = "{}?token={}".format(base_url,token)


        if 'reqarg' in self.restMap[parsed_args.p1[0]] and 'reqargdef' in self.restMap[parsed_args.p1[0]]:
            reqargdef =  self.restMap[parsed_args.p1[0]]['reqargdef']
            reqarg = self.restMap[parsed_args.p1[0]]['reqarg']
            if 'reqargdesc' in self.restMap[parsed_args.p1[0]] :
                reqargdesc =  self.restMap[parsed_args.p1[0]]['reqargdesc']
            #if reqargdef and reqarg :
            if type(reqarg) is str:
                ##print('字符串')
                if reqargdef is None:
                    attr = input(reqargdesc)
                    base_url = "{}&{}={}".format(base_url,reqarg,attr)
                elif reqargdef =="auth_username":
                    base_url = "{}&{}={}".format(base_url,reqarg,auth_info["username"])
                else:
                    base_url = "{}&{}={}".format(base_url,reqarg,reqargdef)
            else:
                ##print('数组')
                for index in range(len(reqarg)):
                    if reqargdef is None or reqargdef[index] is None:
                        attr = input(reqargdesc[index])
                        base_url = "{}&{}={}".format(base_url,reqarg[index],attr)
                    elif reqargdef[index] =="auth_username":
                        base_url = "{}&{}={}".format(base_url,reqarg[index],auth_info["username"])
                    else:
                        base_url = "{}&{}={}".format(base_url,reqarg[index],reqargdef[index])

        #print(base_url)
        return base_url

    def take_action(self, parsed_args):

        super(CommonList, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)

        auth_info["token"] = token
        headers = {"Content-Type": "application/json"}
        base_url = self._build_url(auth_info,parsed_args)
        response = requests.get(base_url, headers=headers)
        #print(response)
        status_code = response.status_code
        if status_code != 200 or 'resp' not in self.restMap[parsed_args.p1[0]]:
            # if response.message is not None:
            #     print(response.message)
            data = json.loads(response.text)
            print(data)
            return [],[]

        if parsed_args.p1:
            ok, data = tool.parse_response(response, self.restMap[parsed_args.p1[0]]['resp'])
        #asd = [],asd.append(("1","2")),asd.append(("3","4"))        #return ("Name", "IP"), asd
        #print(asd)
        return self._data_formats(data, ok,parsed_args)


    def _data_formats(self, datas, ok,parsed_args):
        rtn1 = []
        print (datas)
        for data in datas:
            rtn2 = []
            #'respcolumns':'name,crt,JobType'
            colArray = self.restMap[parsed_args.p1[0]]['respcolumns'];

            for index in range(len(colArray)):
                # #print('======================' )
                # #print(data)
                # #print(colArray)
                rtn2.append(data[colArray[index]])
            rtn1.append(rtn2)

        #print(rtn1)

        return self.restMap[parsed_args.p1[0]]['respcolumndesc'], rtn1





class CommonShow(ShowOne,Yml):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(CommonShow, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(CommonShow, self).get_parser(prog_name))
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
            base_url = "{}{}".format(base_url,self.restMap[parsed_args.p1[0]]['getUrl'])

        if 'getUrlReplaceAttr' in self.restMap[parsed_args.p1[0]] :

            getUrlReplaceAttr = self.restMap[parsed_args.p1[0]]['getUrlReplaceAttr']

            if type(getUrlReplaceAttr) is str:
                getUrlReplace = self.restMap[parsed_args.p1[0]]['getUrlReplace']
                if 'getUrlReplacedef' in self.restMap[parsed_args.p1[0]]:
                    base_url = base_url.replace(getUrlReplace,self.restMap[parsed_args.p1[0]]['getUrlReplacedef'])
                else:
                    attr = input(getUrlReplaceAttr)
                    #print(base_url)
                    base_url = base_url.replace(getUrlReplace,attr)
                    #print(base_url)
            else:
                getUrlReplace = self.restMap[parsed_args.p1[0]]['getUrlReplace']
                for index in range(len(getUrlReplaceAttr)):
                    if 'getUrlReplacedef' in self.restMap[parsed_args.p1[0]]:
                        base_url = base_url.replace(getUrlReplace[index],self.restMap[parsed_args.p1[0]]['getUrlReplacedef'][index])
                    else:
                        attr = input(getUrlReplaceAttr[index])
                        #print(base_url)
                        base_url = base_url.replace(getUrlReplace[index],attr)
                        #print(base_url)

        if 'getUrldesc' in self.restMap[parsed_args.p1[0]]:
            reqUrldesc = self.restMap[parsed_args.p1[0]]['getUrldesc']
            attr = input(reqUrldesc)
            base_url = "{}/{}".format(base_url,attr)
        if 'getUrlappend' in self.restMap[parsed_args.p1[0]] :
            base_url = "{}/{}".format(base_url,self.restMap[parsed_args.p1[0]]['getUrlappend'])
        if token:
            base_url = "{}?token={}".format(base_url,token)


        if 'getarg' in self.restMap[parsed_args.p1[0]] and 'getargdef' in self.restMap[parsed_args.p1[0]]:
            reqargdef =  self.restMap[parsed_args.p1[0]]['getargdef']
            reqarg = self.restMap[parsed_args.p1[0]]['getarg']
            if 'getargdesc' in self.restMap[parsed_args.p1[0]] :
                reqargdesc =  self.restMap[parsed_args.p1[0]]['getargdesc']
            #if reqargdef and reqarg :

            if type(reqarg) is str:
                ##print('字符串')
                if reqargdef is None:
                    attr = input(reqargdesc)
                    if 'getargfun' in self.restMap[parsed_args.p1[0]] :
                        attr = fun_zab(self.restMap[parsed_args.p1[0]]['getargfun'],attr)
                        #print(attr)
                    base_url = "{}&{}={}".format(base_url,reqarg,attr)
                elif reqargdef =="auth_username":
                    base_url = "{}&{}={}".format(base_url,reqarg,auth_info["username"])
                else:
                    base_url = "{}&{}={}".format(base_url,reqarg,reqargdef)
            else:
                ##print('数组')
                for index in range(len(reqarg)):
                    if reqargdef is None or reqargdef[index] is None:
                        attr = input(reqargdesc[index])
                        if 'getargfun' in self.restMap[parsed_args.p1[0]] :
                            if self.restMap[parsed_args.p1[0]]['getargfun'][index]  is not None:
                                attr = fun_zab(self.restMap[parsed_args.p1[0]]['getargfun'][index],attr)
                                #print(attr)
                        base_url = "{}&{}={}".format(base_url,reqarg[index],attr)
                    elif reqargdef[index] =="auth_username":
                        base_url = "{}&{}={}".format(base_url,reqarg[index],auth_info["username"])
                    else:
                        base_url = "{}&{}={}".format(base_url,reqarg[index],reqargdef[index])

        #print(base_url)
        return base_url

    def take_action(self, parsed_args):

        super(CommonShow, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)

        auth_info["token"] = token
        headers = {"Content-Type": "application/json"}#"text/plain"
        response = requests.get(self._build_url(auth_info,parsed_args), headers=headers)#params=[]


        status_code = response.status_code
        if status_code != 200 or 'resp' not in self.restMap[parsed_args.p1[0]]:
            # if response.message is not None:
            #     print(response.message)
            data = json.loads(response.text)
            print(data)
            return [],[]

        ok, data = tool.parse_response(response)
        ##print('-------------------------asd-----------------')

        return self._data_formats(data, ok,parsed_args)

    def _data_formats(self, data, ok,parsed_args):
        rtn1 = []
        #'respcolumns':'name,crt,JobType'

        if 'respcolumns' in self.restMap[parsed_args.p1[0]]:
            colArray = self.restMap[parsed_args.p1[0]]['respcolumns'];
            for index in range(len(colArray)):
                rtn1.append(data[colArray[index]])
            return self.restMap[parsed_args.p1[0]]['respcolumndesc'], rtn1
        else:
            return data
        # #print(self.restMap[parsed_args.p1[0]]['respcolumndesc'])
        # #print(rtn1)
        # return ("name","createTimeStamp","jobType"),("name","createTimeStamp","jobType")



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
        body = {}
        base_url = "http://{}:{}/s".format(address, port)
        if parsed_args.p1:
            base_url = "{}{}".format(base_url,self.restMap[parsed_args.p1[0]]['addUrl'])


        if 'addUrlReplaceAttr' in self.restMap[parsed_args.p1[0]] :

            getUrlReplaceAttr = self.restMap[parsed_args.p1[0]]['addUrlReplaceAttr']

            if type(getUrlReplaceAttr) is str:
                getUrlReplace = self.restMap[parsed_args.p1[0]]['addUrlReplace']
                if 'addUrlReplacedef' in self.restMap[parsed_args.p1[0]]:
                    base_url = base_url.replace(getUrlReplace,self.restMap[parsed_args.p1[0]]['addUrlReplacedef'])
                else:
                    attr = input(getUrlReplaceAttr)
                    #print(base_url)
                    base_url = base_url.replace(getUrlReplace,attr)
                    #print(base_url)
            else:
                getUrlReplace = self.restMap[parsed_args.p1[0]]['addUrlReplace']
                for index in range(len(getUrlReplaceAttr)):
                    if 'addUrlReplacedef' in self.restMap[parsed_args.p1[0]]:
                        base_url = base_url.replace(getUrlReplace[index],self.restMap[parsed_args.p1[0]]['addUrlReplacedef'][index])
                    else:
                        attr = input(getUrlReplaceAttr[index])
                        #print(base_url)
                        base_url = base_url.replace(getUrlReplace[index],attr)
                        #print(base_url)

        if 'addUrldesc' in self.restMap[parsed_args.p1[0]]:
            reqUrldesc = self.restMap[parsed_args.p1[0]]['addUrldesc']
            attr = input(reqUrldesc)
            base_url = "{}/{}".format(base_url,attr)
        if 'addUrlappend' in self.restMap[parsed_args.p1[0]] :
            base_url = "{}/{}".format(base_url,self.restMap[parsed_args.p1[0]]['addUrlappend'])
        if token:
            base_url = "{}?token={}".format(base_url,token)


        if 'addarg' in self.restMap[parsed_args.p1[0]] and 'addargdef' in self.restMap[parsed_args.p1[0]]:
            reqargdef =  self.restMap[parsed_args.p1[0]]['addargdef']
            reqarg = self.restMap[parsed_args.p1[0]]['addarg']
            if 'addargdesc' in self.restMap[parsed_args.p1[0]] :
                reqargdesc =  self.restMap[parsed_args.p1[0]]['addargdesc']
            #if reqargdef and reqarg :
            if type(reqarg) is str:
                ##print('字符串')
                if reqargdef is None:
                    attr = input(reqargdesc)
                    base_url = "{}&{}={}".format(base_url,reqarg,attr)
                    #此处比较特殊 因为restful接口很多没有按照post方式封装bean而是用的url参数 为了方便body体和url都加参数
                    body[reqargdef] = attr
                elif reqargdef =="auth_username":
                    base_url = "{}&{}={}".format(base_url,reqarg,auth_info["username"])
                    body[reqargdef] = auth_info["username"]
                else:
                    base_url = "{}&{}={}".format(base_url,reqarg,reqargdef)
                    body[reqargdef] = reqargdef
            else:
                ##print('数组')
                for index in range(len(reqarg)):

                    if reqargdef is None or reqargdef[index] is None:
                        attr = input(reqargdesc[index])
                        base_url = "{}&{}={}".format(base_url,reqarg[index],attr)
                        body[reqarg[index]] = attr
                    elif reqargdef[index] =="auth_username":
                        base_url = "{}&{}={}".format(base_url,reqarg[index],auth_info["username"])
                        body[reqarg[index]] = auth_info["username"]
                    else:
                        base_url = "{}&{}={}".format(base_url,reqarg[index],reqargdef[index])
                        body[reqarg[index]] = reqargdef[index]

        if 'body' in self.restMap[parsed_args.p1[0]]:
            body = self.restMap[parsed_args.p1[0]]['body']
            #print(body)
            if 'bodyarg' in self.restMap[parsed_args.p1[0]]:
                addbodyarg = self.restMap[parsed_args.p1[0]]['bodyarg']
                addbodydesc = self.restMap[parsed_args.p1[0]]['bodydesc']
                addbodytype = self.restMap[parsed_args.p1[0]]['bodytype']

                if type(addbodyarg) is str:
                    attr = input(addbodydesc)

                    if addbodytype == 'array':
                        arry = attr.split(',')
                        body[addbodyarg] = arry
                    else:
                        #if addbodytype == 'str':#.find(',')>=0:
                        body[addbodyarg] = attr
                else:
                    ##print('数组')
                    for index in range(len(addbodyarg)):
                        attr = input(addbodydesc[index])
                        if addbodytype[index] == 'array':
                            arry = attr.split(',')
                            body[addbodyarg[index]] = arry
                        else:
                            #if addbodytype[index] == 'str':#.find(',')>=0:
                            body[addbodyarg[index]] = attr

        body_data = json.dumps(body)
        if 'bodyjson' in self.restMap[parsed_args.p1[0]]:
            body_data = input(self.restMap[parsed_args.p1[0]]['bodyjson'])
        return base_url,body_data

    def take_action(self, parsed_args):
        super(CommonAdd, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)

        auth_info["token"] = token
        headers = {"Content-Type": "application/json"}

        build_url,body_data=self._build_url(auth_info,parsed_args)
        # #print(body_data)
        response = requests.post(build_url, data=body_data, headers=headers)
        #print(response)
        ok = tool.parse_response(response, None)
        if ok:
            self.app.LOG.info("Succeed to add ")
        else:
            self.app.LOG.info("Failed to add {}".format(body_data))



class CommonDelete(Command,Yml):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(CommonDelete, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(CommonDelete, self).get_parser(prog_name))
        parser.add_argument("p1",  nargs=1, help="restful api uri key")
        return parser

    def _build_url(self,auth_info, parsed_args):
        address = auth_info["address"]
        port = auth_info["port"]
        token = auth_info['token']
        base_url = "http://{}:{}/s".format(address, port)
        nodestr = ''
        body = {}

        if parsed_args.p1:
            base_url = "{}{}".format(base_url,self.restMap[parsed_args.p1[0]]['delUrl'])
        if 'delUrlReplaceAttr' in self.restMap[parsed_args.p1[0]] :
            getUrlReplaceAttr = self.restMap[parsed_args.p1[0]]['delUrlReplaceAttr']
            if type(getUrlReplaceAttr) is str:
                getUrlReplace = self.restMap[parsed_args.p1[0]]['delUrlReplace']
                if 'delUrlReplacedef' in self.restMap[parsed_args.p1[0]]:
                    base_url = base_url.replace(getUrlReplace,self.restMap[parsed_args.p1[0]]['delUrlReplacedef'])
                else:
                    attr = input(getUrlReplaceAttr)
                    #print(base_url)
                    base_url = base_url.replace(getUrlReplace,attr)
                    #print(base_url)
            else:
                getUrlReplace = self.restMap[parsed_args.p1[0]]['delUrlReplace']
                for index in range(len(getUrlReplaceAttr)):
                    if 'delUrlReplacedef' in self.restMap[parsed_args.p1[0]]:
                        base_url = base_url.replace(getUrlReplace[index],self.restMap[parsed_args.p1[0]]['delUrlReplacedef'][index])
                    else:
                        attr = input(getUrlReplaceAttr[index])
                        #print(base_url)
                        base_url = base_url.replace(getUrlReplace[index],attr)
                        #print(base_url)
        if 'delUrldesc' in self.restMap[parsed_args.p1[0]]:
            reqUrldesc = self.restMap[parsed_args.p1[0]]['delUrldesc']
            nodestr = input(reqUrldesc)
            base_url = "{}/{}".format(base_url,nodestr)
        if 'delUrlappend' in self.restMap[parsed_args.p1[0]] :
            base_url = "{}/{}".format(base_url,self.restMap[parsed_args.p1[0]]['delUrlappend'])
        if token:
            base_url = "{}?token={}".format(base_url,token)


        if 'delarg' in self.restMap[parsed_args.p1[0]] and 'delargdef' in self.restMap[parsed_args.p1[0]]:
            reqargdef =  self.restMap[parsed_args.p1[0]]['delargdef']
            reqarg = self.restMap[parsed_args.p1[0]]['delarg']
            if 'delargdesc' in self.restMap[parsed_args.p1[0]] :
                reqargdesc =  self.restMap[parsed_args.p1[0]]['delargdesc']
            #if reqargdef and reqarg :

            if type(reqarg) is str:
                ##print('字符串')
                if reqargdef is None:
                    attr = input(reqargdesc)
                    base_url = "{}&{}={}".format(base_url,reqarg,attr)
                    #此处比较特殊 因为restful接口很多没有按照post方式封装bean而是用的url参数 为了方便body体和url都加参数
                    body[reqargdef] = attr
                elif reqargdef =="auth_username":
                    base_url = "{}&{}={}".format(base_url,reqarg,auth_info["username"])
                    body[reqargdef] = auth_info["username"]
                else:
                    base_url = "{}&{}={}".format(base_url,reqarg,reqargdef)
                    body[reqargdef] = reqargdef
            else:
                ##print('数组')
                for index in range(len(reqarg)):
                    if reqargdef is None or reqargdef[index] is None:
                        attr = input(reqargdesc[index])
                        base_url = "{}&{}={}".format(base_url,reqarg[index],attr)
                        body[reqarg[index]] = attr
                    elif reqargdef[index] =="auth_username":
                        base_url = "{}&{}={}".format(base_url,reqarg[index],auth_info["username"])
                        body[reqarg[index]] = auth_info["username"]
                    else:
                        base_url = "{}&{}={}".format(base_url,reqarg[index],reqargdef[index])
                        body[reqarg[index]] = reqargdef[index]
        if 'delbody' in self.restMap[parsed_args.p1[0]]:
            #print('--------------------------------')
            body = self.restMap[parsed_args.p1[0]]['delbody']
            #print(body)
            #print('--------------------------------')
        body_data = json.dumps(body)
        #print(self.restMap[parsed_args.p1[0]])
        if 'delbodyjson' in self.restMap[parsed_args.p1[0]]:
            body_data = input(self.restMap[parsed_args.p1[0]]['delbodyjson'])
        #print(body_data)
        #print(base_url)
        return base_url,nodestr,body_data


    def take_action(self, parsed_args):
        super(CommonDelete, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        auth_info["token"] = token
        headers = {"Content-Type": "application/json"}
        ##print(parsed_args.p1[0])
        ##print(parsed_args.p1[1])
        url,nodestr,body_data = self._build_url(auth_info,parsed_args)
        prompt = self.restMap[parsed_args.p1[0]]['delconfirm'].format(nodestr)
        select = input(prompt)
        if select.upper() != "Y":
            return
        response = requests.delete(url,  data=body_data, headers=headers)
        #print(response)
        ok = tool.parse_response(response, None)
        if ok:
            self.app.LOG.info("Succeed to remove {}".format(nodestr))
        else:
            self.app.LOG.info("Failed to remove {}".format(nodestr))


class CommonUpload(Command,Yml):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(CommonUpload, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(CommonUpload, self).get_parser(prog_name))
        parser.add_argument("p1",  nargs=1, help="restful api uri key")
        return parser

    def _build_url(self,auth_info, parsed_args):
        address = auth_info["address"]
        port = auth_info["port"]
        token = auth_info['token']
        body = {'enctype':'multipart/form-data'}



        if 'uploadfilepath' in self.restMap[parsed_args.p1[0]]:
            uploadfilepath = self.restMap[parsed_args.p1[0]]['uploadfilepath']
            path = input(uploadfilepath)
        ##print(path.split('/')[-1])
        #file ={'fileName':path.split('/')[0],'file':open(path,'rb')}
        file ={'file':open(path,'rb')}
        base_url = "http://{}:{}/s".format(address, port)
        if parsed_args.p1:
            base_url = "{}{}".format(base_url,self.restMap[parsed_args.p1[0]]['uploadUrl'])

        if 'uploadUrlReplaceAttr' in self.restMap[parsed_args.p1[0]] :

            getUrlReplaceAttr = self.restMap[parsed_args.p1[0]]['uploadUrlReplaceAttr']

            if type(getUrlReplaceAttr) is str:
                getUrlReplace = self.restMap[parsed_args.p1[0]]['uploadUrlReplace']
                if 'uploadUrlReplacedef' in self.restMap[parsed_args.p1[0]]:
                    base_url = base_url.replace(getUrlReplace,self.restMap[parsed_args.p1[0]]['uploadUrlReplacedef'])
                else:
                    attr = input(getUrlReplaceAttr)
                    #print(base_url)
                    base_url = base_url.replace(getUrlReplace,attr)
                    #print(base_url)
            else:
                getUrlReplace = self.restMap[parsed_args.p1[0]]['uploadUrlReplace']
                for index in range(len(getUrlReplaceAttr)):
                    if 'uploadUrlReplacedef' in self.restMap[parsed_args.p1[0]]:
                        base_url = base_url.replace(getUrlReplace[index],
                                                    self.restMap[parsed_args.p1[0]]['uploadUrlReplacedef'][index])
                    else:
                        attr = input(getUrlReplaceAttr[index])
                        #print(base_url)
                        base_url = base_url.replace(getUrlReplace[index],attr)
                        #print(base_url)

        if 'uploadUrldesc' in self.restMap[parsed_args.p1[0]]:
            reqUrldesc = self.restMap[parsed_args.p1[0]]['uploadUrldesc']
            attr = input(reqUrldesc)
            base_url = "{}/{}".format(base_url,attr)
        if 'uploadUrlappend' in self.restMap[parsed_args.p1[0]] :
            base_url = "{}/{}".format(base_url,self.restMap[parsed_args.p1[0]]['uploadUrlappend'])
        if token:
            base_url = "{}?token={}".format(base_url,token)

        if 'uploadarg' in self.restMap[parsed_args.p1[0]] and 'uploadargdef' in self.restMap[parsed_args.p1[0]]:
            reqargdef =  self.restMap[parsed_args.p1[0]]['uploadargdef']
            reqarg = self.restMap[parsed_args.p1[0]]['uploadarg']
            if 'uploadargdesc' in self.restMap[parsed_args.p1[0]] :
                reqargdesc =  self.restMap[parsed_args.p1[0]]['uploadargdesc']
            #if reqargdef and reqarg :
            if type(reqarg) is str:
                ##print('字符串')
                if reqargdef is None:
                    attr = input(reqargdesc)
                    base_url = "{}&{}={}".format(base_url,reqarg,attr)
                    #此处比较特殊 因为restful接口很多没有按照post方式封装bean而是用的url参数 为了方便body体和url都加参数
                    body[reqarg] = attr
                elif reqargdef =="auth_username":
                    base_url = "{}&{}={}".format(base_url,reqarg,auth_info["username"])
                    body[reqarg] = auth_info["username"]
                elif reqargdef =="file_Size":
                    fsize = os.path.getsize(path)
                    base_url = "{}&{}={}".format(base_url,reqarg,fsize)
                    body[reqarg] = fsize
                else:
                    base_url = "{}&{}={}".format(base_url,reqarg,reqargdef)
                    body[reqarg] = reqargdef
            else:
                ##print('数组')
                for index in range(len(reqarg)):
                    if reqargdef is None or reqargdef[index] is None:
                        attr = input(reqargdesc[index])
                        base_url = "{}&{}={}".format(base_url,reqarg[index],attr)
                        body[reqarg[index]] = attr
                    elif reqargdef[index] =="auth_username":
                        base_url = "{}&{}={}".format(base_url,reqarg[index],auth_info["username"])
                        body[reqarg[index]] = auth_info["username"]
                    elif reqargdef[index] =="file_Size":
                        fsize = os.path.getsize(path)
                        base_url = "{}&{}={}".format(base_url,reqarg[index],fsize)
                        body[reqarg[index]] = fsize
                    else:
                        base_url = "{}&{}={}".format(base_url,reqarg[index],reqargdef[index])
                        body[reqarg[index]] = reqargdef[index]
        #body_data = json.dumps(body)
        # if 'bodyjson' in self.restMap[parsed_args.p1[0]]:
        #     body_data = input(self.restMap[parsed_args.p1[0]]['bodyjson'])
        # print(base_url)
        return base_url,body,file

    def take_action(self, parsed_args):
        super(CommonUpload, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        auth_info["token"] = token
        build_url,body_data,file=self._build_url(auth_info,parsed_args)
        response = requests.post(build_url, data=body_data,files=file)
        # print(response)
        ok = tool.parse_response(response, None)
        if ok:
            self.app.LOG.info("Succeed to add ")
        else:
            self.app.LOG.info("Failed to add {}".format(body_data))


class CommonDownload(ShowOne,Yml):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(CommonDownload, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(CommonDownload, self).get_parser(prog_name))
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
            base_url = "{}{}".format(base_url,self.restMap[parsed_args.p1[0]]['getUrl'])

        if 'getUrlReplaceAttr' in self.restMap[parsed_args.p1[0]] :

            getUrlReplaceAttr = self.restMap[parsed_args.p1[0]]['getUrlReplaceAttr']

            if type(getUrlReplaceAttr) is str:
                getUrlReplace = self.restMap[parsed_args.p1[0]]['getUrlReplace']
                if 'getUrlReplacedef' in self.restMap[parsed_args.p1[0]]:
                    attr = self.restMap[parsed_args.p1[0]]['getUrlReplacedef']
                else:
                    attr = input(getUrlReplaceAttr)

                #print(base_url)
                base_url = base_url.replace(getUrlReplace,attr)
                #print(base_url)
            else:
                getUrlReplace = self.restMap[parsed_args.p1[0]]['getUrlReplace']
                for index in range(len(getUrlReplaceAttr)):
                    if 'getUrlReplacedef' in self.restMap[parsed_args.p1[0]]:
                        attr = self.restMap[parsed_args.p1[0]]['getUrlReplacedef'][index]
                    else:
                        attr = input(getUrlReplaceAttr[index])

                    #print(base_url)
                    base_url = base_url.replace(getUrlReplace[index],attr)
                    #print(base_url)

        if 'getUrldesc' in self.restMap[parsed_args.p1[0]]:
            reqUrldesc = self.restMap[parsed_args.p1[0]]['getUrldesc']
            attr = input(reqUrldesc)
            base_url = "{}/{}".format(base_url,attr)
        if 'getUrlappend' in self.restMap[parsed_args.p1[0]] :
            base_url = "{}/{}".format(base_url,self.restMap[parsed_args.p1[0]]['getUrlappend'])
        if token:
            base_url = "{}?token={}".format(base_url,token)


        if 'getarg' in self.restMap[parsed_args.p1[0]] and 'getargdef' in self.restMap[parsed_args.p1[0]]:
            reqargdef =  self.restMap[parsed_args.p1[0]]['getargdef']
            reqarg = self.restMap[parsed_args.p1[0]]['getarg']

            if 'getargdesc' in self.restMap[parsed_args.p1[0]] :
                reqargdesc =  self.restMap[parsed_args.p1[0]]['getargdesc']
            #if reqargdef and reqarg :
            if type(reqarg) is str:
                ##print('字符串')
                if reqargdef is None:
                    attr = input(reqargdesc)
                    if 'getargfun' in self.restMap[parsed_args.p1[0]] :
                        attr = fun_zab(self.restMap[parsed_args.p1[0]]['getargfun'],attr)
                        #print(attr)
                    base_url = "{}&{}={}".format(base_url,reqarg,attr)
                elif reqargdef =="auth_username":
                    base_url = "{}&{}={}".format(base_url,reqarg,auth_info["username"])
                else:
                    base_url = "{}&{}={}".format(base_url,reqarg,reqargdef)
            else:
                ##print('数组')
                for index in range(len(reqarg)):
                    if reqargdef is None or reqargdef[index] is None:
                        attr = input(reqargdesc[index])
                        if 'getargfun' in self.restMap[parsed_args.p1[0]] :
                            if self.restMap[parsed_args.p1[0]]['getargfun'][index]  is not None:
                                attr = fun_zab(self.restMap[parsed_args.p1[0]]['getargfun'][index],attr)
                                #print(attr)
                        base_url = "{}&{}={}".format(base_url,reqarg[index],attr)
                    elif reqargdef[index] =="auth_username":
                        base_url = "{}&{}={}".format(base_url,reqarg[index],auth_info["username"])
                    else:
                        base_url = "{}&{}={}".format(base_url,reqarg[index],reqargdef[index])

        #print(base_url)
        return base_url

    def take_action(self, parsed_args):

        super(CommonDownload, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)

        auth_info["token"] = token
        headers = {"Content-Type": "application/json"}#"text/plain"
        response = requests.get(self._build_url(auth_info,parsed_args), headers=headers)#params=[]
        #print(response)
        #if parsed_args.p1[1]:
        ok, data = tool.parse_response(response)

        return self._data_formats(data, ok,parsed_args)

    def _data_formats(self, data, ok,parsed_args):
        rtn1 = []
        #'respcolumns':'name,crt,JobType'

        if 'respcolumns' in self.restMap[parsed_args.p1[0]]:
            colArray = self.restMap[parsed_args.p1[0]]['respcolumns'];
            for index in range(len(colArray)):
                rtn1.append(data[colArray[index]])
            return self.restMap[parsed_args.p1[0]]['respcolumndesc'], rtn1
        else:
            return data

class CommonPut(Lister,Yml):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(CommonPut, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(CommonPut, self).get_parser(prog_name))
        parser.add_argument("p1",  nargs=1, help="restful api uri key")
        return parser

    def _build_url(self,auth_info,parsed_args,ymlobj):
        address = auth_info["address"]
        port = auth_info["port"]
        token = auth_info['token']
        body = {}
        base_url = "http://{}:{}/s{}".format(address, port,ymlobj['putUrl'])

        if 'putUrlReplaceAttr' in ymlobj :
            getUrlReplaceAttr = ymlobj['putUrlReplaceAttr']
            if type(getUrlReplaceAttr) is str:
                getUrlReplace = ymlobj['putUrlReplace']
                if 'putUrlReplacedef' in ymlobj:
                    base_url = base_url.replace(getUrlReplace,ymlobj['putUrlReplacedef'])
                else:
                    attr = input(getUrlReplaceAttr)
                    base_url = base_url.replace(getUrlReplace,attr)
            else:
                getUrlReplace = ymlobj['putUrlReplace']
                for index in range(len(getUrlReplaceAttr)):
                    if 'putUrlReplacedef' in ymlobj:
                        base_url = base_url.replace(getUrlReplace[index],ymlobj['putUrlReplacedef'][index])
                    else:
                        attr = input(getUrlReplaceAttr[index])
                        base_url = base_url.replace(getUrlReplace[index],attr)
        if 'putUrldesc' in ymlobj:
            reqUrldesc = ymlobj['putUrldesc']
            attr = input(reqUrldesc)
            base_url = "{}/{}".format(base_url,attr)
        if 'putUrlappend' in ymlobj :
            base_url = "{}/{}".format(base_url,ymlobj['putUrlappend'])
        if token:
            base_url = "{}?token={}".format(base_url,token)
        if 'putarg' in ymlobj and 'putargdef' in ymlobj:
            reqargdef =  ymlobj['putargdef']
            reqarg = ymlobj['putarg']
            if 'putargdesc' in ymlobj :
                reqargdesc =  ymlobj['putargdesc']
            #if reqargdef and reqarg :
            if type(reqarg) is str:
                ##print('字符串')
                if reqargdef is None:
                    attr = input(reqargdesc)
                    base_url = "{}&{}={}".format(base_url,reqarg,attr)
                    #此处比较特殊 因为restful接口很多没有按照post方式封装bean而是用的url参数 为了方便body体和url都加参数
                    body[reqargdef] = attr
                elif reqargdef =="auth_username":
                    base_url = "{}&{}={}".format(base_url,reqarg,auth_info["username"])
                    body[reqargdef] = auth_info["username"]
                elif reqargdef.endswith('_fun'):
                    fun_ymlobj = self.restMap[reqargdef]
                    base_url_fun,body_data = self._build_url(auth_info,parsed_args,fun_ymlobj)
                    headers = {"Content-Type": "application/json"}
                    response = requests.get(base_url_fun, headers=headers)
                    ok, data = tool.parse_response(response, fun_ymlobj['resp'])
                    body = data

                else:
                    base_url = "{}&{}={}".format(base_url,reqarg,reqargdef)
                    body[reqargdef] = reqargdef
            else:
                ##print('数组')
                for index in range(len(reqarg)):
                    if reqargdef is None or reqargdef[index] is None:
                        attr = input(reqargdesc[index])
                        base_url = "{}&{}={}".format(base_url,reqarg[index],attr)
                        body[reqarg[index]] = attr
                    elif reqargdef[index] =="auth_username":
                        base_url = "{}&{}={}".format(base_url,reqarg[index],auth_info["username"])
                        body[reqarg[index]] = auth_info["username"]
                    elif reqargdef[index].endswith('_fun'):
                        fun_ymlobj = self.restMap[reqargdef[index]]
                        base_url_fun,body_data = self._build_url(auth_info,parsed_args,fun_ymlobj)
                        headers = {"Content-Type": "application/json"}
                        response = requests.get(base_url_fun, headers=headers)
                        ok, data = tool.parse_response(response, fun_ymlobj['resp'])
                        body = data
                    else:
                        base_url = "{}&{}={}".format(base_url,reqarg[index],reqargdef[index])
                        body[reqarg[index]] = reqargdef[index]


        if 'putbody' in ymlobj:
            #print('--------------------------------')
            body = ymlobj['putbody']
            #print(body)
            #print('--------------------------------')

        body_data = json.dumps(body)
        if 'bodyjson' in self.restMap[parsed_args.p1[0]]:
            body_data = input(self.restMap[parsed_args.p1[0]]['bodyjson'])
        #print(base_url)
        ##print(body_data)
        return base_url,body_data

    def take_action(self, parsed_args):
        super(CommonPut, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)

        auth_info["token"] = token
        headers = {"Content-Type": "application/json"}

        ymlobj = self.restMap[parsed_args.p1[0]]
        build_url,body_data=self._build_url(auth_info,parsed_args,ymlobj)
        #print(build_url)
        #print('lllllllllllllllllllllllllllllllllll')
        #print(body_data)
        response = requests.put(build_url, data=body_data, headers=headers)
        #print(response)

        status_code = response.status_code
        if status_code != 200 or 'resp' not in self.restMap[parsed_args.p1[0]]:
            # if response.message is not None:
            #     print(response.message)
            data = json.loads(response.text)
            print(data)
            return [],[]

        if parsed_args.p1:
            ok, data = tool.parse_response(response, ymlobj['resp'])
        return self._data_formats(data, ok,parsed_args)

    def _data_formats(self, datas, ok,parsed_args):
        rtn1 = []
        for data in datas:
            rtn2 = []
            #'respcolumns':'name,crt,JobType'
            colArray = self.restMap[parsed_args.p1[0]]['respcolumns'];
            for index in range(len(colArray)):
                # #print('======================' )
                # #print(data)
                # #print(colArray)
                rtn2.append(data[colArray[index]])
            rtn1.append(rtn2)

        ##print(rtn1)

        return self.restMap[parsed_args.p1[0]]['respcolumndesc'], rtn1
        # ok = tool.parse_response(response, self.restMap[parsed_args.p1[0]]['resp'])
        # if ok:
        #     self.app.LOG.info("Succeed to add ")
        # else:
        #     self.app.LOG.info("Failed to add {}".format(body_data))


def fun_zab(fun_name,str):
    #print('11111111111111111111111111111111111111')
    if fun_name == 'zab':
        return "{}{}".format(str,'-zabbix-agent')
    return str