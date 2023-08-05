import requests
import aimaxsdk.tool as tool

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

