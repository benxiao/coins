import math
from scipy.stats import norm
from enum import Enum

y = [46.8, 27.8, 32.5, 39.5, 32.8, 31.0, 26.2, 20.8]
y1 = 26.8


class TestType(Enum):
    Equality = 0
    LessThan = 1
    GreaterThan = 2


def approx_variance(d):
    mval = mean(d)
    l = len(d)
    if l < 5:
        assert ValueError()

    return (1 / (l - 1) * sum((x-mval) ** 2 for x in d))


def mean(d):
    return sum(d) / len(d)


def zscoreForDistributionAndMean(d, v, known_variance=None):
    mval = mean(d)
    distribution_variance = known_variance or approx_variance(d)
    return (mval - v) / math.sqrt(distribution_variance / len(d))


def zcoreForTwoDistributions(d0, d1):
    m0 = mean(d0)
    m1 = mean(d1)
    return (m0 - m1)/ math.sqrt(approx_variance(d0)/len(d0)+approx_variance(d1)/len(d1))


def surprise(z, _type=None):
    _type = _type or TestType.Equality
    if _type == TestType.Equality:
        return 2 * norm.cdf(-abs(z))
    if _type == TestType.LessThan:
        return 1 - norm.cdf(z)
    else:
        return norm.cdf(z)


if __name__ == '__main__':
    z = zscoreForDistributionAndMean(y, y1, known_variance=4.5 ** 2)
    z2 = zscoreForDistributionAndMean(y,  y1) # in this case variance will be computed
    print("when variance is known: ",surprise(z))
    # when the variance is unknown, surprise is estimated in a far more conservative manner.
    print("when variance is unknown: ", surprise(z2))

    z = zscoreForDistributionAndMean([-1,2,3,4,5], -1100)
    print(surprise(z, _type=TestType.LessThan))
    z = zcoreForTwoDistributions([1,2,3,2,1],[-1,-2,-3,-2,-1])
    print(surprise(z, _type=TestType.LessThan))



