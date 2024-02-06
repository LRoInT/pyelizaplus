def w1(func):
    def wrapper(*args, **kwargs):
        print(func.__name__)
        print(args)
        print(kwargs)
        print()
    return wrapper
@w1
def t1(a,b):
    c=a+b
    print("--------------")

t1(10,5)