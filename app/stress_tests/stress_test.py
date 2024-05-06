import random
import threading

def bubble_sort():
    arr = [random.randint(0, 1000) for _ in range(10000)]
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

def prime_numbers():
    primes = []
    for num in range(2, 1000000000):
        if is_prime(num):
            primes.append(num)
    return primes

def is_prime(n):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def start_fibonacci():
    fibonacci(35)

def start_threads():
    first_thread = threading.Thread(target=bubble_sort)
    second_thread = threading.Thread(target=prime_numbers)
    third_thread = threading.Thread(target=start_fibonacci)
    first_thread.start()
    second_thread.start()
    third_thread.start()

    first_thread.join()
    second_thread.join()
    third_thread.join()