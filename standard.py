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


# short name to reduce clutter
n_ = PreDefs()
