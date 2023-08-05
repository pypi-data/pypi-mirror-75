#!/usr/bin/python3

import graphviz as gv
import tensorflow as tf

from typing import Union

from .exceptions import *

class visualizer():
    """
    Neural Network visualizer class

    Parameters
    ----------
    title : str
        Name of the image file
    file_type : str
        Extension of the file to be stored in, one of 'png', 'jpeg', 'jpg', 'svg', 'gif' (case-insensitive)
    savepdf : bool
        To save in pdf
    orientation : str
        orientation of the network architecture, one of 'LR', 'TB', 'BT', 'RL' (case-insensitive)

    Attributes
    ----------
    orient_ : str
        Orientation of the Architecture
    layers_ : int
        Total number of layers in the architecture
    layer_names_ : list
        Layer names in the architecture
    layer_types_ : list
        Layer types of the architecture
    layer_units_ : list
        Number of units each layer of the network

    Methods
    -------
    add_layer()
        Add a layer to the network
    from_tensorflow()
        Make a network from the tensorflow model object
    get_meta_data()
        Return a dictionary containing the networks meta data
    summarize()
        Print a network summary in a MySQL Tabular format
    visualize()
        Render the network and open it with a suitable application

    Examples
    --------
    >>> from neuralnet_visualize import visualize as nnviz
    >>>
    >>> network = nnviz.visualizer()
    >>>
    >>> network.add_layer('dense', 7)
    >>> network.add_layer('dense', 12)
    >>> network.add_layer('dense', 4)
    >>>
    >>> network.visualize()
    """

    def __init__(self, title="My Neural Network", file_type='png', savepdf=False, orientation='LR'):
        self.title = title
        self.color_encoding = {'input': 'yellow', 'hidden': 'green', 'output': 'red', 'conv2d': 'pink'}
        self.possible_layers = ['dense', 'conv2d']
        self.possible_filetypes = ['png', 'jpeg', 'jpg', 'svg', 'gif']
        self.possible_orientations = ['LR', 'TB', 'BT', 'RL']

        if savepdf:
            self.file_type = 'pdf'
        else:
            if file_type.lower() not in self.possible_filetypes:
                raise NotAValidOption(file_type, self.possible_filetypes)
            self.file_type = file_type

        if orientation.upper() not in self.possible_orientations:
            raise NotAValidOption(orientation, self.possible_orientations)
        self.orient_ = orientation

        self.network = gv.Graph(title, directory='./graphs', format=self.file_type,
              graph_attr=dict(ranksep='2', rankdir=self.orient_, color='white', splines='line'),
              node_attr=dict(label='', nodesep='4', shape='circle', width='0.5'))

        self.layers_ = 0
        self.layer_names_ = list()
        self.layer_types_ = list()
        self.layer_units_ = list()
        self.tmp_units = list()
        self.from_tensorflow_called = False

    def __str__(self):
        return self.title

    def _update_meta_data(self, layer_type, nodes):
        # Update the meta data of the network

        if layer_type.lower() == 'dense':
            self.layer_units_.append(nodes)
        elif layer_type.lower() == 'conv2d':
            self.layer_units_.append(1)

        if self.layers_ == 0:
            layer_name = layer_type.capitalize()+'_input'
        else:
            layer_name = layer_type.capitalize()+'_hidden'+str(self.layers_)

        self.layer_names_.append(layer_name)
        self.layer_types_.append(layer_type)
        self.layers_ = self.layers_ + 1

        return layer_name

    def add_layer(self, layer_type, nodes=10, filters=32, kernel_size=3, padding='valid', stride=1):
        """Adds a layer to the network

        Parameters
        ----------
        layer_type : str
            Type of layer to add to the network (case-insensitive)
        nodes : int, default
            Number of units in the layer
        filters : int, default
            NUmber of 2D Convolution to be applied, only if layer_type == 'conv2d'
        kernel_size : int, tuple, list, default
            Size of the 2D Convolution window, an integer or tuple/list of 2 integers only if layer_type == 'conv2d'
        padding : str, default
            One of 'same' or 'valid' (case-insensitive), only if layer_type == 'conv2d'
        stride : int, tuple, list, default
            Stride of the Convolution window, an integer or tuple/list of 2 integers, only if layer_type == 'conv2d'

        Raises
        ------
        NotAValidOption
            When the layer_type is not implemented
        """

        if self.from_tensorflow_called:
            print("Network was already created from the tensorflow model object")
            return

        if layer_type not in self.possible_layers:
            raise NotAValidOption(layer_type, self.possible_layers)

        layer_name = self._update_meta_data(layer_type, nodes)

        if self.layer_types_[-1] == 'dense':
            with self.network.subgraph(name=f'cluster_{layer_name}') as layer:
                if nodes > 10:
                    layer.attr(labeljust='right', labelloc='bottom', label='+'+str(nodes - 10))
                    nodes = 10
                self.tmp_units.append(nodes)

                for i in range(nodes):
                    if self.layers_ == 1:
                        color = self.color_encoding['input']
                    else:
                        color = self.color_encoding['hidden']
                    layer.node(f'{layer_name}_{i}', shape='point', style='filled', fillcolor=color)
        elif self.layer_types_[-1] == 'conv2d':
            with self.network.subgraph(node_attr=dict(shape='box')) as layer:
                color = self.color_encoding['conv2d']

                if isinstance(kernel_size, Union[list, tuple].__args__):
                    ksstr = str(kernel_size[0])+"x"+str(kernel_size[0])
                else:
                    ksstr = str(kernel_size)+"x"+str(kernel_size)

                if isinstance(stride, Union[list, tuple].__args__):
                    sstr = str(tuple(stride))
                else:
                    sstr = str(stride)

                content = "Kernal Size: "+ksstr+"\nFilters: "+str(filters)+"\nPadding: "+str(padding).capitalize()+"\nStride: "+sstr
                layer.node(name=self.layer_names_[-1], label=content, height='1.5', width='1.5', style='filled', fillcolor=color)

        return

    def _connect_layers(self, l1_nodes, l2_nodes, l1_idx, l2_idx):
        # Connect all the nodes between the two layers

        for l1 in range(l1_nodes):
            for l2 in range(l2_nodes):
                if self.layer_types_[l1_idx] == 'dense' and self.layer_types_[l2_idx] == 'dense':
                    n1 = self.layer_names_[l1_idx]+'_'+str(l1)
                    n2 = self.layer_names_[l2_idx]+'_'+str(l2)
                elif self.layer_types_[l1_idx] == 'dense' and self.layer_types_[l2_idx] == 'conv2d':
                    n1 = self.layer_names_[l1_idx]+'_'+str(l1)
                    n2 = self.layer_names_[l2_idx]
                elif self.layer_types_[l1_idx] == 'conv2d' and self.layer_types_[l2_idx] == 'dense':
                    n1 = self.layer_names_[l1_idx]
                    n2 = self.layer_names_[l2_idx]+'_'+str(l2)
                elif self.layer_types_[l1_idx] == 'conv2d' and self.layer_types_[l2_idx] == 'conv2d':
                    n1 = self.layer_names_[l1_idx]
                    n2 = self.layer_names_[l2_idx]

                self.network.edge(n1, n2)

        return

    def _build_network(self):
        # Connect all the adjacent layers in the network

        for i in range(self.layers_ - 1):
            nodes1 = self.layer_units_[i]
            nodes2 = self.layer_units_[i+1]

            if self.layer_units_[i] > 10:
                nodes1 = 10
            if self.layer_units_[i+1] > 10:
                nodes2 = 10

            self._connect_layers(nodes1, nodes2, i, i+1)

        if self.layer_types_[-1] == 'dense':
            # Updating the color of output dense layer to red
            with self.network.subgraph(name=f'cluster_{self.layer_names_[-1]}') as layer:
                for i in range(self.tmp_units[-1]):
                    layer.node(f'{self.layer_names_[-1]}_{i}', style='filled', fillcolor='red')

        return

    def from_tensorflow(self, model):
        """Converts a given tensorflow model into graph

        Parameters
        ----------
        model : tensorflow.python.keras.engine.sequential.Sequential
            A tensorflow model
        """

        for layer in model.layers:
            if type(layer) == tf.keras.layers.Dense:
                self.add_layer('dense', nodes=layer.units)
            elif type(layer) == tf.keras.layers.Conv2D:
                self.add_layer('conv2d', kernel_size=layer.kernel_size)

        self.from_tensorflow_called = True

        return

    def get_meta_data(self):
        """Give a dictionary which contains meta data of the network.

        Returns
        -------
        meta_data : dict
            meta data which contains the details of all the layerss
        """

        meta_data = dict()
        meta_data['Number of Layers'] = self.layers_
        meta_data['Layer names'] = self.layer_names_
        meta_data['Layer Types'] = self.layer_types_
        meta_data['Node in Layers'] = self.layer_units_

        return meta_data

    def summarize(self):
        """Prints a summary of the network in MySQL tabular format
        """

        title = "Neural Network Architecture"
        hline = "+"+"-"*69+"+"

        print(hline)
        print("|"+title.center(69)+"|")
        print(hline)
        print("|"+"Layer Name".center(28)+"|"+"Layer Type".center(24)+"|"+"Layer Units".center(15)+"|")
        print(hline)
        for i in range(self.layers_):
            col1 = self.layer_names_[i].center(28)
            col2 = self.layer_types_[i].capitalize().center(24)
            col3 = str(self.layer_units_[i]).center(15)
            print("|"+col1+"|"+col2+"|"+col3+"|")
            print(hline)

        return

    def visualize(self):
        """Visualize the network
        """

        if self.layers_ < 2:
            print("Cannot draw Neural Network")
            print("Add atleast two layers to the network")
            return

        self._build_network()
        self.network.view()

        return

if __name__ == '__main__':
    input_nodes = 7
    hidden_nodes = 12
    output_nodes = 4

    net = visualizer()

    # net.add_layer('conv2d', kernel_size=5)
    # net.add_layer('dense', hidden_nodes)
    # net.add_layer('dense', output_nodes)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(filters=32, kernel_size=3, activation='sigmoid'),
        tf.keras.layers.Dense(128, activation='sigmoid'),
        tf.keras.layers.Dense(64, activation='sigmoid'),
        tf.keras.layers.Dense(32, activation='sigmoid'),
        tf.keras.layers.Dense(16, activation='sigmoid')
    ])

    net.from_tensorflow(model)
    net.add_layer('conv2d', 4)
    net.visualize()
    net.summarize()