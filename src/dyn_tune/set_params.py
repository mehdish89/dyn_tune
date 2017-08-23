#!/usr/bin/env python

import sys
import rospy
from gazebo_msgs.srv import *

from ddynamic_reconfigure_python.ddynamic_reconfigure import DDynamicReconfigure

def get_services():
	rospy.wait_for_service('/gazebo/advertise_joint_params')

	try:
		advertise_params = rospy.ServiceProxy('/gazebo/advertise_joint_params', ParamListRequest)
		res = advertise_params()
		return res.params
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e


def set_param(service_name, value):
	rospy.wait_for_service("gazebo/" + service_name)
	try:
		set_param_ = rospy.ServiceProxy("gazebo/" + service_name, SetParamFloat)
		res = set_param_(value)
		return res.success
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e

def set_params(value):
	services = get_services()
	for service_name in services:
		set_param(service_name, value)

def dyn_rec_callback(config, level, param_ns):
	# print(config)
	# print(level)
	# print(param_ns)

	for key in config:
		if key == "groups":
			continue
		# service_name = key.replace("___", "/")
		service_name = ''.join([param_ns,"/", key])
		print service_name, key, config[key]
		set_param(service_name, config[key])

	# rospy.loginfo("Received reconf call: " + str(config))
	return config

if __name__ == '__main__':
	rospy.init_node('ddynrec')

	print("init ok")

	# Create a D(ynamic)DynamicReconfigure
	# ddynrec = DDynamicReconfigure("/kosekhar/kosegav")

	# print("ddyn ok")

	ddyns = {}

	services = get_services()

	services = rospy.get_param("/optimizable_params")

	# print services

	# exit()

	print services

	for service_name in services:

		# service_name = ''.join(["/", service_name])

		index = service_name.rfind("/")
		param_ns =  service_name[:index]
		param_name = service_name[index+1:]



		# param_name = service_name.replace("/", "___")

		if param_ns not in ddyns:
			ddyns[param_ns] = DDynamicReconfigure(param_ns)

		ddynrec = ddyns[param_ns]

		ddynrec.add_variable(param_name, service_name, 0.0, 0.0, 10.0)	

	# fs = {}

	for param_ns in ddyns:
		def _dyn_rec_callback(config, level, _param_ns = param_ns):
			return dyn_rec_callback(config, level, _param_ns)
		
		# fs[param_ns] = _dyn_rec_callback

		ddynrec = ddyns[param_ns]
		ddynrec.start(_dyn_rec_callback)


	# print "start printing"
	# for _, f in fs.items():
	# 	f("", "")

	# print ddyns

	# Add variables (name, description, default value, min, max, edit_method)
	# ddynrec.add_variable("decimal", "float/double variable", 0.0, -1.0, 1.0)
	# ddynrec.add_variable("integer", "integer variable", 0., -1., 1.)
	# ddynrec.add_variable("bool", "bool variable", True)
	# ddynrec.add_variable("string", "string variable", "string dynamic variable")
	# enum_method = ddynrec.enum([ ddynrec.const("Small",      "int", 0, "A small constant"),
	#                    ddynrec.const("Medium",     "int", 1, "A medium constant"),
	#                    ddynrec.const("Large",      "int", 2, "A large constant"),
	#                    ddynrec.const("ExtraLarge", "int", 3, "An extra large constant")],
	#                  "An enum example")
	# ddynrec.add_variable("enumerate", "enumerate variable", 1, 0, 3, edit_method=enum_method)

	# Start the server


	rospy.spin()