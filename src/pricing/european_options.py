
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

    def __d1(self):

        if self.__T == 0 or self.__sigma == 0:
            return None

        return (
            np.log(self.__S / self.__K)
            + (self.__r + 0.5 * self.__sigma**2) * self.__T
        ) / (self.__sigma * np.sqrt(self.__T))

    def __d2(self):

        d1 = self.__d1()

        if d1 is None:
            return None

        return d1 - self.__sigma * np.sqrt(self.__T)

    def price(self):
        """Calculate the Black-Scholes option price."""

        if self.__T == 0:
            if self.__option_type == "call":
                return max(self.__S - self.__K, 0)
            return max(self.__K - self.__S, 0)

        if self.__sigma == 0:
            discounted_strike = self.__K * np.exp(-self.__r * self.__T)
            intrinsic = self.__S - discounted_strike

            if self.__option_type == "call":
                return max(intrinsic, 0)

            return max(-intrinsic, 0)

        d1 = self.__d1()
        d2 = self.__d2()

        if self.__option_type == "call":
            return (
                self.__S * norm.cdf(d1)
                - self.__K * np.exp(-self.__r * self.__T) * norm.cdf(d2)
            )

        return (
            self.__K * np.exp(-self.__r * self.__T) * norm.cdf(-d2)
            - self.__S * norm.cdf(-d1)
        )

    def delta(self):
        """Calculate option delta."""

        if self.__T == 0:
            if self.__option_type == "call":
                return float(self.__S > self.__K)
            return -float(self.__S < self.__K)

        if self.__sigma == 0:
            discounted_strike = self.__K * np.exp(-self.__r * self.__T)

            if self.__S == discounted_strike:
                return 0.5 if self.__option_type == "call" else -0.5

            if self.__option_type == "call":
                return float(self.__S > discounted_strike)

            return -float(self.__S < discounted_strike)

        d1 = self.__d1()

        if self.__option_type == "call":
            return norm.cdf(d1)

        return norm.cdf(d1) - 1

    def gamma(self):
        """Calculate option gamma."""

        if self.__T == 0 or self.__sigma == 0:
            return 0.0

        d1 = self.__d1()

        return norm.pdf(d1) / (
            self.__S * self.__sigma * np.sqrt(self.__T)
        )

    def vega(self):
        """Calculate option vega."""

        if self.__T == 0 or self.__sigma == 0:
            return 0.0

        d1 = self.__d1()

        return self.__S * norm.pdf(d1) * np.sqrt(self.__T)

    def theta(self):
        """Calculate calendar-time theta per year."""

        if self.__T == 0 or self.__sigma == 0:
            return 0.0

        d1 = self.__d1()
        d2 = self.__d2()

        first_term = (
            -self.__S * norm.pdf(d1) * self.__sigma
            / (2 * np.sqrt(self.__T))
        )

        if self.__option_type == "call":
            return (
                first_term
                - self.__r * self.__K * np.exp(-self.__r * self.__T)
                * norm.cdf(d2)
            )

        return (
            first_term
            + self.__r * self.__K * np.exp(-self.__r * self.__T)
            * norm.cdf(-d2)
        )

    def rho(self):
        """Calculate option rho."""

        if self.__T == 0 or self.__sigma == 0:
            return 0.0

        d2 = self.__d2()

        if self.__option_type == "call":
            return (
                self.__K * self.__T * np.exp(-self.__r * self.__T)
                * norm.cdf(d2)
            )

        return (
            -self.__K * self.__T * np.exp(-self.__r * self.__T)
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

    # Create a European call option
    call = EuropeanOption(
        S=S,
        K=K,
        T=T,
        r=r,
        sigma=sigma,
        option_type="call"
    )

    # Display results
    print("EUROPEAN CALL OPTION")
    print("--------------------")

    for greek, value in call.greeks().items():
        print(f"{greek.capitalize():<10}: {value:.6f}")


