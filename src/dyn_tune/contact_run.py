from timeout import timeout
import rospy
import matplotlib.pyplot as plt
rospy.init_node('tester')



# def f(t):
# 	# @timeout(t)
# 	def h():
# 		rospy.sleep(20)
# 	h()

# f(1)

def plot_dual(config):
	plt.clf()
	data_sim = config['/simulation/joint_states/position']
	data_real = config['/real/joint_states/position']
	plot(data_sim)
	plot(data_real)
	plt.draw()
	plt.show()


def plot(data, style = '-'):

	print "single plot %d" % data.shape[1]

	plt.ion()

	for i in range(data.shape[1]):
		col = data[:, i]
		plt.subplot(3, 2, i+1)
		print "plottting data %d" % i
		print col
		
		plt.plot(col, ls = style)#, hold=True)
		# plt.ylabel(key)
		plt.xlabel('time')

		plt.pause(0.05)

def error(x, y, axis = 0):
	mserr = ((x - y) ** 2).mean(axis=axis)
	# print(mserr)
	mserr = sum(mserr)
	return mserr


def shift(x, y, i):
	if i>=0:
		x_new = x[i:]
		y_new = y[:len(y)-i]
	else:
		x_new = x[0:len(x)+i]
		y_new = y[-i:]
	return x_new, y_new


def find_best_error(x, y, offset, axis = 0):
	min_err = float("inf")
	min_index = 0
	for i in range(-offset, offset+1):
		x_new, y_new = shift(x, y, i)		
		# print "################"
		# print len(x_new)
		# print len(y_new)
		
		err = error(x_new, y_new, axis)
		print err, i
		if err < min_err:
			min_err = err
			min_index = i
	
	print min_err, min_index

	return min_err, min_index


def f(config, axis = 0):

	return 0.
	
	print "the config is:"
	print(config)
	sim_pos = config['/simulation/joint_states/position']
	# sim_pos[:,[2,1,0,3,4,5]] = sim_pos[:,[0,1,2,3,4,5]]
	

	real_pos = config['/real/joint_states/position']

	sim_pos = sim_pos[:,[1,3,4,5,6,8]]
	real_pos = real_pos[:,[1,3,4,5,6,8]]

	mserr, offset = find_best_error(sim_pos, real_pos, len(sim_pos)/4)

	sim_pos, real_pos = shift(sim_pos, real_pos, offset)

	config['/simulation/joint_states/position'] = sim_pos
	config['/real/joint_states/position'] = real_pos

	print "before plot"

	# plot(sim_pos)
	# plot(real_pos)
	# plt.draw()
	# plt.show()


	plot_dual(config)

	print "after plot"

	# rospy.sleep(50)

	# mserr = ((sim_pos - real_pos) ** 2).mean(axis=axis)
	# mserr = sum(mserr)
	print(mserr)
	return mserr


from dynamic_tuner import *
# params = rospy.get_param("/optimizable_params")
# values = rospy.get_param("/objective_values")

values = [
			'/simulation/sensor_states/contact[10]',
			'/simulation/sensor_states/contact[6]',
			'/simulation/sensor_states/contact[1]',
			'/simulation/sensor_states/contact[8]',

			'/real/sensor_states/contact[3]',
			'/real/sensor_states/contact[2]',
			'/real/sensor_states/contact[4]',
			'/real/sensor_states/contact[0]',
			'/real/sensor_states/contact[1]',

			'/simulation/sensor_states',
			'/real/sensor_states',
			
			'/real/commands',
			
			'/simulation/haptix_deka_controller/command',
			'/real/haptix_deka_controller/command'
		]

print "###"
# print params

# print params, values 

src_topic = '/haptix_deka_controller/command'
dst_topic = '/haptix_deka_controller/command'

# src_bag = 'exp-rand-01.bag'
src_bag = 'exp-contacts.bag'
dst_bag = 'test_sim.bag'

# start = {'/haptix_deka_controller/follow_joint_trajectory/status/status_list[0]/status':1, '/haptix_deka_controller/follow_joint_trajectory/feedback/status/status':1}
# end = {'/haptix_deka_controller/follow_joint_trajectory/result':None, '/haptix_deka_controller/follow_joint_trajectory/result':None}

start = {}
end = {}

print "ready to start"

# dyn = dynamic_tuner(params, values, src_bag, dst_bag, src_topic, dst_topic, objective = f, start_signal = start, end_signal = end)


print "starting..."
# dyn.tune_params()


bag = start_simulation(src_bag, dst_bag, src_topic, dst_topic, values = values)

"""
from dynamic_tuner import *
start_simulation('exp-real-7.bag', 'test_sim.bag', '/follow_joint_trajectory/goal', '/arm_controller/follow_joint_trajectory/goal', {'/follow_joint_trajectory/goal':None, '/arm_controller/follow_joint_trajectory/goal':None}, {'/arm_controller/follow_joint_trajectory/result':None, '/follow_joint_trajectory/result':None})


from dynamic_tuner import *
start_simulation('exp-real-7.bag', 'test_sim.bag', '/follow_joint_trajectory/goal', '/arm_controller/follow_joint_trajectory/goal', {'/follow_joint_trajectory/status/status_list[0]/status':1, '/arm_controller/follow_joint_trajectory/feedback/status/status':1}, {'/arm_controller/follow_joint_trajectory/result':None, '/follow_joint_trajectory/result':None})



sim_bag = rosbag.Bag('test_sim.bag', 'r')
bag = restamp(sim_bag, output_bag_file = 'sim-restamped.bag', prefix = SIM_PREFIX, start_signal = start_signal, end_signal = end_signal)


dyn._optimizer.optimize()

dyn._optimizer.set_params_config({'/arm_controller/gains/elbow_joint/p':100001})
desc = dyn.get_params_desc(['/arm_controller/gains/elbow_joint/p', '/arm_controller/gains/elbow_joint/i', '/arm_controller/gains/wrist_3_joint/d'])
"""