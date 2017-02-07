import numpy as np
import tensorflow as tf
import pandas as pd
import timeit







#### code for Genetic Tensor Decomposition (GTD), with Stochastic Gradient Descent (SGD) algorithm
#### pick individual wiht all his/her samples (of all tissues), with probability propotional to pool size (for this indiv)
#### we output the xxx







##==================================================================================================================
##
T = np.load("./data_simu_gtd/T.npy")
U = np.load("./data_simu_gtd/U.npy")
V = np.load("./data_simu_gtd/V.npy")
##
Beta = np.load("./data_simu_gtd/Beta.npy")
##
Y = np.load("./data_simu_gtd/Y.npy")
Y_spread = np.load("./data_simu_gtd/Y_spread.npy")					## this for now is a full tensor
X = np.load("./data_simu_gtd/X.npy")
##
table_index_indiv = np.load("./data_simu_gtd/table_index_indiv.npy")
pool_index_indiv = {}
for i in range(len(table_index_indiv)):
	pool_index_indiv[i] = table_index_indiv[i]
list_index_all = np.load("./data_simu_gtd/list_index_train.npy")


## for categorical draw:
list_p = np.load("./data_simu_gtd/list_p_indiv.npy")



##
dimension1 = len(T)
dimension2 = len(U)
dimension3 = len(V)
feature_len = len(T[0])










with tf.device("/cpu:0"):




	#### the genetic component
	placeholder_index_x = tf.placeholder(tf.int32)
	x = tf.placeholder(tf.float32, shape=(None, len(X[0])))							## genotype
	place_beta = tf.placeholder(tf.float32, shape=(len(Beta), len(Beta[0])))
	beta = tf.Variable(place_beta)
	u_ = tf.matmul(x, beta)


	#### the tensor product
	## for T, we have the extra dimension for broadcasting the multiply op
	'''
	T = tf.Variable(initial_value=tf.truncated_normal([dimension1, 1, feature_len]), name='tissues')
	U = tf.Variable(initial_value=tf.truncated_normal([dimension2, feature_len]), name='indivs')
	V = tf.Variable(initial_value=tf.truncated_normal([dimension3, feature_len]), name='genes')
	'''
	#### initialize the three with pre-loaded fm
	T = tf.Variable(initial_value=T, dtype=tf.float32, name='tissues')
	U = tf.Variable(initial_value=U, dtype=tf.float32, name='indivs')
	V = tf.Variable(initial_value=V, dtype=tf.float32, name='genes')
	T = tf.expand_dims(T, 1)



	TUD = tf.mul(T, U, name=None)					## dimension1 x dimension2 x feature_len
	result = tf.einsum('kid,jd->kij', TUD, V)		## dimension1 x dimension2 x dimension3
	result_flatten = tf.reshape(result, [-1])

	# expected Y (inside Gene Tensor)
	placeholder_index_y = tf.placeholder(tf.int32)
	y_ = tf.gather(result_flatten, placeholder_index_y)

	# real Y
	y = tf.placeholder(tf.float32)


	####
	#### SO: to fill in this batch the following feed dic:
	####	placeholder_index_x (to make it a list, to make it general to multiple individuals)
	####	x
	####	placeholder_index_y
	####	y
	####




	##==================================================================================================================
	## cost function
	base_cost = tf.reduce_sum(tf.square(tf.sub(y_, y)))


	## the prior for U --> genetic cost
	U_sub = tf.gather(U, placeholder_index_x)
	U_cost = tf.reduce_sum(tf.square(tf.sub(u_, U_sub)))


	## the prior for V and T --> regularization (for V and T)
	lda_VT = tf.constant(.001)
	norm_sums = tf.add(tf.reduce_sum(tf.abs(T)),
	                   tf.reduce_sum(tf.abs(V)))
	regularizer_VT = tf.mul(norm_sums, lda_VT)


	## regularization (for Beta)
	lda_beta = tf.constant(.001)
	norm_sums_beta = tf.reduce_sum(tf.abs(beta))
	regularizer_beta = tf.mul(norm_sums_beta, lda_beta)


	## total train cost
	cost_train = tf.add(base_cost, U_cost)
	cost_train = tf.add(cost_train, regularizer_VT)
	cost_train = tf.add(cost_train, regularizer_beta)


	## learning rate
	lr = tf.constant(0.000001, name='learning_rate')
	global_step = tf.Variable(0, trainable=False)
	learning_rate = tf.train.exponential_decay(lr, global_step, 10000, 0.96, staircase=True)


	## learn!!!
	optimizer = tf.train.GradientDescentOptimizer(learning_rate)
	training_step = optimizer.minimize(cost_train, global_step=global_step)







	##==================================================================================================================
	# execute
	init = tf.initialize_all_variables()
	sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
	#sess = tf.Session()
	#sess.run(init)
	sess.run(init, feed_dict={place_beta: Beta})


	##==== timer
	start_time = timeit.default_timer()
	for i in xrange(1000):


		#### sample individuals based on tissues avaliable for that individual (unbiased sampling for loss function)
		list_temp = np.random.multinomial(1, list_p)
		index = np.argmax(list_temp)
		list_index_x = [index]
		# pick up sample indices (in the spread version of Y) for that individual
		list_index_y = pool_index_indiv[index]
		# call run and feed in data
		sess.run(training_step, feed_dict={placeholder_index_x: list_index_x, x: [X[index]], placeholder_index_y: list_index_y, y: Y_spread[list_index_y]})

		####
		## training error
		N = len(X)
		list_index_x = np.arange(N)
		print sess.run(cost_train, feed_dict={placeholder_index_x: list_index_x, x: X, placeholder_index_y: list_index_all, y: Y_spread[list_index_all]})

	##==== timer
	elapsed = timeit.default_timer() - start_time
	print "time spent:", elapsed

















