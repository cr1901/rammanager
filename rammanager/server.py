import json
import bisect
import os.path
from rammanager.address import LOROM

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

from flask import jsonify, abort, g, url_for, request

from rammanager import app


class DefaultConfig(object):
    NAME = ""
    STORE = "ramstore.json"

app.config.from_object(DefaultConfig)


# Handle tinydb creation/teardown. Taken straight from manual.
def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = TinyDB(app.config["STORE"],
                                  storage=CachingMiddleware(JSONStorage))
    return db


@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def open_viewer():
    return app.send_static_file("index.html")


@app.route("/jquery-3.0.0.js")
def send_jquery():
    return app.send_static_file("jquery-3.0.0.js")


@app.route("/ram", methods=["GET"])
def get_all():
    all_entries = get_db().all()
    if not all_entries:
        abort(404)
    return jsonify(sorted(all_entries, key=lambda k: k["address"]))


@app.route("/ram/<addr>", methods=["GET"])
def get_addr(addr):
    str_addr = addr[0:2] + ":" + addr[2:]
    db = get_db()
    var = Query()
    # addr is a string in this case!
    ram_vars = db.search(var.address.search(str_addr))
    if not ram_vars:
        abort(404)
    return jsonify(sorted(ram_vars, key=lambda k: k["address"]))


@app.route("/ram/<addr>", methods=["PUT"])
def add_addr(addr):
    if request.headers["Content-Type"] != "application/json":
        print(request.headers["Content-Type"])
        abort(400)
    try:
        json_req = json.loads(request.data.decode("utf-8"))
        addr = repr(LOROM(int(json_req["address"], 16), flat=False))
        data = {"address": addr,
                "type": json_req["type"],
                "size": json_req["size"],
                "description": json_req["description"]}
    except:
        # TODO: Better error handlers which return messages
        # indicating what went wrong. Return deleted added/entries?
        # Perhaps return what "GET" for the given input would send
        # after updating, given an input address range?
        abort(500)

    db = get_db()
    var = Query()
    if not db.contains(var.address == addr):
        db.insert(data)
        resp = "CREATED"
        code = 201
    else:
        db.update(data, var.address == addr)
        resp = "UPDATED"
        code = 200
        # Return 204? But client should refresh view.
    return (resp, code)


@app.route("/ram/<addr>", methods=["DELETE"])
def delete_addr(addr):
    if request.headers["Content-Type"] != "application/json":
        abort(400)
    json_req = json.loads(request.data.decode("utf-8"))
    addr = repr(LOROM(int(json_req["address"], 16), flat=False))

    db = get_db()
    var = Query()
    if db.contains(var.address == addr):
        db.remove(var.address == addr)
    else:
        abort(404)
    return "DELETED"
