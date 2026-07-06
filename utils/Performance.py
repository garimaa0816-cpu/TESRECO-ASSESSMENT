import time

def logger(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print("Execution Time:", time.time() - start)
        return result
    return wrapper

@logger
def calculate_performance(attendance, tasks):
    return (attendance * 0.4) + (tasks * 0.6)