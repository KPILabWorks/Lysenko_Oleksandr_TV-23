import time
from functools import cache, lru_cache # last recently used cache

@lru_cache(maxsize=10)
def fibonacci(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

start = time.time()
result = fibonacci(40)
end = time.time()
print(f"Result: {result} and elapsed time: {end - start} seconds")