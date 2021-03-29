import multiprocessing
from time import sleep

def myProcess(name,nsec):
    print ("---- do somthing ----")
    sleep(nsec)

if  __name__ == '__main__' :
    t = multiprocessing.Process(target=myProcess, args=("Process-1", 3))
    t.start()
    t.join()
    print ("---- exit ----")


from concurrent.futures import ProcessPoolExecutor
from time import sleep


def return_after_5_secs(message):
    sleep(5)
    return message

if  __name__ == '__main__' :
    pool = ProcessPoolExecutor(3)

    future = pool.submit(return_after_5_secs, ("hello"))
    print(future.done())
    sleep(5)
    print(future.done())
    print("Result: " + future.result())

import concurrent.futures
import math

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    1157978480787878787877099,
    1099726899285419]

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))


if __name__ == '__main__':
    main()

