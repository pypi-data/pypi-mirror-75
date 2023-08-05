cimport cython
from libc.math cimport sqrt
from libc.limits cimport ULONG_MAX
from libc.stdlib cimport calloc, free, ldiv, ldiv_t
from libc.string cimport memcpy

__version__ = '0.7.0'
max_ulong = ULONG_MAX


cpdef _check_int(num, name='number'):
    if not isinstance(num, int):
        raise TypeError(f'{name} must be integer')


cpdef _check_range(num, limit):
    if num < 0 or num > limit:
        raise ValueError(f'out of range 0..{limit}')


@cython.cdivision(True)
cpdef bint is_prime(number) except -1:
    _check_int(number)
    _check_range(number, max_ulong)
    cdef unsigned long n = <unsigned  long> number
    if n <= 1:
        return 0
    if n < 4:
        return 1
    if n % 2 == 0:
        return 0
    if n < 9:
        return 1
    if n % 3 == 0:
        return 0
    cdef unsigned long r = <unsigned long> sqrt(n)
    cdef unsigned long f = 5
    while f <= r:
        if n % f == 0 or n % (f + 2) == 0:
            return 0
        f += 6
    return 1


cpdef unsigned long next_prime(number) except -1:
    _check_int(number)
    cdef unsigned long n = <unsigned  long> number
    if n == 0 or n == 1:
        return 2
    if n % 2 == 0:
        n = n + 1
    else:
        n = n + 2
    for x in range(n, max_ulong, 2):
        if is_prime(x):
            return x


cpdef unsigned long previous_prime(number) except -1:
    _check_int(number)
    cdef unsigned long n = <unsigned  long> number
    if n <= 2:
        raise ValueError(f'no previous prime for {number}')
    if n == 3:
        return 2
    if n % 2 == 0:
        n = n - 1
    else:
        n = n - 2
    for x in range(n, 1, -2):
        if is_prime(x):
            return x


cpdef tuple primes_between(start, end):
    _check_int(start, 'start')
    _check_int(end, 'end')
    if end < start:
        raise ValueError('end must be > start')
    if not is_prime(start):
        start = next_prime(start)
    if not is_prime(end):
        end = previous_prime(end)
    if start > end:
        return ()
    if start == end:
        return (start,)
    if start == 2:
        if end == 3:
            return (2, 3)
        r = [2]
        start = 3
    else:
        r = [start]
        start = start + 2
    for x in range(start, end, 2):
        if is_prime(x):
            r.append(x)
    r.append(end)
    return tuple(r)


cdef class Primes:
    cdef char *data
    cdef readonly long limit
    cdef long len
    cdef long ar_len
    cdef size_t ar_size

    def __cinit__(self, limit):
        _check_int(limit, 'limit')
        if limit <= 0:
            raise ValueError(f'limit must be > 0 (got {limit})')
        cdef long n = <long> limit
        self.limit = n
        self.ar_len = (n - 3) // 2 + 1
        self.len = self.ar_len + 1 if n > 1 else 0
        cdef ldiv_t r = ldiv(self.ar_len, 8)
        self.ar_size = r.quot + (1 if r.rem else 0)
        self.data = <char*> calloc(self.ar_size, 1)
        if not self.data:
            raise MemoryError()

    def __init__(self, limit):
        cdef long i, k, s, n = <long> limit
        for i in range(3, <long> sqrt(n) + 1, 2):
            if self.get_bit((i - 3) // 2) == 1:
                continue
            k = i * i
            s = 2 * i
            while k <= n:
                self.set_bit((k - 3) // 2)
                k += s

    def __dealloc__(self):
        free(self.data)

    cdef void set_bit(self, long idx):
        cdef ldiv_t r = ldiv(idx, 8)
        if not self.data[r.quot] & (1 << r.rem):
            self.len -= 1
            self.data[r.quot] |= 1 << r.rem

    cdef int get_bit(self, long idx):
        cdef ldiv_t r = ldiv(idx, 8)
        return 1 if self.data[r.quot] & (1 << r.rem) else 0

    def __len__(self):
        return self.len

    def __contains__(self, num):
        _check_range(num, self.limit)
        if num == 2:
            return True
        if num < 2 or num % 2 == 0:
            return False
        return self.get_bit((num - 3) // 2) == 0

    def __iter__(self):
        def iterator():
            if self.limit >= 2:
                yield 2
                yield from (i * 2 + 3 for i in range(self.ar_len)
                            if self.get_bit(i) == 0)
        return iterator()

    def __reversed__(self):
        def iterator():
            if self.limit >= 2:
                yield from (i * 2 + 3 for i in range(self.ar_len - 1, -1, -1)
                            if self.get_bit(i) == 0)
                yield 2
        return iterator()

    def __getitem__(self, idx):
        length = self.__len__()
        if isinstance(idx, slice):
            lst = []
            for x in range(*idx.indices(length)):
                lst.append(self.__getitem__(x))
            return tuple(lst)
        if idx < 0:
            idx = length + idx
        if idx < 0 or idx >= length:
            raise IndexError('list index out of range')
        if idx == 0:
            return 2
        cdef long c = 0, i = <long> idx, k
        for k in range(self.ar_len):
            if self.get_bit(k) == 0:
                c += 1
                if c == i:
                    return k * 2 + 3

    def __eq__(self, other):
        return self.len == len(other)

    def __hash__(self):
        return hash(self.len)

    def __sizeof__(self):
        return sizeof(char*) + 3 * sizeof(long) + sizeof(size_t) + self.ar_size

    def __repr__(self):
        return f'{self.__class__.__name__}(limit={self.limit})'

    def index(self, number):
        _check_int(number)
        _check_range(number, self.limit)
        if number == 2:
            return 0
        cdef long idx = <long> (number - 3) // 2
        if number < 2 or number % 2 == 0 or self.get_bit(idx) == 1:
            raise ValueError('not prime')
        cdef long c = 1, i
        for i in range(idx):
            if self.get_bit(i) == 0:
                c += 1
        return c

    def next(self, number):
        _check_int(number)
        _check_range(number, self.limit)
        if number < 2:
            return 2
        for n in range(number + 2 if number % 2 else number + 1, self.limit + 1, 2):
            if n in self:
                return n

    def previous(self, number):
        _check_int(number)
        _check_range(number, self.limit)
        if number == 3:
            return 2
        for n in range(number - 2 if number % 2 else number - 1, 0, -2):
            if n in self:
                return n

    def between(self, start, end):
        _check_int(start, 'start')
        _check_int(end, 'end')
        _check_range(start, self.limit)
        _check_range(end, self.limit)
        if end < start:
            raise ValueError('end must be > start')
        r = []
        for n in range(start, end + 1):
            if n in self:
                r.append(n)
        return tuple(r)

    cdef bytes get_data(self):
        return <bytes> (<char*> self.data)[:self.ar_size]

    cdef void set_data(self, bytes data, long length):
        memcpy(self.data, <char*> data, self.ar_size)
        self.len = length

    def __reduce__(self):
        return _reconstruct, (self.get_data(), self.limit, self.len)


cpdef object _reconstruct(data, limit, length):
    obj = Primes.__new__(Primes, limit)
    Primes.set_data(obj, data, length)
    return obj
