import pprint
import time
from typing import Final

"""
The following is a class and set of unit tests related to Hyperoperation.
A number class is implemented with a unary representation.
It implements increment/succession via python list addition of a single value.
Higher order operations are layered above up to and including tetration/hyper-4.

Notes about implementation:
* after inc, (add,mul,pow,tetr) are extremely similar with the exception of their
  initial condition.

References:
https://en.wikipedia.org/wiki/Hyperoperation
"""


def assert_equal(a, b):
    if a != b:
        raise AssertionError(f"{a} does not equal {b}")


class number:
    """
    A number class with unary internal representation that attempts to implement
    arithmatic operations with minimal external functions.

    Member functions attempt to be functional in intent, but are implemented in an
    imperative style. (Because that is how I learned how to program?)
    """

    # Use a property to ensure the state is immutable
    @property
    def state(self):
        return self._state

    def __init__(self, copy_state=None):
        if None is copy_state:
            self._state = []  # Unary zero
        else:
            self._state = copy_state.copy()

    @staticmethod
    def create_zero():
        #  I kind of hate to add this, but it might make creating a 0
        #  clearer for new readers
        return number()

    def inc(self):
        # Make a new number that is the previous list + a new element
        # (conscious effort to not use the + operator here even if it
        #  is just a cosmetic distinction)
        return number([*self.state, 'x'])

    def add(self, b):
        # 0th iteration is identity
        result = number(self.state)
        for _ in b.state:
            result = result.inc()
        return result

    def mul(self, b):
        # 0th iteration is 0
        result = number.create_zero()
        for _ in b.state:
            result = result.add(self)
        return result

    def pow(self, b):
        # 0th iteration is 1
        result = number.create_zero().inc()
        for _ in b.state:
            result = result.mul(self)
        return result

    def tetr(self, b):
        # Stupid piecewise definition
        try:
            b.state[0]
        except:
            # 0th iteration is 1
            return number.create_zero().inc()
        result = number(self.state)
        once = True
        # For the non-zero tetration case, you loop b - 1 times.
        for _ in b.state:
            if once:  # Skip the first so do one less
                once = False
                continue
            result = result.pow(self)
        return result

    def dec(self):
        try:
            self.state[0]
            return number(self.state[1:])
        except:
            raise("Oops.  You tried to decrement a zero.  Just natural numbers for now.")

    def compare(self, b):
        for _ in self.state:
            try:
                b.state[0]
                b = b.dec()
            except:
                return "greater"
        try:
            b.state[0]
            return "less"
        except:
            return "equal"


def standard_tests():

# Base representation
    # Test equality of zeros
    a = number.create_zero()
    b = number.create_zero()
    assert_equal(a.compare(b), "equal")

    # We can't test inequality until we can make a different number!

# Base operation, increment

    zero: Final = number.create_zero()

    # Verify 0 incremented is 1 > 0
    one: Final = number.create_zero().inc()
    assert_equal(one.compare(zero), "greater")

    assert_equal(zero.compare(one), "less")



# Addition

    # Basic... 1 + 2 = 3
    two: Final = zero.inc().inc()
    three: Final = one.add(two)
    assert_equal(three.compare(zero.inc().inc().inc()), "equal")

    # identity is 0
    one_b = one.add(number.create_zero())
    assert_equal(one_b.compare(one), "equal")

    # Commutivity... 1 + 2 = 2 + 1
    three_fwd = one.add(two)
    three_rev = two.add(one)
    assert_equal(three_fwd.compare(three_rev), "equal")

    # Associativity... (1 + 2) + 3 = 1 + (2 + 3)
    six = one.add(two).add(three)
    six_b = one.add(two.add(three))
    assert_equal(six.compare(six_b), "equal")



# Multiplication

    # Verify multiplication... 2 * 3 = 6
    six = two.mul(three)
    assert_equal(six.compare(three.add(three)), "equal")

    # Multiplication by Zero... 2 * 0 = 0
    two_times_zero: Final = two.mul(number.create_zero())
    assert_equal(two_times_zero.compare(zero), "equal")

    # identity... 2 * 1 = 2
    two_times_one = two.mul(zero.inc())
    assert_equal(two_times_one.compare(two), "equal")

    # Commutivity... 2 * 6 = 6 * 1
    twelve: Final = two.mul(six)
    twelve_b = six.mul(two)
    assert_equal(twelve.compare(twelve_b), "equal")

    # Associativity
    thirtysix: Final = two.mul(three).mul(six)
    thirtysix_b = two.mul(three.mul(six))
    assert_equal(thirtysix.compare(thirtysix_b), "equal")


# Power

    # Basic... 2 ^ 3 = 8
    eight: Final = two.pow(three)
    four: Final = two.add(two)
    assert_equal(eight.compare(four.add(four)), "equal")

    # Zer power... 2 ^ 0 = 1
    two_to_zero = two.pow(zero)
    assert_equal(two_to_zero.compare(one), "equal")

# Tetration

    # 2 ^^ 3 = 16
    sixteen: Final = two.pow(two).pow(two)
    two_tetra_three = two.tetr(three)
    assert_equal(sixteen.compare(two_tetra_three), "equal")

    # X ^^ 0 = 1, so we'll just use sixteen, 0 = 1
    sixteen_tetrated_zero = sixteen.tetr(zero)
    assert_equal(sixteen_tetrated_zero.compare(one), "equal")

    # timing test for fun
    results = {}
    count = 0
    height = number.create_zero()
    while True:
        start = time.time_ns()
        result = two.tetr(height)
        duration = time.time_ns() - start
        results[count] = (duration, len(result.state))
        if count > 4:
            # Stop at 64K.  64K outside of debug mode is ~12s on my laptop.
            # Next would be 4GB.  Assuming runtime is linear vs size as this is just
            # adding more unary digits, that is ~5K un-digits/s.  4GB is ~850K seconds/
            # ~14K minutes/~238 hours/~4 days.  Small differences in implementations can push
            # this time down to barely measurable or unreasonably long for a unit test.
            break
        count += 1
        height = height.inc()

    print(f"Tetration stats:")
    pprint.pprint(results)


if __name__ == '__main__':
    standard_tests()
