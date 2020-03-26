#!/usr/bin/env python

import threading, argparse, json
from flask import Flask, request
from flask_restplus import Resource, Api, fields
from werkzeug.middleware.proxy_fix import ProxyFix

class OxfsAgent:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.files = []
        self.directories = []
        self.lock = threading.Lock()

    def append(self, path, ptye):
        self.lock.acquire()
        if 'd' == ptye:
            self.directories.append(path)
        else:
            self.files.append(path)

        self.lock.release()

    def steal(self):
        self.lock.acquire()
        message = self.dumps()
        self.directories = []
        self.files = []
        self.lock.release()
        return message

    def dumps(self):
        return json.dumps(
            {
                'files': self.files,
                'directories': self.directories
            })

    def run(self):
        apiserver = self
        self.app = Flask(__name__)
        self.app.wsgi_app = ProxyFix(self.app.wsgi_app)
        self.api = Api(self.app, version='0.1', title='Oxfs Agent Api',
                       description='The Oxfs Agent Api')

        fs_namespace = self.api.namespace('fs', description='fs operations')
        status_model = self.api.model(
            'Status',
            {
                'status': fields.Boolean,
                'data': fields.String
            })

        put_args = self.api.parser()
        put_args.add_argument('path', required=True, help='full path')
        put_args.add_argument('type', required=True, help='path type')
        @fs_namespace.route('/path/put')
        @fs_namespace.expect(put_args)
        class PutPath(Resource):
            @fs_namespace.marshal_with(status_model, envelope='data')
            def put(self):
                args = put_args.parse_args()
                apiserver.append(args['path'], args['type'])
                return {'status': True, 'data': 'success'}


        fetch_args = self.api.parser()
        fetch_args.add_argument('clear', required=True, help='clear after fetch')
        @fs_namespace.route('/path/fetch')
        @fs_namespace.expect(fetch_args)
        class GetPath(Resource):
            @fs_namespace.marshal_with(status_model, envelope='data')
            def get(self):
                args = fetch_args.parse_args()
                if 'yes' == args['clear']:
                    message = apiserver.steal()
                else:
                    message = apiserver.dumps()
                return {'status': True, 'data': message}

        self.app.run(host=self.host, port=self.port)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bind', dest='bind', help='eg: 0.0.0.0')
    parser.add_argument('-p', '--port', dest='port', type=int, help='eg: 1234')
    args = parser.parse_args()

    port = 2020
    bind = '0.0.0.0'
    if args.bind:
        bind = args.bind
    if args.port:
        port = args.port

    agent = OxfsAgent(bind, port)
    agent.run()

if '__main__' == __name__:
    main()
