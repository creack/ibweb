#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""@package Main
Main application file
"""

from AppIB import AppIB
from sys import exit
from flask import Flask
#from Strategy import Strategy

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

if __name__ == "__main__":
    try:
        appIb = AppIB()
        appIb.start()
        app.run('0.0.0.0', 5001)
    except KeyboardInterrupt:
        exit(1)

