# CMA-ES implementation here as a subclass of optimizer

import cma
import sys
from timeout import *

from random import randint
import rospy



class optimizer:

	_params_desc = {}
	_eval_callback = lambda _:None
	_timeout = 60

	# SIGMA = 0.005
	# SIGMA = 0.25
	SIGMA = 0.1

	_timeout_count = 0.

	INF = 100000000000


	def set_params_desc(self, desc):
		# update the configuration of the parameters e.g. min, max, default values.
		self._params_desc = desc
		pass

	def set_eval_callback(self, func):
		# set the objective value that the optimizer uses for evaluation
		self._eval_callback = func
		pass

	def set_params_config(self, config):
		for key, value in config.items():
			print key, value
			if key not in self._params_desc:
				self._params_desc[key] = {}
			self._params_desc[key]['default'] = value
		pass

	def __init__(self, desc, eval_callback, timeout = 60):
		# initializer
		# set the params configs and the objective function
		self.set_params_desc(desc)
		self.set_eval_callback(eval_callback)
		self.set_timeout(timeout)
		pass

	def set_timeout(self, timeout):
		self._timeout = timeout
		pass

	def optimize(self):
		default_values =  [ self.normalize(param_desc) for _, param_desc in self._params_desc.items() ]
		print default_values

		# do the normalization and interfacing
		# self.eval(default_values)
		# return self.eval(default_values)

		# res = cma.fmin(self.eval, default_values, self.SIGMA)

		es = cma.CMAEvolutionStrategy(default_values, self.SIGMA)

		while not es.stop():
			solutions = es.ask()
						
			
			costs = []

			for sol in solutions:

				rospy.loginfo("==============================" + \
							  "==============================" )
				rospy.loginfo("Iteration #%d: ", es.itereigenupdated)
				rospy.loginfo("______________________________" + \
							  "______________________________" )
				if es.best.evalsall:
					rospy.loginfo("\t# of samples: %d", es.best.evalsall )
				if es.best.x != None:
					rospy.loginfo("\tbest solution found = \n\t\t%s: ", 
									",\n\t\t".join([ str(key) + " : " + str(value) 
										for key, value in self.extract_config(es.best.x).items() ]))
					rospy.loginfo("\tbest objective value = \t%f: ", es.best.f )


				rospy.loginfo("______________________________" + \
							  "______________________________" )

				rospy.loginfo("running experiment for: \n\t %s", repr(list(sol)) )
				cost = self.eval(sol)
				rospy.loginfo("objective value = %f: \n", cost)
				costs.append(cost)

				rospy.loginfo("==============================" + \
							  "==============================" )

			es.tell(solutions, costs)
			es.disp()
		es.result_pretty()

		res = es.result()

		return res


	def extract_config(self, values):
		params = self._params_desc.keys()

		# print "keys are: {0}".format(params)

		config = {}
		for i in range(len(params)):
			param = params[i]
			desc = self._params_desc[param]
			config[param] = self.denormalize(values[i], desc["min"], desc["max"])			

		return config

	def normalize(self, param_desc):
		# default_values =  [ param_desc['default'] for _, param_desc in params_desc.items() ]
		value_range = param_desc['max'] - param_desc['min']
		value = (param_desc['default'] - param_desc['min']) / value_range
		return value

	def denormalize(self, value, vmin, vmax):
		value_range = vmax - vmin
		nvalue = value * value_range + vmin
		return nvalue

		

	def eval(self, values):

		print "raw values are: {0}".format(values)

		if any(val>1 or val<0 for val in values):
			obj_val = 0.
			for val in values:
				if val>1:
					obj_val += val-1
				elif val<0:
					obj_val += -val

			print("OUT OF BOUND")
			return self.INF * obj_val


		try:

			## 131 1441 0.00896432940323 0 0.234643642667 
			# values = [  0.00789639790315,
			# 			0.625585161861,
			# 			0.0292802172125,
			# 			0.452373387972,
			# 			0.034331367985,
			# 			0.269772560896,
			# 			0.0255957600625,
			# 			0.353741608684,
			# 			0.340681632899,
			# 			0.000624421036917,
			# 			0.00710255638588,
			# 			0.263852030857  ]

			# values = [0.0] * 12

			config = self.extract_config(values)
			print "extracted configs are: {0}".format(config)

			print "timeout is: {0}".format(self._timeout)			
			@timeout(self._timeout)
			def timeout_wrapper():
				return self._eval_callback(config)
			res = timeout_wrapper()
			
			print "result is: {0}".format(res)
			return res

		except TimeoutError:
			self._timeout_count += 1

			e = sys.exc_info()[0]

			print("experiment timeout. Error: %s" % e)
			print("returning infinity")

			if self._timeout_count >= 2:
				_timeout_count = 0
				## TODO: restart the simulation
				print "Seems something is wrong!! Do you want to continue?"
			# raise e
			return self.INF + randint(-50000, 50000)

		except: # TypeError: # catch *all* exceptions
			e = sys.exc_info()[0]
			import traceback
			traceback.print_exc()

			print("Something went wrong. Error: %s" % e)		
			print("returning infinity")
			# raise e
			return self.INF + randint(-50000, 50000)
