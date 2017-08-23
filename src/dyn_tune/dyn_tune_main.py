#! /usr/bin/env python

import rospy
import dynamic_tuner
import function
import dyn_tune.srv
import dyn_tune.msg
import json




def bypasser(func):
	def wrapper(config):
		return func(**config)
	wrapper.tasks = func.tasks
	return wrapper

dyn_tuner = None


# TODO: need to double check things. just implemented
def optimize_callback(req):

	# rospy.loginfo("I heard %s",req)
	global dyn_tuner

	if dyn_tuner != None:
		return False

	values = req.observation_values
	start = json.loads(req.start_signals)
	end = json.loads(req.end_signals)

	params = json.loads(req.experiments[0].parameters)
	func = req.experiments[0].objective

	funcs = function.load_functions()

	tasks = [ (funcs[task.function], task.args, task.return_var, task.has_script, task.script) if not task.has_script
				else (None, [], None, task.has_script, task.script)
				for task in func.tasks ]

	obj_func = function.Function(tasks = tasks,
						retvar = func.return_var,
						types = func.arg_types )

	obj_func = bypasser(obj_func)

	# src_topic = req.src_topic
	# dst_topic = req.dst_topic

	src_topic = "/haptix_deka_controller/command"
	dst_topic = "/haptix_deka_controller/command"

	src_bag = req.src_bag
	dst_bag = req.dst_bag

	

	dyn_tuner = dynamic_tuner.dynamic_tuner(params, 
						values, 
						src_bag, 
						dst_bag, 
						src_topic, 
						dst_topic, 
						objective = obj_func, 
						start_signal = start, 
						end_signal = end )


	# # TODO: ROSLOG
	# print "starting..."
	# dyn.tune_params()

	return True

def list_functions_callback(req):
	# rospy.loginfo("I heard %s",req)

	funcs = { name: func for name, func  in function.load_functions().items() 
				if not req.args or func.validate(tuple(req.args)) }

	return {'functions': map(str, funcs) }

def save_function_callback(req):
	rospy.loginfo("I heard %s",req)
	return True
	
def main():
	rospy.init_node('dyn_tune_backbone')

	# tuner = dynamic_tuner.dynamic_tuner()

	opt_srv = rospy.Service('optimize', dyn_tune.srv.Optimize, optimize_callback)
	list_srv = rospy.Service('list_available_functions', dyn_tune.srv.ListAvailableFunctions, list_functions_callback)
	save_srv = rospy.Service('create_function', dyn_tune.srv.CreateUserFunction, save_function_callback)

	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		global dyn_tuner

		if dyn_tuner != None:
			dyn_tuner.tune_params()
			print dyn_tuner._src_topic
			print dyn_tuner._dst_topic
			print dyn_tuner._real_bag_file
			print dyn_tuner._sim_bag_file
			print dyn_tuner._objective
			print dyn_tuner._objective.tasks
			print dyn_tuner._params_desc

			dyn_tuner = None

		rate.sleep()


if __name__ == '__main__':
	main()