import time

# Decorator for caching
def cached(func):
    cache = {}

    def wrapper(*args, **kwargs):
        key = (*args, *kwargs.items())

        if key in cache:
            print(f"Retrieving result from cache:{cache[key]}")
            return cache[key]

        result = func(*args, **kwargs)
        cache[key] = result

        return result

    return wrapper


@cached
def fibonacci(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

start = time.time()
result = fibonacci(40)
end = time.time()
print(f"Result: {result} and elapsed time: {end - start} seconds")