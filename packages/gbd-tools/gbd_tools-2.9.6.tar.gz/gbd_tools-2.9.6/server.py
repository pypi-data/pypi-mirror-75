#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Global Benchmark Database (GBD)
# Copyright (C) 2019 Markus Iser, Luca Springer, Karlsruhe Institute of Technology (KIT)
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime
import logging
import os
import argparse

import werkzeug

from gbd_tool.util import eprint
from os.path import basename

import gbd_server

import tatsu
import flask
from flask import Flask, request, send_file, json, Response
from flask import render_template
from flask.logging import default_handler
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from gbd_tool.gbd_api import GbdApi
from tatsu import exceptions
from werkzeug.middleware.proxy_fix import ProxyFix

limiter = None
DATABASE = None
gbd_api = None
app = Flask(__name__)


@app.route("/", methods=['GET'])
def quick_search():
    return render_template('index.html')


@app.route("/results", methods=['POST'])
def quick_search_results_json():
    data = request.get_json(force=True, silent=True)
    if data is None:
        return Response("Bad Request", status=400, mimetype="text/plain")
    query = data.get('query')
    selected_groups = data.get('selected_groups')
    if not len(selected_groups):
        selected_groups.append("filename")
    available_groups = sorted(gbd_api.get_all_groups())
    available_groups.remove("local")
    groups = sorted(list(set(available_groups) & set(selected_groups)))
    try:
        rows = list(gbd_api.query_search(query, groups))
        groups.insert(0, "GBDhash")
        result = list(dict((groups[index], row[index]) for index in range(0, len(groups))) for row in rows)
        return Response(json.dumps(result), status=200, mimetype="application/json")
    except tatsu.exceptions.FailedParse:
        return Response("Malformed query", status=400, mimetype="text/plain")
    except ValueError:
        return Response("Attribute not Available", status=400, mimetype="text/plain")


@app.route("/getgroups", methods=['GET'])
def get_all_groups():
    available_groups = sorted(gbd_api.get_all_groups())
    available_groups.remove("local")
    return Response(json.dumps(available_groups), status=200, mimetype="application/json")


@app.route("/exportcsv", methods=['POST'])
def get_csv_file():
    data = request.get_json(force=True, silent=True)
    if data is None:
        return Response("Bad Request", status=400, mimetype="text")
    query = data.get('query')
    selected_groups = data.get('selected_groups')
    if not len(selected_groups):
        selected_groups.append("filename")
    results = gbd_api.query_search(query, selected_groups)
    headers = ["hash"] + selected_groups
    content = "\n".join([" ".join([str(entry) for entry in result]) for result in results])
    app.logger.info('Sending CSV file to {} at {}'.format(request.remote_addr, datetime.datetime.now()))
    file_name = "query_result.csv"
    return Response(" ".join(headers) + "\n" + content, mimetype='text/csv',
                    headers={"Content-Disposition": "attachment; filename=\"{}\"".format(file_name),
                             "filename": "{}".format(file_name)})


@app.route("/getinstances", methods=['POST'])
def get_url_file():
    data = request.get_json(force=True, silent=True)
    if data is None:
        return Response("Bad Request", status=400, mimetype="text")
    query = data.get('query')
    result = gbd_api.query_search(query, ["local"])
    # hashes = [row[0] for row in result]
    # content = "\n".join([flask.url_for("get_file", hashvalue=hv, _external=True) for hv in hashes])
    content = "\n".join(
        [os.path.join(flask.url_for("get_file", hashvalue=row[0], _external=True), os.path.basename(row[1])) for row in
         result])
    app.logger.info('Sending URL file to {} at {}'.format(request.remote_addr, datetime.datetime.now()))
    file_name = "query_result.uri"
    return Response(content, mimetype='text/uri-list',
                    headers={"Content-Disposition": "attachment; filename=\"{}\"".format(file_name),
                             "filename": "{}".format(file_name)})


@app.route('/attribute/<attribute>/<hashvalue>')
def get_attribute(attribute, hashvalue):
    try:
        values = gbd_api.search(attribute, hashvalue)
        if len(values) == 0:
            return Response("No entry in attribute table associated with this hash", status=404, mimetype="text/plain")
        return str(",".join(str(value) for value in values))
    except ValueError as err:
        return Response("Value Error: {}".format(err), status=500, mimetype="text/plain")


@app.route('/file/<hashvalue>', defaults={'filename': None})
@app.route('/file/<hashvalue>/<filename>')
def get_file(hashvalue, filename):
    values = gbd_api.search("local", hashvalue)
    if len(values) == 0:
        return Response("No according file found in our database", status=404, mimetype="text/plain")
    try:
        path = values.pop()
        return send_file(path, as_attachment=True, attachment_filename=os.path.basename(path))
    except FileNotFoundError:
        return Response("Files temporarily not accessible", status=404, mimetype="text/plain")


@app.route('/info/<hashvalue>')
def get_all_attributes(hashvalue):
    groups = gbd_api.get_all_groups()
    info = dict([])
    for attribute in groups:
        values = gbd_api.search(attribute, hashvalue)
        info.update({attribute: str(",".join(str(value) for value in values))})
    return Response(json.dumps(info), status=200, mimetype="application/json")


@app.route("/getdatabase", methods=['GET'])
def get_default_database_file():
    global DATABASE
    app.logger.info('Sending database to {} at {}'.format(request.remote_addr, datetime.datetime.now()))
    return send_file(DATABASE, as_attachment=True, attachment_filename=os.path.basename(DATABASE), mimetype='application/x-sqlite3')


def main():
    parser = argparse.ArgumentParser(description='Web- and Micro- Services to access global benchmark database.')
    parser.add_argument('-d', "--db", help='Specify database to work with', default=os.environ.get('GBD_DB'), nargs='?')
    parser.add_argument('-p', "--port", help='Specify port on which to listen', type=int)
    args = parser.parse_args()
    if not args.db:
        eprint("""No database path is given. 
A database path can be given in two ways:
-- by setting the environment variable GBD_DB
-- by giving a path via --db=[path]
A database file containing some attributes of instances used in the SAT Competitions can be obtained at http://gbd.iti.kit.edu/getdatabase
Don't forget to initialize each database with the paths to your benchmarks by using the init-command. """)
    else:
        logging_dir = "gbd-server-logs"
        logging_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), logging_dir)
        if not os.path.exists(logging_path):
            os.makedirs(logging_path)
        logging.basicConfig(filename='{}/server.log'.format(logging_path), level=logging.DEBUG)
        logging.getLogger().addHandler(default_handler)
        global DATABASE
        DATABASE = args.db
        global gbd_api
        gbd_api = GbdApi(DATABASE)
        global app
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1)
        app.config['database'] = DATABASE
        app.static_folder = os.path.join(os.path.dirname(os.path.abspath(gbd_server.__file__)), "static")
        app.template_folder = os.path.join(os.path.dirname(os.path.abspath(gbd_server.__file__)), "templates-vue")
        global limiter
        limiter = Limiter(app, key_func=get_remote_address)
        app.run(host='0.0.0.0', port=args.port)


if __name__ == '__main__':
    main()
