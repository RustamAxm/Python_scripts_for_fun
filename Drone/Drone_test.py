from functools import wraps

def log(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print(f'init: {args}, {kwargs}')
        output = f(*args, **kwargs)
        print(f'output = {output}')
        print('finished')
        return output
    return decorated

@log
def add_one(a):
    print('add one')
    return a + 1

@log
def minus_one(a):
    print('minus one')
    return a - 1

print(add_one(a=10))
print(minus_one(a=10))