# Closure
def add_number(num):
    def adder(number):
        print("adder is a closeure")
        return num + number
    return adder

a_10 = add_number(10)
a_20 = add_number(20)

a1 = a_10(21)
a2 = a_20(21)

print(a1)
print(a2)


# Decorator_function
from functools import wraps
def NewDecorator(func):
    @wraps(func) # 함수명 및 설명문 유지, 없으면(NewAdd)
    def NewAdd(*args, **kwargs):
        print('Before call')
        result = func(*args, **kwargs)
        print('After call')
        return result
    return NewAdd

@NewDecorator
def add(a, b):
    print('Add')
    return a + b
sum = add(1, 3)

print(sum)
print(add.__name__) # @wraps(func) -> add(@wraps 사용) or NewAdd


# Decorator_class
class P2:
    def __init__(self, x):
        self.x = x
    
    @property
    def x(self):
        return self.x

    @x.setter
    def x(self, x):
        if x < 0:
            self._x = 0
        elif x > 1000:
            self._x = 1000
        else:
            self._x = x

p2 = P2(1001)
print(P2.x)

p2.x = -12
print(p2.x)    