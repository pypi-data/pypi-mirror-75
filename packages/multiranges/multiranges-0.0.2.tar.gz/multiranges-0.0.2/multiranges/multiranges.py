import functools

from multiranges.exceptions import NoRangeableObjectError


def productReduce(squence, default=0):
    """Reduce a list of ints by product"""
    return functools.reduce(lambda x, y: x * y, squence) if squence else default


def lens(_list):
    """Map a list of iterabels with len() function"""
    return [len(x) for x in _list]


def argToRange(arg):
    """Map a value to a rangeable object:
        tuple (x, y) -> range(x, y)
        range (x, y) -> same range(x, y)
        int x -> range (0, x)
        list -> same list
        string -> same string
        tuple (...) -> list (...)
        set (...) -> list (...)
    """
    # (init, end)
    if isinstance(arg, tuple) and len(arg) == 2:
        return range(arg[0], arg[1])
    # [o1, o2, o3]
    elif isinstance(arg, (range, list, str, MultiRange)):
        return arg
    elif isinstance(arg, (tuple, set)) and len(arg) > 0:
        return list(arg)
    # 1, 166, any positive integer
    elif isinstance(arg, int) and arg > 0:
        return range(arg)
    else:
        raise NoRangeableObjectError(arg)


def _generator(ranges):
    """Generator function based en ranges"""
    if not ranges:
        return []
    elif len(ranges) == 1:
        for value in ranges[0]:
            yield value
    else:
        limits = lens(ranges)
        indexes = [0] * len(ranges)
        while not indexes[0] == limits[0]:
            # Return actual value
            actual = [ranges[irange][ivalue] for irange, ivalue in enumerate(indexes)]
            yield tuple(actual)
            # Update indexes
            indexes[-1] += 1
            for i in range(len(ranges) - 1):
                actual = indexes[- (i + 1)]
                limit = limits[- (i + 1)]
                # should update left index?
                if actual == limit:
                    # reset index to 0
                    indexes[- (i + 1)] = 0

                    # update left index +1
                    indexes[- (i + 2)] += 1
                else:
                    break


class MultiRange:
    # TODO: [len(r) for r in self.ranges] repeated
    def __init__(self, *args):
        self.ranges = [argToRange(arg) for arg in args]
        self.generator = _generator(self.ranges)

    def __len__(self):
        return productReduce(lens(self.ranges))

    def __iter__(self):
        return self.generator

    # def next(self):
    #     return next(self.generator)

    def __getitem__(self, item):
        if item > self.__len__():
            raise IndexError

        # Get the division factors as de product reduction of the tails elements of the list, ignoring the last one
        # Example: ranges = [range(3), 'hello', [1, 3, 7, 9]]
        #            Lens = [3, 5, 4]
        #        Divisors = [5 * 4, 5] = [20, 5]
        _lens = lens(self.ranges)
        divisors = [productReduce(_lens[i+1::]) for i, _ in enumerate(_lens[:-1:])]

        indexes = []
        dividend = item
        for i, divisor in enumerate(divisors):
            quotient = dividend // divisor
            dividend = dividend % divisor
            indexes.append(quotient)

        indexes.append(dividend)
        value = tuple([r[indexes[i]] for i, r in enumerate(self.ranges)])
        return value
