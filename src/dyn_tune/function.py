import dill
import os
import errno
import rospkg
import copy



rospack = rospkg.RosPack()

class Resolver(object):
	
	# types = []

	def validate_rule(self, arg_types, arg_rule):

		# print "validating ", arg_types, " agianst ", arg_rule

		def is_valid(type_src, type_dst):
			return ( type_src == type_dst or type_dst == "*" or
						( type(type_src) == str and type(type_dst) == str and type_src.lower() == type_dst.lower() ) or
						( hasattr(type_dst,'__iter__') and 
							(type_src in type_dst or 
							any( is_valid(type_src, atype) for atype in type_dst ))) )

		index_1 = 0
		index_2 = 0

		while index_1 < len(arg_types):

			if index_2 >= len(arg_rule):
				return False

			type_src = arg_types[index_1]
			type_dst = arg_rule[index_2]

			if not type_dst:
				if index_2>0 and is_valid(type_src, arg_rule[index_2-1]):
					index_1 += 1
					continue
				else:
					index_2 += 1
					continue

			elif is_valid(type_src, type_dst):
				index_1 += 1
				index_2 += 1
			else:
				return False

		if index_2 < len(arg_rule) and arg_rule[index_2]:
			return False

		return True


	def validate(self, arg_types):

		for rule in self.types:
			if self.validate_rule(arg_types, rule):
				return True

		return False



	def __init__(self, func):
		self.func = func
		self.__name__ = func.__name__
		self.types = []

	def get_name(self):
		return self.func.__name__

	def __call__(self, *args, **kwargs):
		# print('Called {func} with args: {args} and keyword args: {kwargs}'.format(func="func", 
		# 																			kwargs = kwargs,
		# 																			args=args))

		rargs = []
		for arg in args:
			if arg not in kwargs:
				raise KeyError('Cannot resolve the argument \'{arg}\''.format(arg = arg))
			rargs.append(copy.copy(kwargs.get(arg)))

		# print "Resolved ARGS are: ", rargs

		return self.func(*rargs)

	def serialize(self):
		return dill.dumps(self)

	def save(self, name, path = rospack.get_path('dyn_tune')+"/functions/default"):

		filename = '/'.join([path, name])

		if not os.path.exists(os.path.dirname(filename)):
			try:
				os.makedirs(os.path.dirname(filename))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise
		
		file = open(filename, 'w')

		code = self.serialize()
		file.write(code)



def accept(*args):
	def decorator(func):
		func.types.append(args)
		return func
	return decorator

import random
import string

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

class Function():
	def __init__(self, tasks = [], retvar = '_', types = [], name = None):
		self.tasks = tasks
		self.retvar = retvar
		self.types = types

		if name == None:
			self.__name__ = "USER_FUNC_" + id_generator()


	def __call__(self, *args, **values):

		locals_0 = locals().copy()

		current = {}
		current.update(values)

		for i in range(len(args)):
			current.update({'args[{0}]'.format(i):current[args[i]]})


		for func, args, retvar, has_script, script in self.tasks:					
			if func != None:
				current.update({retvar: func(*args, **current)})	
			if has_script:
				exec(script, current, current)

		return current.get(self.retvar)

	def add_task(self, func, args, retvar, index = None):

		if index is None:
			index = len(self.tasks)

		self.tasks.insert(index, (func, args, retvar))

	def delete_task(index):
		del self.tasks[index]

	def serialize(self):
		return dill.dumps(self)

	def save(self, name, path = rospack.get_path('dyn_tune')+"/functions/user"):

		filename = '/'.join([path, name])

		if not os.path.exists(os.path.dirname(filename)):
			try:
				os.makedirs(os.path.dirname(filename))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise
		
		file = open(filename, 'w')

		code = self.serialize()
		file.write(code)

	# @staticmethod
	# def load(filename):
	# 	file = open(filename, 'r')
	# 	code = self.serialize()



	def validate(self, arg_types):
		return arg_types in self.types

from os import listdir
from os.path import isfile, join

def load_functions(path = rospack.get_path('dyn_tune')+'/functions/default'):
	func_dict = {}

	for name in listdir(path):
		filename = join(path, name)
		
		if isfile(filename):
			file = open(filename, 'r')
			code = file.read()
			func = dill.loads(code)
			func_dict.update({func.__name__: func})

	return func_dict





# @accept("int[]","int[]")
# @accept("float[]","float[]")
# @accept("int", "int")
# @accept("float", "float")
# @Resolver
# def ADD(a, b):
# 	return a+b

# @accept("int[]","int[]")
# @accept("float[]","float[]")
# @accept("int", "int")
# @accept("float", "float")
# @Resolver
# def MULT(a, b):
# 	return a*b

# @accept("int[]","int[]")
# @accept("float[]","float[]")
# @accept("int", "int")
# @accept("float", "float")
# @Resolver
# def SUB(a, b):
# 	return a-b

# print ADD.types
# print ADD.validate(("float", "float"))
# print ADD.validate(("float[]", "float[]"))
# print ADD.validate((int, int))
# print ADD.validate((float, float, float))

# abs = Resolver(abs)

# func = Function()
# func.add_task(ADD, ['args[0]','args[1]'], 'abs_val')
# func.add_task(abs, ['abs_val'], 'ret_val')
# func.retvar = 'ret_val'
# print func('a','b','c','d', a=10, b=-12, c=33, d=55)
# print func('a','b', a=43, b=64)


