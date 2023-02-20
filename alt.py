from typing import Final
from standard import number



class alt_num(number):

    @property
    def fx_tab(self):
        return {
            0: self.inc,
            1: self.add,
            2: self.mul,
            3: self.pow,
            4: self.tetr
        }

    def apply(self, b, i):
        result = number(self.state)
        for _ in range(b.val() - 1):
            result = result.fx_tab()[i](result)
        return result

    def inc(self, _=None):
        # Make a new number that is the previous list + a new element
        # (conscious effort to not use the + operator here even if it
        #  is just a cosmetic distinction)
        return alt_num([*self.state, 'x'])

    def add(self, b):
        return self.apply(b, 0)

    def mul(self, b):
        return self.apply(b, 1)

    def pow(self, b):
        return self.apply(b, 2)

    def tetr(self, b):
        return self.apply(b, 3)

    def do(self, b, i):
        return self.apply(b, i)

    @staticmethod
    def create_zero():
        return alt_num()


def assert_equal(a, b):
    if a != b:
        raise AssertionError(f"{a} does not equal {b}")


def test_alt():
# Base representation
    # Test equality of zeros
    a = alt_num.create_zero()
    b = alt_num.create_zero()
    assert_equal(a.val(), b.val())

    # We can't test inequality until we can make a different number!

# Base operation, increment

    # Verify 0 incremented is 1

    zero: Final = alt_num.create_zero()

    one: Final = zero.inc()
    assert_equal(one.val(), 1)

    # Now we can test inequality
    inequality_success = False
    try:
        assert_equal(one.val(), zero.val())
    except AssertionError:
        inequality_success = True
    assert inequality_success

    # Verify 0 incremented twice is 2
    two = zero.inc().inc()
    assert_equal(two.val(), 2)

    one: Final = zero.inc()

    three: Final = zero.inc().inc().inc()
    # For alternate addition,
    #   N + M = {
    #     M<=1: N
    #     M>1: N-1
    # }
    result = one.add(one)
    assert_equal(result.val(), 1)

    result = two.add(one)
    assert_equal(result.val(), 2)

    result = one.add(two)
    assert_equal(result.val(), 2)

    result = two.add(two)
    assert_equal(result.val(), 3)

    result = two.add(three)
    assert_equal(result.val(), 4)

    result = three.add(two)
    assert_equal(result.val(), 4)

    # For alt-mult, N * M = N * (M+1)

    result_a: Final = two.mul(zero)
    assert_equal(result_a.val(), 2)

    # 2 x 2 = 6
    result_b = two.mul(zero)
    assert_equal(result_b.val(), 2)

    # 2 x 3 = 2 x (3+1)
    result_c = two.mul(three)
    assert_equal(result_c.val(), 8)

    # For alt-pow, N ^ M = {
    #   M = 0, N
    #   M > 0, N^M
    # }
    result = two.pow(zero)
    assert_equal(result.val(), 2)

    result = two.pow(one)
    assert_equal(result.val(), 2)

    result = two.pow(two)
    assert_equal(result.val(), 4)

    result = three.pow(two)
    assert_equal(result.val(), 9)


if __name__ == '__main__':
    test_alt()

