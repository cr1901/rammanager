RAM Manager
===========

This application provides a database store and viewer for documenting
RAM addresses in reverse engineering SNES games.

Right now, the client and server are meant for SNES-formatted addresses
(``bank:offset``), but the provided RESTful-like API is not bound to
this format.

Contrary to Flask's recommendations, I use the built-in Flask HTTP
server to run this application. Because this is meant for a single user
to interactively update I feel this works fine.

Installation
------------

| To install RAM Manager, simply run setup.py:
| ``python3 setup.py install`` or ``python3 setup.py develop``

| To invoke a RAM Manager, use the following command:
| ``python3 -m rammanager [config_file]``

``[config_file]`` is an *absolute* path (I'll work on this), which
contains the following fields:

-  ``STORE``: *Absolute* path to the file backing store for the
   database. Required.
-  ``NAME``: Name of the application. Optional/not used.

REST API
--------

-  ``GET /ram``: Get JSON representation of all entries in database.
-  ``GET /ram/[0-9a-f]*``: Get JSON representation of all entries whose
   *leading digits* match the supplied address. Note that the
   bank:offset separating colon is not included. The provided client
   will strip this for you.
-  ``PUT /ram/[0-9a-f]*``: Add or update a RAM address. The server
   expects an ``application/json`` Content-Type, which is accepted by
   the following schema:

::

    {
      "$schema": "http://json-schema.org/draft-04/schema#",
      "type": "object",
      "properties": {
        "type": {
          "type": "string"
        },
        "description": {
          "type": "string"
        },
        "size": {
          "type": "string"
        },
        "address": {
          "type": "string"
        }
      },
      "required": [
        "address"
      ]
    }

-  ``DELETE /ram/[0-9a-f]*``: Remove a RAM address. The server expects
   an ``application/json`` Content-Type, which is accepted by the above
   schema.
