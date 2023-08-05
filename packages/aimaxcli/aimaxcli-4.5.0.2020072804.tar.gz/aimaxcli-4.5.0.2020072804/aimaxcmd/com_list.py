import os

from cliff.lister import Lister
from cliff.show import ShowOne
from cliff.command import Command
import aimaxcmd.cmds_base as base
import logging
import requests
import aimaxsdk.tool as tool
import json

from aimaxcmd.yml_list import Yml

ymlkey ={}
class CommonList(Lister,Yml):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(CommonList, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(CommonList, self).get_parser(prog_name))
        #parser = super(CommonList, self).get_parser(prog_name)
        #取 库的映射 增加如下 提示代码uri
        #aimax zone list
        i = len(parser.prog.split(' '))
        self.ymlkey = self.restMap[parser.prog.split(' ')[i-2]][parser.prog.split(' ')[i-1]]
        return parser

    def _build_url(self,auth_info, parsed_args):
        address = auth_info["address"]
        port = auth_info["port"]
        token = auth_info['token']
        base_url = "http://{}:{}/s".format(address, port)
        if 'reqUrl' in self.ymlkey:
            base_url = "{}{}".format(base_url,self.ymlkey['reqUrl'])
        if 'reqUrlReplaceAttr' in self.ymlkey :
            getUrlReplaceAttr = self.ymlkey['reqUrlReplaceAttr']
            if type(getUrlReplaceAttr) is str:
                getUrlReplace = self.ymlkey['reqUrlReplace']
                if 'reqUrlReplacedef' in self.ymlkey:
                    base_url = base_url.replace(getUrlReplace,self.ymlkey['reqUrlReplacedef'])
                else:
                    attr = input(getUrlReplaceAttr)
                    base_url = base_url.replace(getUrlReplace,attr)
            else:
                getUrlReplace = self.ymlkey['reqUrlReplace']
                for index in range(len(getUrlReplaceAttr)):
                    if 'reqUrlReplacedef' in self.ymlkey:
                        base_url = base_url.replace(getUrlReplace[index],
                                                    self.ymlkey['reqUrlReplacedef'][index])
                    else:
                        attr = input(getUrlReplaceAttr[index])
                        base_url = base_url.replace(getUrlReplace[index],attr)

        if 'reqUrldesc' in self.ymlkey:
            reqUrldesc = self.ymlkey['reqUrldesc']
            attr = input(reqUrldesc)
            base_url = "{}/{}".format(base_url,attr)
        if 'reqUrlappend' in self.ymlkey :
            base_url = "{}/{}".format(base_url,self.ymlkey['reqUrlappend'])
        if token:
            base_url = "{}?token={}".format(base_url,token)

        if 'reqarg' in self.ymlkey and 'reqargdef' in self.ymlkey:
            reqargdef =  self.ymlkey['reqargdef']
            reqarg = self.ymlkey['reqarg']
            if 'reqargdesc' in self.ymlkey :
                reqargdesc =  self.ymlkey['reqargdesc']
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
        if status_code != 200 or 'resp' not in self.ymlkey:
            # if response.message is not None:
            #     print(response.message)
            data = json.loads(response.text)
            print(data)
            return [],[]
        if self.ymlkey:
            ok, data = tool.parse_response(response, self.ymlkey['resp'])
        return self._data_formats(data, ok,parsed_args)

    def _data_formats(self, datas, ok,parsed_args):
        rtn1 = []
        print (datas)
        for data in datas:
            rtn2 = []
            colArray = self.ymlkey['respcolumns'];
            for index in range(len(colArray)):
                rtn2.append(data[colArray[index]])
            rtn1.append(rtn2)
        return self.ymlkey['respcolumndesc'], rtn1


class CommonShow(ShowOne,Yml):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(CommonShow, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(CommonShow, self).get_parser(prog_name))
        #print(parser.prog.split(' '))
        i = len(parser.prog.split(' '))
        self.ymlkey = self.restMap[parser.prog.split(' ')[i-2]][parser.prog.split(' ')[i-1]]
        return parser

    def _build_url(self,auth_info, parsed_args):
        address = auth_info["address"]
        port = auth_info["port"]
        token = auth_info['token']
        base_url = "http://{}:{}/s".format(address, port)
        if 'getUrl' in self.ymlkey:
            base_url = "{}{}".format(base_url,self.ymlkey['getUrl'])
        if 'getUrlReplaceAttr' in self.ymlkey :
            getUrlReplaceAttr = self.ymlkey['getUrlReplaceAttr']
            if type(getUrlReplaceAttr) is str:
                getUrlReplace = self.ymlkey['getUrlReplace']
                if 'getUrlReplacedef' in self.ymlkey:
                    base_url = base_url.replace(getUrlReplace,self.ymlkey['getUrlReplacedef'])
                else:
                    attr = input(getUrlReplaceAttr)
                    #print(base_url)
                    base_url = base_url.replace(getUrlReplace,attr)
                    #print(base_url)
            else:
                getUrlReplace = self.ymlkey['getUrlReplace']
                for index in range(len(getUrlReplaceAttr)):
                    if 'getUrlReplacedef' in self.ymlkey:
                        base_url = base_url.replace(getUrlReplace[index],self.ymlkey['getUrlReplacedef'][index])
                    else:
                        attr = input(getUrlReplaceAttr[index])
                        #print(base_url)
                        base_url = base_url.replace(getUrlReplace[index],attr)
                        #print(base_url)

        if 'getUrldesc' in self.ymlkey:
            reqUrldesc = self.ymlkey['getUrldesc']
            attr = input(reqUrldesc)
            base_url = "{}/{}".format(base_url,attr)
        if 'getUrlappend' in self.ymlkey :
            base_url = "{}/{}".format(base_url,self.ymlkey['getUrlappend'])
        if token:
            base_url = "{}?token={}".format(base_url,token)


        if 'getarg' in self.ymlkey and 'getargdef' in self.ymlkey:
            reqargdef =  self.ymlkey['getargdef']
            reqarg = self.ymlkey['getarg']
            if 'getargdesc' in self.ymlkey :
                reqargdesc =  self.ymlkey['getargdesc']
            #if reqargdef and reqarg :

            if type(reqarg) is str:
                ##print('字符串')
                if reqargdef is None:
                    attr = input(reqargdesc)
                    if 'getargfun' in self.ymlkey :
                        attr = fun_zab(self.ymlkey['getargfun'],attr)
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
                        if 'getargfun' in self.ymlkey :
                            if self.ymlkey['getargfun'][index]  is not None:
                                attr = fun_zab(self.ymlkey['getargfun'][index],attr)
                        base_url = "{}&{}={}".format(base_url,reqarg[index],attr)
                    elif reqargdef[index] =="auth_username":
                        base_url = "{}&{}={}".format(base_url,reqarg[index],auth_info["username"])
                    else:
                        base_url = "{}&{}={}".format(base_url,reqarg[index],reqargdef[index])
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
        if status_code != 200 or 'resp' not in self.ymlkey:
            data = json.loads(response.text)
            print(data)
            return [],[]

        ok, data = tool.parse_response(response)
        return self._data_formats(data, ok,parsed_args)

    def _data_formats(self, data, ok,parsed_args):
        rtn1 = []
        if 'respcolumns' in self.ymlkey:
            colArray = self.ymlkey['respcolumns'];
            for index in range(len(colArray)):
                rtn1.append(data[colArray[index]])
            return self.ymlkey['respcolumndesc'], rtn1
        else:
            return data

class CommonAdd(Command,Yml):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(CommonAdd, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(CommonAdd, self).get_parser(prog_name))
        i = len(parser.prog.split(' '))
        self.ymlkey = self.restMap[parser.prog.split(' ')[i-2]][parser.prog.split(' ')[i-1]]
        return parser

    def _build_url(self,auth_info, parsed_args):
        address = auth_info["address"]
        port = auth_info["port"]
        token = auth_info['token']
        body = {}
        base_url = "http://{}:{}/s".format(address, port)
        if 'addUrl' in self.ymlkey:
            base_url = "{}{}".format(base_url,self.ymlkey['addUrl'])
        if 'addUrlReplaceAttr' in self.ymlkey :
            getUrlReplaceAttr = self.ymlkey['addUrlReplaceAttr']
            if type(getUrlReplaceAttr) is str:
                getUrlReplace = self.ymlkey['addUrlReplace']
                if 'addUrlReplacedef' in self.ymlkey:
                    base_url = base_url.replace(getUrlReplace,self.ymlkey['addUrlReplacedef'])
                else:
                    attr = input(getUrlReplaceAttr)
                    base_url = base_url.replace(getUrlReplace,attr)
            else:
                getUrlReplace = self.ymlkey['addUrlReplace']
                for index in range(len(getUrlReplaceAttr)):
                    if 'addUrlReplacedef' in self.ymlkey:
                        base_url = base_url.replace(getUrlReplace[index],self.ymlkey['addUrlReplacedef'][index])
                    else:
                        attr = input(getUrlReplaceAttr[index])
                        base_url = base_url.replace(getUrlReplace[index],attr)

        if 'addUrldesc' in self.ymlkey:
            reqUrldesc = self.ymlkey['addUrldesc']
            attr = input(reqUrldesc)
            base_url = "{}/{}".format(base_url,attr)
        if 'addUrlappend' in self.ymlkey :
            base_url = "{}/{}".format(base_url,self.ymlkey['addUrlappend'])
        if token:
            base_url = "{}?token={}".format(base_url,token)

        if 'addarg' in self.ymlkey and 'addargdef' in self.ymlkey:
            reqargdef =  self.ymlkey['addargdef']
            reqarg = self.ymlkey['addarg']
            if 'addargdesc' in self.ymlkey :
                reqargdesc =  self.ymlkey['addargdesc']
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

        if 'body' in self.ymlkey:
            body = self.ymlkey['body']
            #print(body)
            if 'bodyarg' in self.ymlkey:
                addbodyarg = self.ymlkey['bodyarg']
                addbodydesc = self.ymlkey['bodydesc']
                addbodytype = self.ymlkey['bodytype']

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
        if 'bodyjson' in self.ymlkey:
            body_data = input(self.ymlkey['bodyjson'])
        print(base_url)
        return base_url,body_data

    def take_action(self, parsed_args):
        super(CommonAdd, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)

        auth_info["token"] = token
        headers = {"Content-Type": "application/json"}

        build_url,body_data=self._build_url(auth_info,parsed_args)
        response = requests.post(build_url, data=body_data, headers=headers)
        print(response)
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
        i = len(parser.prog.split(' '))
        self.ymlkey = self.restMap[parser.prog.split(' ')[i-2]][parser.prog.split(' ')[i-1]]
        return parser

    def _build_url(self,auth_info, parsed_args):
        address = auth_info["address"]
        port = auth_info["port"]
        token = auth_info['token']
        base_url = "http://{}:{}/s".format(address, port)
        nodestr = ''
        body = {}

        if 'delUrl' in self.ymlkey:
            base_url = "{}{}".format(base_url,self.ymlkey['delUrl'])
        if 'delUrlReplaceAttr' in self.ymlkey :
            getUrlReplaceAttr = self.ymlkey['delUrlReplaceAttr']
            if type(getUrlReplaceAttr) is str:
                getUrlReplace = self.ymlkey['delUrlReplace']
                if 'delUrlReplacedef' in self.ymlkey:
                    base_url = base_url.replace(getUrlReplace,self.ymlkey['delUrlReplacedef'])
                else:
                    attr = input(getUrlReplaceAttr)
                    base_url = base_url.replace(getUrlReplace,attr)
            else:
                getUrlReplace = self.ymlkey['delUrlReplace']
                for index in range(len(getUrlReplaceAttr)):
                    if 'delUrlReplacedef' in self.ymlkey:
                        base_url = base_url.replace(getUrlReplace[index],self.ymlkey['delUrlReplacedef'][index])
                    else:
                        attr = input(getUrlReplaceAttr[index])
                        base_url = base_url.replace(getUrlReplace[index],attr)
        if 'delUrldesc' in self.ymlkey:
            reqUrldesc = self.ymlkey['delUrldesc']
            nodestr = input(reqUrldesc)
            base_url = "{}/{}".format(base_url,nodestr)
        if 'delUrlappend' in self.ymlkey :
            base_url = "{}/{}".format(base_url,self.ymlkey['delUrlappend'])
        if token:
            base_url = "{}?token={}".format(base_url,token)


        if 'delarg' in self.ymlkey and 'delargdef' in self.ymlkey:
            reqargdef =  self.ymlkey['delargdef']
            reqarg = self.ymlkey['delarg']
            if 'delargdesc' in self.ymlkey :
                reqargdesc =  self.ymlkey['delargdesc']
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
        if 'delbody' in self.ymlkey:
            body = self.ymlkey['delbody']
        body_data = json.dumps(body)
        if 'delbodyjson' in self.ymlkey:
            body_data = input(self.ymlkey['delbodyjson'])
        return base_url,nodestr,body_data


    def take_action(self, parsed_args):
        super(CommonDelete, self).take_action(parsed_args)
        auth_info = self.auth_info_loader.load_auth_info(parsed_args)
        connections = self.app.connections
        token = base.get_token(auth_info, connections)
        auth_info["token"] = token
        headers = {"Content-Type": "application/json"}
        url,nodestr,body_data = self._build_url(auth_info,parsed_args)
        prompt = self.ymlkey['delconfirm'].format(nodestr)
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
        i = len(parser.prog.split(' '))
        self.ymlkey = self.restMap[parser.prog.split(' ')[i-2]][parser.prog.split(' ')[i-1]]
        return parser

    def _build_url(self,auth_info, parsed_args):
        address = auth_info["address"]
        port = auth_info["port"]
        token = auth_info['token']
        body = {'enctype':'multipart/form-data'}

        if 'uploadfilepath' in self.ymlkey:
            uploadfilepath = self.ymlkey['uploadfilepath']
            path = input(uploadfilepath)
        file ={'file':open(path,'rb')}
        base_url = "http://{}:{}/s".format(address, port)
        if 'uploadUrl' in self.ymlkey:
            base_url = "{}{}".format(base_url,self.ymlkey['uploadUrl'])

        if 'uploadUrlReplaceAttr' in self.ymlkey :

            getUrlReplaceAttr = self.ymlkey['uploadUrlReplaceAttr']

            if type(getUrlReplaceAttr) is str:
                getUrlReplace = self.ymlkey['uploadUrlReplace']
                if 'uploadUrlReplacedef' in self.ymlkey:
                    base_url = base_url.replace(getUrlReplace,self.ymlkey['uploadUrlReplacedef'])
                else:
                    attr = input(getUrlReplaceAttr)
                    #print(base_url)
                    base_url = base_url.replace(getUrlReplace,attr)
                    #print(base_url)
            else:
                getUrlReplace = self.ymlkey['uploadUrlReplace']
                for index in range(len(getUrlReplaceAttr)):
                    if 'uploadUrlReplacedef' in self.ymlkey:
                        base_url = base_url.replace(getUrlReplace[index],
                                                    self.ymlkey['uploadUrlReplacedef'][index])
                    else:
                        attr = input(getUrlReplaceAttr[index])
                        #print(base_url)
                        base_url = base_url.replace(getUrlReplace[index],attr)
                        #print(base_url)

        if 'uploadUrldesc' in self.ymlkey:
            reqUrldesc = self.ymlkey['uploadUrldesc']
            attr = input(reqUrldesc)
            base_url = "{}/{}".format(base_url,attr)
        if 'uploadUrlappend' in self.ymlkey :
            base_url = "{}/{}".format(base_url,self.ymlkey['uploadUrlappend'])
        if token:
            base_url = "{}?token={}".format(base_url,token)

        if 'uploadarg' in self.ymlkey and 'uploadargdef' in self.ymlkey:
            reqargdef =  self.ymlkey['uploadargdef']
            reqarg = self.ymlkey['uploadarg']
            if 'uploadargdesc' in self.ymlkey :
                reqargdesc =  self.ymlkey['uploadargdesc']
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
        i = len(parser.prog.split(' '))
        self.ymlkey = self.restMap[parser.prog.split(' ')[i-2]][parser.prog.split(' ')[i-1]]
        return parser

    def _build_url(self,auth_info, parsed_args):
        address = auth_info["address"]
        port = auth_info["port"]
        token = auth_info['token']
        base_url = "http://{}:{}/s".format(address, port)
        if 'getUrl' in self.ymlkey:
            base_url = "{}{}".format(base_url,self.ymlkey['getUrl'])
        if 'getUrlReplaceAttr' in self.ymlkey :
            getUrlReplaceAttr = self.ymlkey['getUrlReplaceAttr']
            if type(getUrlReplaceAttr) is str:
                getUrlReplace = self.ymlkey['getUrlReplace']
                if 'getUrlReplacedef' in self.ymlkey:
                    attr = self.ymlkey['getUrlReplacedef']
                else:
                    attr = input(getUrlReplaceAttr)
                base_url = base_url.replace(getUrlReplace,attr)
            else:
                getUrlReplace = self.ymlkey['getUrlReplace']
                for index in range(len(getUrlReplaceAttr)):
                    if 'getUrlReplacedef' in self.ymlkey:
                        attr = self.ymlkey['getUrlReplacedef'][index]
                    else:
                        attr = input(getUrlReplaceAttr[index])
                    base_url = base_url.replace(getUrlReplace[index],attr)

        if 'getUrldesc' in self.ymlkey:
            reqUrldesc = self.ymlkey['getUrldesc']
            attr = input(reqUrldesc)
            base_url = "{}/{}".format(base_url,attr)
        if 'getUrlappend' in self.ymlkey :
            base_url = "{}/{}".format(base_url,self.ymlkey['getUrlappend'])
        if token:
            base_url = "{}?token={}".format(base_url,token)

        if 'getarg' in self.ymlkey and 'getargdef' in self.ymlkey:
            reqargdef =  self.ymlkey['getargdef']
            reqarg = self.ymlkey['getarg']

            if 'getargdesc' in self.ymlkey :
                reqargdesc =  self.ymlkey['getargdesc']
            #if reqargdef and reqarg :
            if type(reqarg) is str:
                ##print('字符串')
                if reqargdef is None:
                    attr = input(reqargdesc)
                    if 'getargfun' in self.ymlkey :
                        attr = fun_zab(self.ymlkey['getargfun'],attr)
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
                        if 'getargfun' in self.ymlkey :
                            if self.ymlkey['getargfun'][index]  is not None:
                                attr = fun_zab(self.ymlkey['getargfun'][index],attr)
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
        ok, data = tool.parse_response(response)
        return self._data_formats(data, ok,parsed_args)

    def _data_formats(self, data, ok,parsed_args):
        rtn1 = []
        if 'respcolumns' in self.ymlkey:
            colArray = self.ymlkey['respcolumns'];
            for index in range(len(colArray)):
                rtn1.append(data[colArray[index]])
            return self.ymlkey['respcolumndesc'], rtn1
        else:
            return data

class CommonPut(Lister,Yml):
    log = logging.getLogger(__name__)

    def __init__(self, app, app_args):
        super(CommonPut, self).__init__(app, app_args)
        self.auth_info_loader = base.create_auth_info_builder(app, signed_in=True)

    def get_parser(self, prog_name):
        parser = self.auth_info_loader.filter_parser(super(CommonPut, self).get_parser(prog_name))
        i = len(parser.prog.split(' '))
        self.ymlkey = self.restMap[parser.prog.split(' ')[i-2]][parser.prog.split(' ')[i-1]]
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
                    #print(base_url)
                    base_url = base_url.replace(getUrlReplace,attr)
                    #print(base_url)
            else:
                getUrlReplace = ymlobj['putUrlReplace']
                for index in range(len(getUrlReplaceAttr)):
                    if 'putUrlReplacedef' in ymlobj:
                        base_url = base_url.replace(getUrlReplace[index],ymlobj['putUrlReplacedef'][index])
                    else:
                        attr = input(getUrlReplaceAttr[index])
                        #print(base_url)
                        base_url = base_url.replace(getUrlReplace[index],attr)
                        #print(base_url)

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
            body = ymlobj['putbody']
        body_data = json.dumps(body)
        if 'bodyjson' in self.ymlkey:
            body_data = input(self.ymlkey['bodyjson'])
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
        ymlobj = self.ymlkey
        build_url,body_data=self._build_url(auth_info,parsed_args,ymlobj)
        response = requests.put(build_url, data=body_data, headers=headers)
        #print(response)

        status_code = response.status_code
        if status_code != 200 or 'resp' not in self.ymlkey:
            # if response.message is not None:
            #     print(response.message)
            data = json.loads(response.text)
            print(data)
            return [],[]

        if 'resp' in self.ymlkey:
            ok, data = tool.parse_response(response, ymlobj['resp'])
        return self._data_formats(data, ok,parsed_args)

    def _data_formats(self, datas, ok,parsed_args):
        rtn1 = []
        for data in datas:
            rtn2 = []
            colArray = self.ymlkey['respcolumns'];
            for index in range(len(colArray)):
                rtn2.append(data[colArray[index]])
            rtn1.append(rtn2)

        return self.ymlkey['respcolumndesc'], rtn1
        # ok = tool.parse_response(response, self.ymlkey['resp'])
        # if ok:
        #     self.app.LOG.info("Succeed to add ")
        # else:
        #     self.app.LOG.info("Failed to add {}".format(body_data))


def fun_zab(fun_name,str):
    #print('11111111111111111111111111111111111111')
    if fun_name == 'zab':
        return "{}{}".format(str,'-zabbix-agent')
    return str