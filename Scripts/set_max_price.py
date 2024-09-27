import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "conf.settings")
import django
django.setup()
from company.models import SubPlan,Terms

subplans = SubPlan.objects.all()
for subplan in subplans:
    if subplan.claim_limit_of_liability > 0:
        claim_limit_of_liability = 0.8 * subplan.claim_limit_of_liability
        subplan.claim_limit_of_liability = claim_limit_of_liability
        term = Terms.objects.filter(subplan__id=subplan.id).update(max_price=claim_limit_of_liability)

# print(bool)
# print(bool(""))
# print(bool(1))
# print(bool(-1))
# print(bool([1,2]))
# print(bool({}))
# print(bool({"key":"value"}))

# Callable ()

# class Class:
#     pass
# def func():
#     print("hi")
# def func2():
#     def inner():
#         pass
#     return inner
# func3  = lambda x:x + 1
# not_func = "hello"

# print(callable(Class))
# print(callable(func))
# print(callable(func2()))
# print(callable(func3))
# print(callable(not_func))

# A = 65
# a = 97
# print(chr(A))
# print(chr(a))

# Class Method classmethod()

# class TestClass:
#     def regular_method(self):
#         print(self)
    
#     @classmethod
#     def class_method(cls):
#         print(cls)
    
#     def __str__(self):
#         return "TestClass Instance"

# t = TestClass()
# t.regular_method()
# t.class_method()
# TestClass.class_method()

# a = [1,1,1,3,3]
# print(all(a))

# import asyncio

# class AsyncIterator:
#     def __init__(self,start,stop):
#         self.start = start
#         self.stop = stop
#     def __aiter__(self):
#         self.cur = self.start
#         return self
#     async def __anext__(self):
#         await asyncio.sleep(1)
#         if self.cur >= self.stop:
#             raise StopAsyncIteration
#         self.cur +=1
#         return self.cur -1
    
# async def example():
#     custom_obj = AsyncIterator(1,10)
#     obj_iter = aiter(custom_obj)
#     print(await anext(obj_iter))
#     print(await anext(obj_iter))
#     print(await anext(obj_iter))
# asyncio.run(example())

# complex1 = '32+2j'
# print(complex(complex1))

# print(complex(3,4))
# class MyClass:
#     def __init__(self,x):
#         self.x = x
# c = MyClass(10)
# print(c.x)
# delattr(c,"x")
# print(c.x)