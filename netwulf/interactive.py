# -*- coding: utf-8 -*-
"""
This module provides the necessary functions to start up a local
HTTP server and open an interactive d3-visualization of a network.
"""
from __future__ import print_function

import os
import sys

import http.server
import webbrowser
import time
import threading
from copy import deepcopy

import shutil

import netwulf as wulf

import json
from distutils.dir_util import copy_tree

import networkx as nx
from io import BytesIO

def mkdirp_customdir(directory='~/.netwulf/'):
    """simulate `mkdir -p` functionality"""

    directory = os.path.abspath(os.path.expanduser(directory))
    if not os.path.exists(directory):
        os.makedirs(directory)


html_source_path = os.path.join(wulf.__path__[0], 'js')


def _make_and_get_directory(path):
    """Simulate ``mkdir -p`` and return the path of the repository"""
    directory, _ = os.path.split(
        os.path.abspath(os.path.expanduser(path))
    )
    mkdirp_customdir(directory)
    return directory


def prepare_visualization_directory():
    """Move all files from the netwulf/js directory to ~/.netwulf"""
    src = html_source_path
    dst = os.path.abspath(os.path.expanduser("~/.netwulf/"))

    # always copy source files to the subdirectory
    copy_tree(src, dst)


class StoppableHTTPServer(http.server.HTTPServer):
    """Adapted from https://stackoverflow.com/questions/268629/how-to-stop-basehttpserver-serve-forever-in-a-basehttprequesthandler-subclass """

    # The handler will write in this attribute
    posted_data = None

    def __init__(self, server_address, handler, subjson):
        http.server.HTTPServer.__init__(self, server_address, handler)
        self.subjson = subjson

    def run(self):
        try:
            self.serve_forever()
        except OSError:
            pass

    def stop_this(self):
        # Clean-up server (close socket, etc.)
        print('was asked to stop the server')
        self.server_close()

        # try:
        for f in self.subjson:
            if os.path.exists(f):
                os.remove(f)

        print('deleted all files')


class customHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """A custom handler class adapted from
    https://stackoverflow.com/questions/6204029/extending-basehttprequesthandler-getting-the-posted-data
    and
    https://blog.anvileight.com/posts/simple-python-http-server/#do-post
    """

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(b'Successful POST request.')
        self.wfile.write(response.getvalue())

        # Save this posted data to the server object so it can be retrieved later on
        print("Successfully posted network data to Python!")
        self.server.posted_data = json.loads(body)



default_config = {
  'Apply heat (wiggle)': False,
  'Charge strength': -30,
  'Center gravity': 0.1,
  'Link distance': 10,
  'Link width': 2,
  'Link alpha': 0.5,
  'Node size': 10, 
  'Node stroke size': 0.5,
  'Node size exponent': 0.5,
  'Link width exponent': 0.5,
  'Collision': False,
  'Node fill': '#16a085',
  'Node stroke': '#000000',
  'Link stroke': '#7c7c7c',
  'Label stroke': '#000000',
  'Show labels': False,
  'Show singleton nodes': False,
  'Node size by strength': False,
  'Zoom': 1.5,
  'Min. link weight %': 0,
  'Max. link weight %': 100
}


def visualize(network,
              port=9853,
              config=None):
    """
    Visualize a network interactively using Ulf Aslak's d3 web app.
    Saves the network as json, saves the passed config and runs 
    a local HTTP server which then runs the web app.
    
    Parameters
    ==========
    network : networkx.Graph or networkx.DiGraph
        The network to visualize
    port : int, default : 9853
        The port at which to run the server locally.
    config : dict, default : None,
        In the default configuration, each key-value-pair will
        be overwritten with the key-value-pair provided in `config`.
        The default configuration is
        ```
            default_config = {
              'Apply heat (wiggle)': false,
              'Charge strength': -10,
              'Center gravity': 0.1,
              'Link distance': 10,
              'Link width': 2,
              'Link alpha': 0.5,
              'Node size': 5, 
              'Node stroke size': 0.5,
              'Node size exponent': 0.5,
              'Link strength exponent': 0.1,
              'Link width exponent': 0.5,
              'Collision': False,
              'Node fill': '#16a085',
              'Node stroke': '#000000',
              'Link stroke': '#7c7c7c',
              'Label stroke': '#000000',
              'Show labels': False,
              'Zoom': 1.5,
              'Min. link weight %': 0,
              'Max. link weight %': 100
        ```
    """

    this_config = deepcopy(default_config)
    if config is not None:
        this_config.update(config)

    path = "~/.netwulf/"
    mkdirp_customdir()
    web_dir = os.path.abspath(os.path.expanduser(path))

    # copy the html and js files for the visualizations
    prepare_visualization_directory()

    # create a json-file based on the current time
    file_id = "tmp_{:x}".format(int(time.time()*1000)) + ".json"
    filename = file_id
    configname = "config_" + filename

    filepath = os.path.join(web_dir, filename)
    configpath = os.path.join(web_dir, configname)

    with open(filepath,'w') as f:
        json.dump(nx.node_link_data(network), f)

    with open(configpath,'w') as f:
        json.dump(this_config, f)

    # change directory to this directory
    print("changing directory to", web_dir)
    print("starting server here ...", web_dir)
    cwd = os.getcwd()
    os.chdir(web_dir)

    server = StoppableHTTPServer(("127.0.0.1", port),
                                 customHTTPRequestHandler,
                                 [filepath, configpath],
                                 )

    # ========= start server ============
    thread = threading.Thread(None, server.run)
    thread.start()

    webbrowser.open("http://localhost:"+str(port)+"/?data=" + filename + "&config=" + configname)

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        print('stopping server ...')
        server.stop_this()
        thread.join()

    posted_data = server.posted_data

    print('changing directory back to', cwd)

    os.chdir(cwd)

    return posted_data


if __name__ == "__main__":
    # download_d3()
    G = nx.fast_gnp_random_graph(100,0.1)
    posted_data = visualize(G,config={'Node size':5})
    if posted_data is not None:
        print("received posted data:", posted_data)
