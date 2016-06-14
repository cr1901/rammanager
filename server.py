import json
import bisect
import os.path
from snes.rom import LOROM

from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

from flask import Flask, jsonify, abort, g, url_for, request


class DefaultConfig(object):
    NAME=""
    STORE="ramstore.json"

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(DefaultConfig)
app.config.from_pyfile("application.cfg")


# Handle tinydb creation/teardown. Taken straight from manual.
def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = TinyDB(os.path.join(app.instance_path,
          app.config["STORE"]),
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
    return jsonify(sorted(get_db().all(), key=lambda k: k["address"]))

@app.route("/ram/<addr>", methods=["PUT"])
def add_addr(addr):
    if request.headers["Content-Type"]  != "application/json":
        print(request.headers["Content-Type"])
        abort(400)
    #try:
    json_req = json.loads(request.data.decode("utf-8"))
    addr = repr(LOROM(int(json_req["address"], 16), flat=False))
    data = {"address" : addr,
            "type" : json_req["type"],
            "size" : json_req["size"],
            "description" : json_req["description"]}
    #except:
    #    abort(400)

    db = get_db()
    var = Query()
    if not db.contains(var.address == addr):
        db.insert(data)
    else:
        db.update(data, var.address == addr)
    return "OK"


@app.route("/ram/<addr>", methods=["DELETE"])
def delete_addr(addr):
    if request.headers["Content-Type"]  != "application/json":
        print(request.headers["Content-Type"])
        abort(400)
    json_req = json.loads(request.data.decode("utf-8"))
    addr = repr(LOROM(int(json_req["address"], 16), flat=False))

    db = get_db()
    var = Query()
    if db.contains(var.address == addr):
        db.remove(var.address == addr)
    return "OK"


@app.route("/ram/<addr>", methods=["GET"])
def get_addr(addr):
    str_addr = addr[0:2] + ":" + addr[2:]
    var = Query()
    db = get_db()
    # addr is a string in this case!
    ram_vars = db.search(var.address.search(str_addr))

    # TODO: Should we return 404 if no match?
    # if not ram_vars:
    #    abort(404)
    return jsonify(sorted(ram_vars, key=lambda k: k["address"]))


if __name__ == "__main__":
    app.run()
