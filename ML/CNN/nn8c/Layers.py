

import tensorflow as tf
import numpy as np


def conv(tensor, outDim, filterSize, stride, IsTrainingMode, name,KP_dropout=1.0, act=tf.nn.relu,pad='SAME'):
	with tf.name_scope(name):
		inDimH = tensor.get_shape()[1].value
		inDimW = tensor.get_shape()[2].value
		inDimD = tensor.get_shape()[3].value
		Winit = tf.truncated_normal([filterSize, filterSize, inDimD, outDim], stddev=np.sqrt(2.0/(inDimH*inDimW*inDimD)))
		W = tf.Variable(Winit,trainable=False)
		tf.add_to_collection("mes parametres",W)
		tensor = tf.nn.conv2d(tensor, W, strides=[1, stride, stride, 1], padding=pad)

		Binit = tf.constant(0.0, shape=[outDim])
		B = tf.Variable(Binit,trainable=False)
		tf.add_to_collection("mes parametres",B)
		tensor += B
		
		tensor = act(tensor)
		if KP_dropout != 1.0:
			tensor = tf.cond(IsTrainingMode,lambda: tf.nn.dropout(tensor, KP_dropout), lambda: tf.identity(tensor))	

	return tensor

		
def maxpool(tensor, poolSize, name):
	with tf.name_scope(name):
		tensor = tf.nn.max_pool(tensor, ksize=(1,poolSize,poolSize,1), strides=(1,poolSize,poolSize,1), padding='SAME')
	return tensor
	
def flat(tensor):
	inDimH = tensor.get_shape()[1].value
	inDimW = tensor.get_shape()[2].value
	inDimD = tensor.get_shape()[3].value
	tensor = tf.reshape(tensor, [-1, inDimH * inDimW * inDimD])
	# print ('flat output  ',tensor)
	return tensor

def unflat(tensor, outDimH,outDimW,outDimD):
	tensor = tf.reshape(tensor, [-1,outDimH,outDimW,outDimD])
	# tf.summary.image('input', tensor, 10)
	# print ('unflat output  ',tensor)
	return tensor	