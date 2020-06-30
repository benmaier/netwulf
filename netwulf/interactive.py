# -*- coding: utf-8 -*-
"""
This module provides the necessary functions to start up a local
HTTP server and open an interactive d3-visualization of a network.
"""
from __future__ import print_function

import os
import sys
import simplejson as json
from distutils.dir_util import copy_tree
import base64
import http.server
import webbrowser
import time
import threading
from copy import deepcopy
import shutil
from io import BytesIO
import pathlib

import numpy

import networkx as nx
import netwulf as wulf

netwulf_user_folder = pathlib.Path('~/.netwulf/').expanduser()
html_source_path = (pathlib.Path(wulf.__path__[0]) / 'js').expanduser()

def _json_default(o):
    if isinstance(o, numpy.int64): return int(o)
    elif isinstance(o, numpy.float64): return float(o)
    raise TypeError

def mkdirp_customdir(directory=None):
    """simulate `mkdir -p` functionality"""
    if directory is None:
        directory = netwulf_user_folder

    try:
        directory = pathlib.Path(directory).expanduser().resolve()
    except FileNotFoundError as e:
        directory = pathlib.Path(directory).expanduser() # Python 3.5 compliant

    directory.mkdir(parents=True, exist_ok=True)

def prepare_visualization_directory():
    """Move all files from the netwulf/js directory to ~/.netwulf"""
    src = html_source_path
    dst = netwulf_user_folder

    # always copy source files to the subdirectory
    copy_tree(str(src), str(dst))

class NetwulfHTTPServer(http.server.HTTPServer):
    """Custom netwulf server class adapted from 
    https://stackoverflow.com/questions/268629/how-to-stop-basehttpserver-serve-forever-in-a-basehttprequesthandler-subclass """

    # The handler will write in this attribute
    posted_network_properties = None
    posted_config = None
    posted_image_base64 = None
 
    end_requested = False

    def __init__(self, server_address, handler, subjson, verbose=False):
        http.server.HTTPServer.__init__(self, server_address, handler)
        self.subjson = subjson
        self.verbose = verbose

    def run(self):
        try:
            self.serve_forever()
        except OSError:
            pass

    def serve_forever(self):
        """Handle one request at a time until doomsday."""
        while not self.end_requested:
            self.handle_request()
        if self.verbose:
            print("serve_forever() terminated")

    def stop_this(self):
        # Clean-up server (close socket, etc.)
        if self.verbose:
            print('was asked to stop the server')
        self.server_close()

        # try:
        for f in self.subjson:
            fPath = pathlib.Path(f)
            if fPath.exists():
                fPath.unlink()

        if self.verbose:
            print('deleted all files')


class NetwulfHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """A custom handler class adapted from
    https://stackoverflow.com/questions/6204029/extending-basehttprequesthandler-getting-the-posted-data
    and
    https://blog.anvileight.com/posts/simple-python-http-server/#do-post
    """

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])

        # an empty POST means the server should be stopped
        if content_length == 0:
            try:
                body = self.rfile.read(content_length)
                self.send_response(200)
                self.end_headers()
                response = BytesIO()
                response.write(b'Closing now.')
                self.wfile.write(response.getvalue())
            except: #this should actually catch a ConnectionError for windows or firefox
                pass
            self.server.end_requested = True
        else:
            body = self.rfile.read(content_length)
            self.send_response(200)
            self.end_headers()
            response = BytesIO()
            response.write(b'Successful POST request.')
            self.wfile.write(response.getvalue())

            # Save this posted data to the server object so it can be retrieved later on
            if self.server.verbose:
                print("Successfully posted network data to Python!")
            received_data = json.loads(body)
            self.server.posted_network_properties = received_data['network']
            self.server.posted_config = received_data['config']
            img = received_data['image'].split(',')[1]
            self.server.posted_image_base64 = base64.decodebytes(img.encode())


    def log_message(self, format, *args):
        if self.server.verbose:
            print(self.address_string(), self.log_date_time_string(), *args)



default_config = {
    # Input/output
    'zoom': 1,
    # Physics
    'node_charge': -45,
    'node_gravity': 0.1,
    'link_distance': 15,
    'link_distance_variation': 0,
    'node_collision': True,
    'wiggle_nodes': False,
    'freeze_nodes': False,
    # Nodes
    'node_fill_color': '#79aaa0',
    'node_stroke_color': '#555555',
    'node_label_color': '#000000',
    'display_node_labels': False,
    'scale_node_size_by_strength': False,
    'node_size': 5,
    'node_stroke_width': 1,
    'node_size_variation': 0.5,
    # Links
    'link_color': '#7c7c7c',
    'link_width': 2,
    'link_alpha': 0.5,
    'link_width_variation': 0.5,
    # Thresholding
    'display_singleton_nodes': True,
    'min_link_weight_percentile': 0,
    'max_link_weight_percentile': 1
}


def visualize(network,
              port=9853,
              verbose=False,
              config=None,
              plot_in_cell_below=True,
              is_test=False,
              ):
    """
    Visualize a network interactively using Ulf Aslak's d3 web app.
    Saves the network as json, saves the passed config and runs 
    a local HTTP server which then runs the web app.
    
    Parameters
    ----------
    network : networkx.Graph or networkx.DiGraph or node-link dictionary
        The network to visualize
    port : int, default : 9853
        The port at which to run the server locally.
    verbose : bool, default : False
        Be chatty.
    config : dict, default : None,
        In the default configuration, each key-value-pair will
        be overwritten with the key-value-pair provided in `config`.
        The default configuration is

        .. code:: python

            default_config = {
                # Input/output
                'zoom': 1,
                # Physics
                'node_charge': -45,
                'node_gravity': 0.1,
                'link_distance': 15,
                'link_distance_variation': 0,
                'node_collision': True,
                'wiggle_nodes': False,
                'freeze_nodes': False,
                # Nodes
                'node_fill_color': '#79aaa0',
                'node_stroke_color': '#555555',
                'node_label_color': '#000000',
                'display_node_labels': False,
                'scale_node_size_by_strength': False,
                'node_size': 5,
                'node_stroke_width': 1,
                'node_size_variation': 0.5,
                # Links
                'link_color': '#7c7c7c',
                'link_width': 2,
                'link_alpha': 0.5,
                'link_width_variation': 0.5,
                # Thresholding
                'display_singleton_nodes': True,
                'min_link_weight_percentile': 0,
                'max_link_weight_percentile': 1
            }

        When started from a Jupyter notebook, this will show a
        reproduced matplotlib figure of the stylized network
        in a cell below. Only works if ``verbose = False``.
    is_test : bool, default : False
        If ``True``, the interactive environment will post
        its visualization to Python automatically after 5 seconds.

    Returns
    -------
    network_properties : dict
        contains all necessary information to redraw the figure which
        was created in the interactive visualization
    config : dict
        contains all configurational values of the interactive
        visualization
    """

    this_config = deepcopy(default_config)
    if config is not None:
        this_config.update(config)

    path = netwulf_user_folder
    mkdirp_customdir()
    web_dir = pathlib.Path(path)

    # copy the html and js files for the visualizations
    prepare_visualization_directory()

    # create a json-file based on the current time
    file_id = "tmp_{:x}".format(int(time.time()*1000)) + ".json"
    filename = file_id
    configname = "config_" + filename

    filepath = str(web_dir / filename)
    configpath = str(web_dir / configname)

    with open(filepath,'w') as f:
        if type(network) in [nx.Graph, nx.DiGraph, nx.MultiDiGraph]:
            network = nx.node_link_data(network)
            if 'graph' in network:
                network.update(network['graph'])
                del network['graph']
            json.dump(network, f, iterable_as_array=True, default=_json_default)
        elif type(network) == dict:
            json.dump(network, f, iterable_as_array=True, default=_json_default)
        else:
            raise TypeError("Netwulf only supports `nx.Graph`, `nx.DiGraph`, `nx.MultiDiGraph`, or `dict`.")

    with open(configpath,'w') as f:
        json.dump(this_config, f, default=_json_default)

    # change directory to this directory
    if verbose:
        print("changing directory to", str(web_dir))
        print("starting server here ...", str(web_dir))
    cwd = os.getcwd()
    os.chdir(str(web_dir))

    server = NetwulfHTTPServer(("127.0.0.1", port),
                                 NetwulfHTTPRequestHandler,
                                 [filepath, configpath],
                                 verbose=verbose,
                                 )

    # ========= start server ============
    thread = threading.Thread(None, server.run)
    thread.start()

    url = "http://localhost:"+str(port)+"/?data=" + filename + "&config=" + configname
    if is_test:
        url += "&pytest"
    webbrowser.open(url)

    try:
        while not server.end_requested:
            time.sleep(0.1)
        is_keyboard_interrupted = False
    except KeyboardInterrupt:
        is_keyboard_interrupted = True
    
    server.end_requested = True

    if verbose:
        print('stopping server ...')
    server.stop_this()
    thread.join(0.2)

    posted_network_properties = server.posted_network_properties
    posted_config = server.posted_config

    if verbose:
        print('changing directory back to', cwd)

    os.chdir(cwd)
    
    # see whether or not the whole thing was started from a jupyter notebook and if yes,
    # actually re-draw the figure and display it
    env = os.environ
    try:
        is_jupyter = 'jupyter' in pathlib.PurePath(env['_']).name
    except: # this should actually be a key error
        # apparently this is how it has to be on Windows
        is_jupyter = 'JPY_PARENT_PID' in env

    if is_jupyter and plot_in_cell_below and not is_keyboard_interrupted:
        if verbose:
            print('recreating layout in matplotlib ...')
        if posted_network_properties is not None:
            fig, ax = wulf.draw_netwulf(posted_network_properties)

    return posted_network_properties, posted_config


if __name__ == "__main__":
    # download_d3()
    G = nx.fast_gnp_random_graph(100,2/100.)
    #G = nx.barabasi_albert_graph(100,1)
    posted_data = visualize(G,config={'collision':True},verbose=True)
    #if posted_data is not None:
    #    print("received posted data:", posted_data)
