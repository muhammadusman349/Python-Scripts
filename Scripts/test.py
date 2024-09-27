import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()

# x = (i for i in "hello")
# print(x)

# s = " My name is muhammad usman khadim hussain "
# x =  {char : s.count(char) for char in set(s)}
# print(x)

# x = [["usman" for _ in range(5)] for _ in range(5)]
# print(x)

# names = ['Abdul-Rehman',"usman","faisal","zain","shehbaz"]
# ages= [26,24,24,20,24]
# eye_color = ['black','brown','brown','brown','black']

# print(list(zip(names,ages,eye_color)))

# for name, age, eye_color in zip(names,ages,eye_color):
#     if age > 20:
#         print(name,eye_color)
 
# num = input('number: ')
# print(type(num))

# print(int(num) - 5)

# x  = 7
# y = 8
# z = 0

# result1 = x == y
# result2 = y > x
# result3 = z < x + 2

# result4 = result1 or result2
# print(result4)

# x = [3,4,42,3,2,4]
# for i, ele in enumerate(x):
#     print(i)

# x = [0,1,2,3,4,5,6,7,8]
# y = ['hi','hello','bye','goodbye','cya','sure']
# s = "hello"
# sliced = x[::-1]
# print(sliced)

# x = set()
# s = {4,32,2,2,23}
# print(type(x))
# s.add(5)
# print(s)

# x = {'key':4}
# print(x.values())

# def decorator_with_arguments(function):
#     def wrapper_accepting_arguments(arg1, arg2):
#         print("My arguments are: {0}, {1}".format(arg1,arg2))
#         # function(arg1, arg2)
#     return wrapper_accepting_arguments


# @decorator_with_arguments
# def cities(city_one, city_two):
#     print("Cities I love are {0} and {1}".format(city_one, city_two))

# cities("Nairobi", "Accra")

# try:
#     x = 7/0
# except Exception as e :
#     print(e)
# finally:
#     print('finally')

# x = lambda x, y: x + y
# print(x(2,32))

# def repeat_decorator(num_repeats = 2)


# import numpy as np
# import pandas as pd
 
# # function decorator to ensure numpy input
# # and round off output to 4 decimal places
# def ensure_numpy(fn):
#     def decorated_function(data):
#         array = np.asarray(data)
#         output = fn(array)
#         return np.around(output, 4)
#     return decorated_function
 
# @ensure_numpy
# def numpysum(array):
#     return array.sum()
 
# x = np.random.randn(10,3)
# y = pd.DataFrame(x, columns=["A", "B", "C"])
 
# # output of numpy .sum() function
# print("x.sum():", x.sum())
# print()
 
# # output of pandas .sum() funuction
# print("y.sum():", y.sum())
# print(y.sum())
# print()
 
# # calling decorated numpysum function
# print("numpysum(x):", numpysum(x))
# print("numpysum(y):", numpysum(y))

# import pickle
# import hashlib
 
 
# MEMO = {} # To remember the function input and output
 
# def memoize(fn):
#     def _deco(*args, **kwargs):
#         # pickle the function arguments and obtain hash as the store keys
#         key = (fn.__name__, hashlib.md5(pickle.dumps((args, kwargs), 4)).hexdigest())
#         # check if the key exists
#         if key in MEMO:
#             ret = pickle.loads(MEMO[key])
#         else:
#             ret = fn(*args, **kwargs)
#             MEMO[key] = pickle.dumps(ret)
#         return ret
#     return _deco
 
# @memoize
# def fibonacci(n):
#     if n in [0, 1]:
#         return n
#     else:
#         return fibonacci(n-1) + fibonacci(n-2)
 
# print(fibonacci(40))
# print(MEMO)

# import pandas_datareader as pdr

# @memoize
# def get_stock_data(ticker):
#     # pull data from stooq
#     df = pdr.stooq.StooqDailyReader(symbols=ticker, start="1/1/00", end="31/12/21").read()
#     return df

# #testing call to function
# import cProfile as profile
# import pstats

# for i in range(1, 3):
#     print(f"Run {i}")
#     run_profile = profile.Profile()
#     run_profile.enable()
#     get_stock_data("^DJI")
#     run_profile.disable()
#     pstats.Stats(run_profile).print_stats(0)

# def generator(n):
#     value = 0
#     while value < n:
#         yield value
#         value += 1
# for value in generator(15):
#     print(value)

# s_generator = (i * i for i in range(5))
# for i in s_generator:
#     print(i)

# def fibonacci_numbers(nums):
#     x, y = 0, 1
#     for _ in range(nums):
#         x, y = y, x+y
#         yield x
# def square(nums):
#     for num in nums:
#         yield num**2
# print(sum(square(fibonacci_numbers(10))))

# def simpleGen():
#     yield 1
#     yield 2
#     # yield 3

# for value in simpleGen():
#     print(value)

# def simpleGeneratorFun(): 
#     yield 1
#     yield 2
#     yield 3
#     yield 4
#     yield 5
#     yield 6
   
# x = simpleGeneratorFun() 
# print(next(x)) 
# print(next(x)) 
# print(next(x))
# print(next(x))
# print(next(x))

# def is_palindrome(num):
#     if num / 10 == 0:
#         return False
#     temp = num
#     reversed_num = 0

#     while temp != 0:
#         reversed_num = (reversed_num * 10) + (temp // 10)
#         # temp = temp // 10

#     if num == reversed_num:
#         return True
#     else:
#         return False
    
# a = is_palindrome(40)
# print(a)


# def Fibbo_Sequence_Generator():
#     # Generates a fibonacci sequence with the size of ngi
#     runFib = True
#     while(runFib):
#         n = int(input('How many numbers do you need? '))
#         if n > 0 :
#             runFib = False
#             series = [1]

#             while len(series) < n:
#                 if len(series) == 1:
#                     series.append(1)
#                 else:
#                     series.append(series[-1] + series[-2])

#             for i in range(len(series)):  # Convert the numbers to strings
#                 series[i] = str(series[i])
#         else:
#             print('enter a valid number')

#     return(', '.join(series))  # Return the sequence seperated by commas

# print(Fibbo_Sequence_Generator())

x = 10
 
print(callable(x))
 
# def geeks(x):
#     return (x)
 
# y = geeks
# print(callable(y))

# class Foo:
#   def printLine(self):
#     print('Print Something')

# print(callable(Foo))
# InstanceOfFoo = Foo()
# InstanceOfFoo()

print("Is str callable? ", callable(str)) # str class
print("Is len callable? ", callable(len)) # len function
print("Is list callable? ", callable(list)) # list class

num=10
print("Is variable callable? ", callable(num)) 
