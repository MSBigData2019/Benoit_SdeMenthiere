
from PIL import Image
import tensorflow as tf
import numpy as np
import Layers


LoadModel = True

nb_block = 4
nb_conv_per_block = 2
nbfilter = 16
KeepProb_Dropout = 1.0
decay = 0.9
bs = 256
dsize = 100

f = open("chuck48.raw", 'rb')
ima = np.empty([1, 2304], dtype=np.float32)
ima[0,:] = np.fromfile(f, dtype=np.uint8, count=2304)
adversarial_label = np.array([0.0,1.0]);
f.close()

with tf.name_scope('input'):
	DXinit = tf.constant(0.0, shape=[1,2304])
	DX = tf.Variable(DXinit)
	x = tf.placeholder(tf.float32, [None, 2304],name='x')
	y_desired = tf.placeholder(tf.float32, [None, 2],name='y_desired')
	ITM = tf.placeholder("bool", name='Is_Training_Mode')

with tf.name_scope('CNN'):
	t = Layers.unflat(x+DX,48,48,1)
	
	for k in range(nb_block):
		for i in range(nb_conv_per_block):
			d = Layers.conv(t,nbfilter,3,1,ITM,'conv33_%d_%d'%(k,i),KeepProb_Dropout)
			t = tf.concat([t,d],axis=3)
		t = Layers.maxpool(t,2,'pool')
		t = Layers.conv(t,32,1,1,ITM,'conv11_%d_%d'%(k,i),KeepProb_Dropout)
	
	t = Layers.conv(t,50,3,1,ITM,'conv_finale1',KeepProb_Dropout,pad='VALID')
	out = Layers.conv(t,2,1,1,ITM,'conv_finale2',act=tf.identity)
	
	y = Layers.flat(tf.nn.log_softmax(out))
	out = Layers.flat(out)
	
with tf.name_scope('cross_entropy'):
	diff = y_desired * y 
	with tf.name_scope('total'):
		cross_entropy = -tf.reduce_mean(diff)	

with tf.name_scope('regul'):
	L2 = tf.reduce_mean(tf.square(DX)) 
	L1 = tf.reduce_mean(tf.abs(DX))
	Linf = tf.reduce_max(tf.abs(DX))	
		
with tf.name_scope('learning_rate'):
	global_step = tf.Variable(0, trainable=False)
	learning_rate = tf.train.exponential_decay(1e-2,global_step,1000, decay, staircase=True)

# cost = 	cross_entropy + 0.1*L2
cost = 	cross_entropy + L1
# cost = 	cross_entropy 
train_step = tf.train.AdamOptimizer(learning_rate).minimize(cost,global_step=global_step)

print ("-----------------------------------------------------")
print ("-----------------------------------------------------")

sess = tf.Session()	
sess.run(tf.global_variables_initializer())
collec=tf.get_collection("mes parametres")
saver = tf.train.Saver(collec)
if LoadModel:
	saver.restore(sess, "./model_dens.ckpt")

nbIt = 2000
for it in range(nbIt):
	if it%10 == 0:
		label,output,normL1,normL2,maxDX = sess.run([tf.argmax(out, 1),out,L1,L2,Linf],{x:ima})
		print ("%4d label %d output %.4f %.4f  L1= %.3f  L2= %.3f  max= %.3f"%(it,label,output[0,0],output[0,1],normL1,normL2,maxDX))
		if label==1:
			break
	sess.run(train_step, {x:ima,y_desired:[adversarial_label]})	
	
for it in range(20):
	sess.run(train_step, {x:ima,y_desired:[adversarial_label]})	

			
mod_image,residual,residual50 = sess.run([x+DX,DX,DX*50],{x:ima})

toshow = np.reshape(ima,(48,48))
im2 = Image.fromarray(toshow)
im2.show()

toshow = np.reshape(mod_image,(48,48))
im2 = Image.fromarray(toshow)
im2.show()

toshow = np.reshape(residual,(48,48))
im2 = Image.fromarray(toshow)
im2.show()

toshow = np.reshape(residual50,(48,48))
im2 = Image.fromarray(toshow)
im2.show()

f = open("mod_chuck.raw", 'wb')
mod_image.astype(dtype=np.uint8).tofile(f)
f.close()

sess.close()
