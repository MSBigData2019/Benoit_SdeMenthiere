from PIL import Image
import tensorflow as tf
import numpy as np
import Layers
import sys

LoadModel = True

nb_conv_per_block = 2
nbfilter = 16
KeepProb_Dropout = 1.0

image_name = sys.argv[1]

f = open(image_name, 'rb')
ima = np.empty([1, 2304], dtype=np.float32)
ima[0,:] = np.fromfile(f, dtype=np.uint8, count=2304)
f.close()

with tf.name_scope('input'):
	x = tf.placeholder(tf.float32, [None, 2304],name='x')
	# y_desired = tf.placeholder(tf.float32, [None, 2],name='y_desired')
	ITM = tf.placeholder("bool", name='Is_Training_Mode')

with tf.name_scope('CNN'):
	t = Layers.unflat(x,48,48,1)
	
	for k in range(4):
		for i in range(nb_conv_per_block):
			d = Layers.conv(t,nbfilter,3,1,ITM,'conv33_%d_%d'%(k,i),KeepProb_Dropout)
			t = tf.concat([t,d],axis=3)
		t = Layers.maxpool(t,2,'pool')
		t = Layers.conv(t,32,1,1,ITM,'conv11_%d_%d'%(k,i),KeepProb_Dropout)
	
	t = Layers.conv(t,50,3,1,ITM,'conv_finale1',KeepProb_Dropout,pad='VALID')
	t = Layers.conv(t,2,1,1,ITM,'conv_finale2',act=tf.identity)
	out = Layers.flat(t)

print ("-----------------------------------------------------")
print ("-----------------------------------------------------")

sess = tf.Session()	
sess.run(tf.global_variables_initializer())
# collec=tf.get_collection("mes parametres")
saver = tf.train.Saver()
if LoadModel:
	saver.restore(sess, "./model_dens.ckpt")

			
label,output = sess.run([tf.argmax(out, 1),out],{x:ima})
print ("label %d output %.4f %.4f "%(label,output[0,0],output[0,1]))
if label == 0:
	print ("homme")
else :
	print ("femme")

# toshow = np.reshape(ima,(48,48))
# im2 = Image.fromarray(toshow)
# im2.show()

sess.close()
