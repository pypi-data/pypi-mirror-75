# CyPrimes

Module for working with [prime numbers](https://en.wikipedia.org/wiki/Prime_number) written
in [Cython](https://cython.org/).

This is just a toy project to try out Cython.


## Installation

    # pip install cyprimes

To install *CyPrimes* a C-compiler ([GCC](https://en.wikipedia.org/wiki/GNU_Compiler_Collection),
[MinGW](https://en.wikipedia.org/wiki/MinGW)) is required.


## Usage

### Function `is_prime(number)`

Returns `True` if the `number` is prime. Because it uses the C-type *unsigned long*
for `number` it raises a `ValueError` if `number < 0` or `number > cyprimes.max_ulong`. It raises
a `TypeError` if `number` is not an integer.

### Function `next_prime(number)`:

Returns the next prime number after `number`.

### Function `previous_prime(number)`

Returns the previous prime number before `number`.

### Function `primes_between(start, end)`

Returns a `tuple` with all prime numbers in the closed interval [`start`, `end`].


### Class `Primes(limit)`

This class uses the [Sieve of Eratosthenes](https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes)
to find all prime numbers up to `limit`.

An instance of this class supports the *len* and *sys.getsizeof* functions, the *in* and *==* operators,
subscription (with integer indexes and slices), is iterable, and can be pickled. Two *Primes* objects are
considered equal if they contain the same prime numbers.
A `TypeError` will be raised if `limit` is not an integer.

**Methods:** All methods raise `TypeError`s if their parameters are not integers and `ValueError`s
             if they are out of range.

* `index(number)`: Returns the index of `number`. Raises `ValueError` if `number` is not prime.

* `next(number)`: Returns the next prime number after `number` or `None` if their is none in the
                  given range.

* `previous(number)`: Returns the previous prime number before `number` or `None` if their is none
                      in the given range.

* `between(start, end)`: Returns a `tuple` with all prime numbers in the closed interval [`start`, `end`].


**Warning**

Although this class uses a bitarray for the sieve be carefull not to run out of memory:

|       limit       |   size   |
| ----------------: | -------: |
|               100 |      7 B |
|             1 000 |     63 B |
|            10 000 |    625 B |
|           100 000 |    6 KiB |
|         1 000 000 |   61 KiB |
|        10 000 000 |  610 KiB |
|       100 000 000 |    6 MiB |
|     1 000 000 000 |   60 MiB |
|    10 000 000 000 |  596 MiB |
|   100 000 000 000 |    6 GiB |
| 1 000 000 000 000 |   58 GiB |


## History

2020-07-27 (0.7.0)

* Add functions next_prime(), previous_prime(), and primes_between()

2020-06-25 (0.6.0)

* Add methods \_\_eq\_\_(), \_\_hash\_\_(), \_\_sizeof\_\_() ,and \_\_repr\_\_() to class Primes

2020-06-15 (0.5.0)

* Add methods next(), previous(), and between() to class Primes
* Add tests

2020-06-03 (0.4.3)

* Fix: README again :blush:

2020-06-03 (0.4.2)

* Fix: README

2020-06-03 (0.4.1)

* Fix: Primes() and is_prime() now raise TypeErrors if the parameter is not an integer
* Fix: Primes.\_\_reversed\_\_() now works correct

2020-06-02 (0.4.0)

* First public release
