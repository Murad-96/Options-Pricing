import math

class StockOption(object):
    def __init__(self, S0, K, r, div, sigma, T, N, is_put = False):
        """
        Initialize European stock option base class
        :param S0: initial stock price
        :param K: price
        :param r: risk free rate
        :param div: stock's dividend
        :param sigma: volatility
        :param T: time to maturity
        :param N: number of time steps
        :param is_put: True for a put option, false for a call option
        """
        self.S0 = S0
        self.K = K
        self.r = r
        self.div = div
        self.sigma = sigma
        self.T = T
        self.N = max(1, N)
        self.is_put = is_put

        """ Optional Parameters used by derived classes """
        self.pu = 0    # probability of an up move
        self.pd = 0     # probability of a down move
        self.is_call = not is_put
        self.ST = []    # stores stock prices at each terminal node of the tree

    @property
    def dt(self):
        # single time step
        return self.T / float(self.N)

    @property
    def df(self):
        # discount factor
        return math.exp(-self.dt * (self.r - self.div))

    def switch_type(self):
        if self.is_put is False:
            self.is_put = True
        else:
            self.is_put = False
        del self.ST[:]  # reset terminal prices list


class BinomialEuropeanOption(StockOption):
    def setup_parameters(self):
        # required calculations for the model
        self.steps = self.N + 1
        self.u = math.exp(self.sigma * math.sqrt(self.dt))
        self.d = float(1/self.u)
        self.pu = (math.exp((self.r - self.div) * self.dt) - self.d) / (float(self.u - self.d))
        self.pd = 1 - self.pu

    def init_tree(self):
        # get all prices at each node into self.ST list
        if self.is_put is False:
            for i in range(self.steps):
                spot = self.S0 * (self.u ** (self.steps - (i + 1))) * self.d ** i
                if spot > self.K:
                    self.ST.append(spot - self.K)
                else:
                    self.ST.append(0)
        else:
            for i in range(self.steps):
                spot = self.S0 * (self.u ** (self.steps - (i + 1))) * self.d ** i
                if spot < self.K:
                    self.ST.append(self.K - spot)
                else:
                    self.ST.append(0)

    def price(self):
        self.setup_parameters()
        self.init_tree()
        self.steps -= 1
        if self.is_put is False:
            # discount option prices
            for j in range(self.steps, 0, -1):
                for i in range(j):
                    self.ST[i] = ((self.ST[i] * self.pu) + (self.ST[i + 1] * self.pd)) * self.df
            return self.ST[0]

        else:
            for j in range(self.steps):
                for i in range(self.steps, j, -1):
                    self.ST[i] = ((self.ST[i] * self.pd) + (self.ST[i - 1] * self.pu)) * self.df
            return max(self.ST)  # or self.ST[-1]