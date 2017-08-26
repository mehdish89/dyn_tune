#! /usr/bin/env python

from function import *

def save(arg):
	if type(arg) is str:
		print arg
		def wrapper(func):
			func.__name__ = arg
			func.save(func.get_name())
			return func
		return wrapper
	else:
		func = arg
		func.save(func.get_name())
		return func



SIGNED = [ 	"int64",
			"uint64",
			"uint32",
			"int32",
			"uint",
			"ulong",
			"int",
			"long",
			"float",
			"float32",
			"float64" ]

SIGNED_ARRAY = ["int64[]",
				"uint64[]",
				"uint32[]",
				"int32[]",
				"uint[]",
				"ulong[]",
				"int[]",
				"long[]",
				"float[]",
				"float32[]",
				"float64[]" ]


UNSIGNED = [ 	
				"int64",
				"int32",
				"int",
				"long",
				"float",
				"float32",
				"float64" ]

UNSIGNED_ARRAY = ["int64[]",
				"int32[]",
				"int[]",
				"long[]",
				"float[]",
				"float32[]",
				"float64[]" ]


CALLABLE = ["function", "builtin_function_or_method", "builtin_function", "type"]



@save 
@accept('duration', [], [['Time','time'], 'duration'], 'duration', [])
@accept([['Time','time'], 'duration'], 'duration', [])
@accept('duration', [], [['Time','time'], 'duration'])
@accept([SIGNED, SIGNED_ARRAY], [SIGNED, SIGNED_ARRAY], [])
@Resolver
def ADD(*nums):
	sum_all = None
	for num in nums:
		if sum_all != None:
			sum_all = sum_all + num
		else:
			sum_all = num

	return sum_all

@save
@accept([SIGNED, SIGNED_ARRAY], [SIGNED, SIGNED_ARRAY], [])
@Resolver
def MULT(*nums):
	mult_all = None
	for num in nums:
		if mult_all != None:
			mult_all = mult_all * num
		else:
			mult_all = num

	return mult_all

@save
@accept(['Time','time'], ['Time','time'], [])
@accept([SIGNED, SIGNED_ARRAY], [SIGNED, SIGNED_ARRAY])
@Resolver
def SUB(a, b):
	return a-b


@save
@accept([UNSIGNED, UNSIGNED_ARRAY])
@Resolver
def NEG(x):
	return -x


@save
@accept([CALLABLE])
@accept([CALLABLE], "*", [])
@Resolver
def CALL(func, *args, **kwargs):

	def CALL(func, *args, **kwargs):
		print "calling {0} with {1} and {2}".format(func, args, kwargs)

		if len(args)>0 and type(args[0]).__name__ in ["function", "builtin_function_or_method", "builtin_function", "type"]:
			args = CALL(args[0], *args[1:], **kwargs)
			if type(args) is not tuple:
				args = [args]
		return func(*args, **kwargs)

	return CALL(func, *args, **kwargs)


@save 
@accept([SIGNED, SIGNED_ARRAY], [])
@Resolver
def MEAN(*nums):
	if len(nums)==1:
		nums = nums[0]

	sum_all = None
	for num in nums:
		if sum_all != None:
			sum_all = sum_all + num
		else:
			sum_all = num

	return sum_all/len(nums)


@save
@accept([SIGNED, SIGNED_ARRAY])
@Resolver
def ABS(x):
	return abs(x)

@save
@accept([SIGNED, SIGNED_ARRAY])
@Resolver
def SUM(x):
	return sum(x)


