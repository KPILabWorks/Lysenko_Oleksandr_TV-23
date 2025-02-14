import time
from collections import Counter
import json
import csv


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
def analyze_word_frequency(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read().lower()

    words = text.split()
    word_frequency = Counter(words)

    # time.sleep(2)
    return dict(word_frequency)

def save_json(data, output):
    with open(output, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Results saved to {output}")

def save_csv(data, output):
    with open(output, 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Word", "Frequency"])
        for word, frequency in data.items():
            writer.writerow([word, frequency])
        print(f"Results saved to {output}")

filename = "text.txt"

# First run
start = time.time()
word_frequency = analyze_word_frequency(filename)
end = time.time()
print(f"First run (without cache) took: {end - start:.4f} seconds")

# Second run
start = time.time()
word_freq2 = analyze_word_frequency(filename)
end = time.time()
print(f"Second run (with cache) took: {end - start:.4f} seconds")

assert word_frequency == word_freq2, "Results should be the same!"
print("Cache is working correctly! ✅")

# print(f"Word Frequency = {word_frequency}")  # print word frequency if you want
# print(f"Elapsed Time = {end - start} seconds")

save_json(word_frequency, "word_frequency.json")
save_csv(word_frequency, "word_frequency.csv")