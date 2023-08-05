# coding: utf-8
import json
import json.encoder


class MyJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bytes):
            return o.decode(errors='ignore')


def test_it():
    test = ['hi', b'world']
    print(json.dumps(test, ensure_ascii=False, cls=MyJsonEncoder))
