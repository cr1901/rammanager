# TODO: Add run.py to top-level directory instead?

import os
import argparse
from rammanager import app


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Run a RAM Manager server")
    parser.add_argument('configuration', help='Config file location')
    args = parser.parse_args()

    app.config.from_pyfile(args.configuration)
    app.run()
