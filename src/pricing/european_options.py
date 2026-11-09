
import numpy as np
from scipy.stats import norm


class EuropeanOption:
    """
    European option pricing using the Black-Scholes model.

    Parameters
    ----------
    S : float, Current underlying price
    K : float, Strike price
    T : float, Time to maturity in years
    r : float, Continuously compounded risk-free interest rate
    sigma : float, Annualised volatility
    option_type : str, 'call' or 'put'
    """

    def __init__(self, S, K, T, r, sigma, option_type="call"):
        if S <= 0 or K <= 0:
            raise ValueError("S and K must be positive.")

        if T < 0:
            raise ValueError("Time to maturity cannot be negative.")

        if sigma < 0:
            raise ValueError("Volatility cannot be negative.")

        if option_type.lower() not in ["call", "put"]:
            raise ValueError("option_type must be 'call' or 'put'.")

        self.__S = S
        self.__K = K
        self.__T = T
        self.__r = r
        self.__sigma = sigma
        self.__option_type = option_type.lower()

    def _d1(self):

        if self.T == 0 or self.sigma == 0:
            return None

        return (
            np.log(self.S / self.K)
            + (self.r + 0.5 * self.sigma**2) * self.T
        ) / (self.sigma * np.sqrt(self.T))

    def _d2(self):

        d1 = self._d1()

        if d1 is None:
            return None

        return d1 - self.sigma * np.sqrt(self.T)

    def price(self):
        """Calculate the Black-Scholes option price."""

        if self.T == 0:
            if self.option_type == "call":
                return max(self.S - self.K, 0)
            return max(self.K - self.S, 0)

        if self.sigma == 0:
            forward_intrinsic = self.S - self.K * np.exp(-self.r * self.T)
            if self.option_type == "call":
                return max(forward_intrinsic, 0)
            return max(-forward_intrinsic, 0)

        d1 = self._d1()
        d2 = self._d2()

        if self.option_type == "call":
            return (
                self.S * norm.cdf(d1)
                - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
            )

        return (
            self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)
            - self.S * norm.cdf(-d1)
        )

    def delta(self):
        """Calculate option delta."""

        if self.T == 0:
            if self.option_type == "call":
                return float(self.S > self.K)
            return -float(self.S < self.K)

        if self.sigma == 0:
            return self._zero_vol_delta()

        d1 = self._d1()

        if self.option_type == "call":
            return norm.cdf(d1)

        return norm.cdf(d1) - 1

    def _zero_vol_delta(self):
        discounted_strike = self.K * np.exp(-self.r * self.T)

        if self.S == discounted_strike:
            return 0.5 if self.option_type == "call" else -0.5

        if self.option_type == "call":
            return float(self.S > discounted_strike)

        return -float(self.S < discounted_strike)

    def gamma(self):
        """Calculate option gamma."""

        if self.T == 0 or self.sigma == 0:
            return 0.0

        d1 = self._d1()

        return norm.pdf(d1) / (
            self.S * self.sigma * np.sqrt(self.T)
        )

    def vega(self):
        """Calculate option vega per 1.00 change in volatility."""

        if self.T == 0 or self.sigma == 0:
            return 0.0

        d1 = self._d1()

        return self.S * norm.pdf(d1) * np.sqrt(self.T)

    def theta(self):
        """Calculate calendar-time theta per year."""

        if self.T == 0:
            return 0.0

        if self.sigma == 0:
            return 0.0

        d1 = self._d1()
        d2 = self._d2()

        first_term = (
            -self.S * norm.pdf(d1) * self.sigma
            / (2 * np.sqrt(self.T))
        )

        if self.option_type == "call":
            return (
                first_term
                - self.r * self.K * np.exp(-self.r * self.T)
                * norm.cdf(d2)
            )

        return (
            first_term
            + self.r * self.K * np.exp(-self.r * self.T)
            * norm.cdf(-d2)
        )

    def rho(self):
        """Calculate option rho per 1.00 change in interest rate."""

        if self.T == 0 or self.sigma == 0:
            return 0.0

        d2 = self._d2()

        if self.option_type == "call":
            return (
                self.K * self.T * np.exp(-self.r * self.T)
                * norm.cdf(d2)
            )

        return (
            -self.K * self.T * np.exp(-self.r * self.T)
            * norm.cdf(-d2)
        )

    def greeks(self):
        """Return all Greeks in a dictionary."""

        return {
            "price": self.price(),
            "delta": self.delta(),
            "gamma": self.gamma(),
            "vega": self.vega(),
            "theta": self.theta(),
            "rho": self.rho()
        }



if __name__ == "__main__":

    # Option parameters
    S = 64.815
    K = 64.815
    T = 0.25
    r = 0.03
    sigma = 0.40

    # Instantiate a European call
    call = EuropeanOption(
        S=S,
        K=K,
        T=T,
        r=r,
        sigma=sigma,
        option_type="call"
    )

    # Display results
    print("European Call Option")
    print("--------------------")
    print(f"Price: {call.price():.4f}")
    print("\nGreeks:")

    for greek, value in call.greeks().items():
        print(f"{greek.capitalize():<10}: {value:.4f}")
