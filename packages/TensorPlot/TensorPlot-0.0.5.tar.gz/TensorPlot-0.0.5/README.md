# TensorPlot
#### Easily plot keras models using nice style and formatting
author: Manu Blanco Valentin </br>
github: [manuelblancovalentin](http://github.com/manuelblancovalentin) </br>
version: v0.0.1


## What is this module intended for?
Tired of old-school boring default tensorflow/keras model architecture plots? Give this code a try! Nice, fresh, super-cool, colorful plots for your keras models (works with any wrapper also!).

This library was designed to help in the process of visualizing keras models graphs. It was expected to be as straightforward as possible.

## How to use?

First define your tf.keras model:

```python
import tensorflow as tf

input = tf.keras.layers.Input(shape=(100,100,1))
layer = tf.keras.layers.Conv2D(64,(3,3),activation='relu')(input)
layer = tf.keras.layers.Conv2D(128,(5,5),activation='relu')(layer)
layer = tf.keras.layers.Flatten()(layer)
layer = tf.keras.layers.Dense(128,activation='relu')(layer)
layer = tf.keras.layers.Dense(32,activation='relu')(layer)
layer = tf.keras.layers.Dense(1,activation='softmax')(layer)

model = tf.keras.Model(input,layer)
```

Now call the function to visualize the model (it does not require the model to be compiled nor trained, just created)

```python
import tensorplot as tp
tp.plot_model(model, filename = 'model.png')
```

This call will generate both a png and an svg image with a graph representing the model we just created. The <display_shapes> flag is used to toggle between displayinh or not the shape of the data through the layers of the net or not displaying them. In case the flag is set to True, the shape of the activations will be shown after any layer of the model that has the potential to effectively change the size of the data: convolutional, dense, pooling, flatten layers (activation, normalization, concatenate, merge, dropout layers are ignored). There is another flag that can be specified: <display_params>, which is by default set to False. When this flag is set to True some important parameters of different layers of the model are displayed along with the layer itself (such as the kernel size and strides of a Conv2D layer, or the pool_size of a Pool layer, the dropout rate in a dropout layer, etc.). 

The image below shows a comparison between the graph obtained using keras built in visualization utility ([see here](https://www.tensorflow.org/api_docs/python/tf/keras/utils/plot_model)) on the left, and the result using our function, on the right, for the model defined in the previous example:

<p align="center">
 <img src="./imgs/builtin_model.png">
 <img src="./imgs/my_model.png">
</p>

If the display_params flag was set to True in the previous example the result would look like:

<p align="center">
 <img src="./imgs/my_model_params.png">
</p>


## Supported layers
Almost every keras layer is supported (unsupported layers are: SimpleRNNCell, GRUCell nor LSTMCell -which are usually wrapped inside an RNN, SimpleRNN, GRU, LSTM or ConvLSTM2D layer-. Layer wrappers (such as TimeDistributed or Bidirectional) are not supported either). See further documentation on Keras layers on https://keras.io/layers . The render for each type of layer is shown below:

### Core layers
From top to bottom and left to right: Input, Flatten, Dense, Lambda, ActivityRegularization, Masking, Reshape, Permute and RepeatVector layers.
<p align="center">
 <img src="./imgs/core_layers.png">
</p>

### Convolutional layers
<p align="center">
 <img src="./imgs/conv_layers.png">
</p>

### Pooling layers
<p align="center">
 <img src="./imgs/pool_layers.png">
</p>

### Locally Connected Layers
<p align="center">
 <img src="./imgs/locally_layers.png">
</p>

### Activation layers 
Notice that these layers are created using the Activation layer and specifying the activation function rather than using specific advanced activation layers. This means that the ReLU layer shown below was obtained using ```tf.keras.layers.Activation('relu')``` instead of ```tf.keras.layers.ReLU```.
<p align="center">
 <img src="./imgs/activation_layers.png">
</p>

### Advanced Activation Layers
<p align="center">
 <img src="./imgs/advance_activation_layers.png">
</p>

### Normalization Layers
<p align="center">
 <img src="./imgs/norm_layers.png">
</p>

### Dropout layers
<p align="center">
 <img src="./imgs/dropout_layers.png">
</p>

### Recurrent layers
<p align="center">
 <img src="./imgs/recurrent_layers.png">
</p>

### Noise layers
<p align="center">
 <img src="./imgs/noise_layers.png">
</p>

### Embedding layers
<p align="center">
 <img src="./imgs/embedding_layers.png">
</p>

### Merge layers
<p align="center">
 <img src="./imgs/merge_layers.png">
</p>


## How to install?

To start using tensorplot simply install it via pip using the following command:

```bash
pip install TensorPlot
```

Extra documentation about the module can be found in our pypi page:

[https://pypi.org/project/TensorPlot/](https://pypi.org/project/TensorPlot/)


## Requirements

The modules required to use tensorplot are cited below:

```
setuptools~=46.4.0
numpy~=1.18.1
pydot>=1.4.1
```

## How to cite this work?

Please, if you found my work valuable and it was useful for you, consider citing it in any published work that used it to help me improve the visibility of my code and make it easier for other people to access it. 

If so, use the following bibtex entry in your paper:

```
@misc{MBValentin2020TensorPlot,
  author = {Valentin, Manuel Blanco},
  title = {Tensorplot},
  year = {2020},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/manuelblancovalentin/tensorplot}}
}
```
