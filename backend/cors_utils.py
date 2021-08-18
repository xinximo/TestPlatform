#!/usr/bin/python3
# @Time    : 2021/4/10 11:17 下午
# @Author  : WangXin
from flask_restful import Resource


class TabrResource(Resource):
    def options(self):
        return {'Allow': '*'}, 200, {'Access-Control-Allow-Origin': '*',
                                     'Access-Control-Allow-Methods': 'HEAD, OPTIONS, GET, POST, DELETE, PUT',
                                     'Access-Control-Allow-Headers': 'Content-Type, Content-Length, Authorization, Accept, x-csrf-token,x-requested-with,token',
                                     }