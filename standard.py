import pprint
import time
from typing import Final
from types import SimpleNamespace

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


def assert_val_equal(a):
    if a != "equal":
        raise AssertionError(f"{a} is not \"equal\"")


def assert_equal(a, b):
    if a != b:
        raise AssertionError(f"{a} is not {b}")


class UnderflowError(ArithmeticError):
    pass


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
        result = n_.zero
        for _ in b.state:
            result = result.add(self)
        return result

    def pow(self, b):
        # 0th iteration is 1
        result = n_.one
        for _ in b.state:
            result = result.mul(self)
        return result

    def tetr(self, b):
        # Stupid piecewise definition
        if b.compare(n_.zero) == "equal":
            # 0th iteration is 1
            return n_.one
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
        if self.compare(n_.zero) == "equal":
            raise UnderflowError("Oops.  You tried to decrement a zero.  Just natural numbers for now.")
        return number(self.state[1:])

    def sub(self, s):
        result = self
        for _ in s.state:
            if result.compare(n_.zero) == "equal":
                raise UnderflowError(
                    "Oops.  You tried to subtract a larger number from a smaller one.  Just natural numbers for now.")
            result = result.dec()
        return result

    def div(self, denominator):
        numerator = number(self.state)
        divisions = n_.zero
        if denominator.compare(n_.zero) == "equal":
            raise ZeroDivisionError()
        while True:
            progress = n_.zero
            for _ in denominator.state:
                if numerator.compare(n_.zero) == "equal":
                    return divisions, progress
                numerator = numerator.dec()
                progress = progress.inc()
            divisions = divisions.inc()

    #  This returns (magnitude, mantissa)
    #  But the currently returned mantissa may not be the best representation.
    #  It is the integer remainder of the next higher magnitude.
    #  As this is a closed form solution, it seems complete enough.
    def log(self, base):
        numerator = number(self.state)
        if base.compare(n_.zero) == "equal":
            raise ZeroDivisionError()
        if base.compare(n_.one) == "equal":
            return n_.zero, n_.zero, n_.zero
        magnitude = n_.zero
        while True:
            numerator, _ = numerator.div(base)
            if numerator.compare(n_.zero) == "equal":
                remainder = self.sub(base.pow(magnitude))
                return magnitude, remainder
            magnitude = magnitude.inc()

    def superlog(self, base):
        if base.compare(n_.zero) == "equal":
            raise ZeroDivisionError()
        if base.compare(n_.one) == "equal":
            return 1
        height = n_.one
        log_progress = number(self.state)
        curr_base = base
        while True:
            log_progress, _ = log_progress.log(curr_base)
            if log_progress.compare(n_.zero) == "equal":
                remainder = self.sub(base.tetr(height))
                return height, remainder
            height = height.inc()
            curr_base = curr_base.mul(curr_base)


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
    a = n_.zero
    b = n_.zero
    assert_val_equal(a.compare(b))

    # We can't test inequality until we can make a different number!

# Base operation, increment
    # Verify 0 incremented is 1 > 0
    assert_equal(n_.one.compare(n_.zero), "greater")

    assert_equal(n_.zero.compare(n_.one), "less")

# Addition
    # Basic... 1 + 2 = 3
    one: Final = number().inc()
    two: Final = number().inc().inc()
    three: Final = number().inc().inc().inc()
    assert_val_equal(three.compare(one.add(two)))

    # identity is 0
    one_b = one.add(number())
    assert_val_equal(one_b.compare(one))

    # Commutivity... 1 + 2 = 2 + 1
    three_fwd = one.add(two)
    three_rev = two.add(one)
    assert_val_equal(three_fwd.compare(three_rev))

    # Associativity... (1 + 2) + 3 = 1 + (2 + 3)
    six = one.add(two).add(three)
    six_b = one.add(two.add(three))
    assert_val_equal(six.compare(six_b))

# Multiplication
    # Verify multiplication... 2 * 3 = 6
    assert_val_equal(n_.six.compare(n_.three.add(n_.three)))

    # Multiplication by Zero... 2 * 0 = 0
    two_times_zero: Final = n_.two.mul(n_.zero)
    assert_val_equal(two_times_zero.compare(n_.zero))

    # identity... 2 * 1 = 2
    two_times_one = two.mul(n_.one)
    assert_val_equal(two_times_one.compare(two))

    # Commutivity... 2 * 6 = 6 * 1
    twelve: Final = n_.two.mul(n_.six)
    twelve_b = n_.six.mul(n_.two)
    assert_val_equal(twelve.compare(twelve_b))

    # Associativity
    thirtysix: Final = n_.two.mul(n_.three).mul(n_.six)
    thirtysix_b = n_.two.mul(n_.three.mul(n_.six))
    assert_val_equal(thirtysix.compare(thirtysix_b))

# Power
    # Basic... 2 ^ 3 = 8
    assert_val_equal(n_.eight.compare(n_.four.add(n_.four)))

    # Zero power... 2 ^ 0 = 1
    two_to_zero = n_.two.pow(n_.zero)
    assert_val_equal(two_to_zero.compare(n_.one))

# Tetration
    # 2 ^^ 3 = 16
    sixteen: Final = n_.two.pow(n_.two).pow(n_.two)
    two_tetra_three = n_.two.tetr(n_.three)
    assert_val_equal(sixteen.compare(two_tetra_three))

    # X ^^ 0 = 1, so we'll just use sixteen, 0 = 1
    sixteen_tetrated_zero = sixteen.tetr(n_.zero)
    assert_val_equal(sixteen_tetrated_zero.compare(n_.one))

    # timing test for fun
    if False:
        results = {}
        count = 0
        height = n_.zero
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

# decrement
    assert_val_equal(n_.one.dec().compare(n_.zero))
    assert_val_equal(n_.three.dec().compare(n_.two))
    assert_equal(n_.four.dec().compare(n_.two), "greater")

    no_except = False
    try:
        n_.zero.dec()
        no_except = True
    except UnderflowError:
        pass
    if no_except:
        raise Exception("Did get an UnderflowError when trying to decrement zero")

# subtraction
    # 0-0=0
    assert_val_equal(n_.zero.sub(n_.zero).compare(n_.zero))
    # 1-0=1
    assert_val_equal(n_.one.sub(n_.zero).compare(n_.one))
    # 1-1=0
    assert_val_equal(n_.one.sub(n_.one).compare(n_.zero))
    # 2-2=0
    assert_val_equal(n_.one.sub(n_.one).compare(n_.zero))
    # 3-1=2
    assert_val_equal(n_.three.sub(n_.one).compare(n_.two))
    # 1-2=underflow
    threw_underflow = False
    try:
        n_.one.sub(n_.two)
    except UnderflowError:
        threw_underflow = True
    assert threw_underflow

    # inverse operation tests
    # (x + y) - y = x
    # (5 + 3) - 3 = x
    assert_val_equal(n_.five.add(n_.three).sub(n_.three).compare(n_.five))
    # (x + y) - x = y
    # (5 + 3) - 5 = 3
    assert_val_equal(n_.five.add(n_.three).sub(n_.five).compare(n_.three))

# division
    # 0/1 = 0,0
    assert_val_equal(n_.zero.div(n_.one)[0].compare(n_.zero))
    assert_val_equal(n_.zero.div(n_.one)[1].compare(n_.zero))
    # 1/1 = 1,0
    assert_val_equal(n_.one.div(n_.one)[0].compare(n_.one))
    assert_val_equal(n_.one.div(n_.one)[1].compare(n_.zero))
    # 2/2 = 1,0
    assert_val_equal(n_.two.div(n_.two)[0].compare(n_.one))
    assert_val_equal(n_.two.div(n_.two)[1].compare(n_.zero))
    # 4/2 = 2,0
    assert_val_equal(n_.four.div(n_.two)[0].compare(n_.two))
    assert_val_equal(n_.four.div(n_.two)[1].compare(n_.zero))

    # 4/3 = 1,1
    assert_val_equal(n_.four.div(n_.three)[0].compare(n_.one))
    assert_val_equal(n_.four.div(n_.three)[1].compare(n_.one))

    # 8/3 = 2,2
    assert_val_equal(n_.eight.div(n_.three)[0].compare(n_.two))
    assert_val_equal(n_.eight.div(n_.three)[1].compare(n_.two))

    # 4/5 = 0,4
    five: Final = n_.two.add(n_.two).inc()
    assert_val_equal(n_.four.div(five)[0].compare(n_.zero))
    assert_val_equal(n_.four.div(five)[1].compare(n_.four))

    # 1/0 = by definition, returns DivideByZeroError
    no_except = True
    try:
        n_.one.div(n_.zero)
    except ZeroDivisionError:
        no_except = False
    assert (not no_except)

    # inverse operation tests
    # (x * y)/x = y rem 0
    # (5 * 3)/5 = 3 rem 0
    assert_val_equal(n_.five.mul(n_.three).div(n_.five)[0].compare(n_.three))
    assert_val_equal(n_.five.mul(n_.three).div(n_.five)[1].compare(n_.zero))
    # (x * y)/y = x rem 0
    # (5 * 3)/3 = 5 rem 0
    assert_val_equal(n_.five.mul(n_.three).div(n_.three)[0].compare(n_.five))
    assert_val_equal(n_.five.mul(n_.three).div(n_.three)[1].compare(n_.zero))


# log
    # log base 0 is undefined
    ok = False
    try:
        n_.zero.log(n_.zero)
    except ZeroDivisionError:
        ok = True
    assert ok

    # logˇ1(2) = 0, mant=0
    assert_val_equal(n_.two.log(n_.one)[0].compare(n_.zero))
    assert_val_equal(n_.two.log(n_.one)[1].compare(n_.zero))
    assert_val_equal(n_.two.log(n_.one)[2].compare(n_.zero))

    # logˇ2(2) = 1, mant=0
    assert_val_equal(n_.two.log(n_.two)[0].compare(n_.one))
    assert_val_equal(n_.two.log(n_.two)[1].compare(n_.zero))

    # logˇ2(4) = 2, mant=0
    assert_val_equal(n_.four.log(n_.two)[0].compare(n_.two))
    assert_val_equal(n_.four.log(n_.two)[1].compare(n_.zero))

    # logˇ2(8) = 3, mant=0
    assert_val_equal(n_.eight.log(n_.two)[0].compare(n_.three))
    assert_val_equal(n_.eight.log(n_.two)[1].compare(n_.zero))

    # logˇ2(15) = 3, mant=7
    fifteen: Final = n_.two.mul(n_.two).inc().mul(n_.three)
    assert_val_equal(fifteen.log(n_.two)[0].compare(n_.three))
    assert_val_equal(fifteen.log(n_.two)[1].compare(n_.seven))

    # logˇ3(15) = 2, mant=6
    assert_val_equal(fifteen.log(n_.three)[0].compare(n_.two))
    assert_val_equal(fifteen.log(n_.three)[1].compare(n_.six))

    # logˇ4(15) = 1, mant=11
    assert_val_equal(fifteen.log(n_.four)[0].compare(n_.one))
    assert_val_equal(fifteen.log(n_.four)[1].compare(n_.ten.inc()))

    # inverse operation test
    # general - logˇX(pow(X,Y) = Y, mant=0
    # logˇ5(pow(5,3) = 3, mant=0
    assert_val_equal(n_.three.pow(n_.five).log(n_.three)[0].compare(n_.five))
    assert_val_equal(n_.three.pow(n_.five).log(n_.three)[1].compare(n_.zero))

# superlog
    # superlogˇ2(16) = 3, 0 (2^2^2 = 2^4 = 16)
    sixteen: Final = fifteen.inc()
    assert_val_equal(sixteen.superlog(n_.two)[0].compare(n_.three))
    assert_val_equal(sixteen.superlog(n_.two)[1].compare(n_.zero))

    # superlogˇ2(255) = 3, 23  (2^2^2 = 2^4 = 16... 255-16 = 239
    twofiftyfive: Final = sixteen.mul(sixteen).dec()
    twothirtynine: Final = twofiftyfive.sub(sixteen)
    assert_val_equal(twofiftyfive.superlog(n_.two)[0].compare(n_.three))
    assert_val_equal(twofiftyfive.superlog(n_.two)[1].compare(twothirtynine))

    # superlogˇ3(20000) = 3, 317  (3^3 = 27^3 = 19683)
    twentythousand: Final = n_.ten.pow(n_.three).mul(n_.ten.mul(n_.two))
    threeseventeen: Final = n_.ten.pow(n_.two).mul(n_.three).add(n_.ten).add(n_.seven)
    assert_val_equal(twentythousand.superlog(n_.three)[0].compare(n_.three))
    assert_val_equal(twentythousand.superlog(n_.three)[1].compare(threeseventeen))




class SetOnceNamespace(SimpleNamespace):
    def __setattr__(self, key, value):
        if hasattr(key, 'property'):
            raise NotImplementedError(f"{key} can be set only once!  Existing value: {self.key}")
        SimpleNamespace.__setattr__(self, key, value)


# Helper with predefined numbers
class PreDefs:
    def __init__(self):
        self.zero = number()
        self.one = self.zero.inc()
        self.two = self.one.inc()
        self.three = self.one.add(self.two)
        self.four = self.two.add(self.two)
        self.five = self.two.add(self.three)
        self.six = self.three.add(self.three)
        self.six = self.three.add(self.three)
        self.seven = self.three.add(self.four)
        self.eight = self.four.add(self.four)
        self.nine = self.five.add(self.four)
        self.ten = self.five.add(self.five)


# short name to reduce clutter
n_ = PreDefs()


if __name__ == '__main__':
    standard_tests()
