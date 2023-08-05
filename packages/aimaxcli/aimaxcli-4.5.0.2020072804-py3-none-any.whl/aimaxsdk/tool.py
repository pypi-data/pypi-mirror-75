import json
from aimaxsdk import errors


def parse_response(response, *keys, cascade=True):
    status_code = response.status_code
    # if response.message is not None:
    #     print(response.message)
    if status_code == 200:
        data = json.loads(response.text)
        #print(data)
        if data["success"]:
            if cascade:
                for key in keys:
                    if isinstance(key, str):
                        #print('str')
                        if isinstance(data, list):
                            break
                        if key is None:
                            return True
                        data = data[key]
                    else:
                        if key is None:
                            return True
                        for ke in key:
                            if isinstance(data, list):
                                break
                            if ke is None:
                                return True
                            data = data[ke]

                return True, data
            else:
                values = []
                for key in keys:
                    values.append(data[key])
                return True, values
        else:
            if data["message"] in errors.all_errors:
                if data["messageParams"]:
                    return False, errors.all_errors[data["message"]].format(data["messageParams"])
                return False, errors.all_errors[data["message"]]
            else:
                return False, "Unknown Error"
    else:
        return False, status_code


    # def _data_se(self, datas,param,i):
    #
    #     if i< len(param):
    #         print("{}-{}".format(datas,param[i]))
    #         dt = datas[param[i]]
    #         i = i + 1
    #         return self._data_se(dt,param,i)
    #     else:
    #         return datas[param[i]]
    #
    # def _data_formatss(self, datas, ok,parsed_args):
    #     rtn1 = []
    #     for data in datas:
    #         rtn2 = []
    #         #'respcolumns':'name,crt,JobType'
    #         colArray = self.restMap[parsed_args.p1[0]]['respcolumns'];
    #         for index in range(len(colArray)):
    #             colOne = colArray[index]
    #             if type(colOne) is str:
    #                 print('its str {}'.format(index))
    #                 rtn2.append(data[colOne])
    #             else:
    #                 print('its array {}'.format(index))
    #
    #                 rtn2.append(self._data_se(data, colOne, 0))
    #
    #         rtn1.append(rtn2)
    #     return self.restMap[parsed_args.p1[0]]['respcolumndesc'], rtn1