import json
from flask import make_response


class Response:
    def __init__(self):
        self.status = 1
        self.message = "システムエラーが発生しました。"
        self.result = {}


def obj_to_dict(obj):
    return obj.__dict__


def get_response(response, html_status):
    json_text = json.dumps(response, ensure_ascii=False, default=obj_to_dict)
    resp = make_response(json_text, html_status)

    return resp
