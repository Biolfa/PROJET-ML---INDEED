#! /usr/bin/env python
import sys
from os.path import dirname
sys.path.append(dirname(__file__))

from flask_website_dashboard.views import app

if __name__ == "__main__":
    app.run(debug=True)
