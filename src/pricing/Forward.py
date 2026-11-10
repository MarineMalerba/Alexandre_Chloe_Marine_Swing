import numpy as np

class Forward:
    """
    Class to price the forward components, under the condition that the forwards should verify the minimum baseline requirements

    Parameters:
    K= float, represents the strike price of the forward contract At The Money (ATM)
    qmin= float, daily mandatory volume (in GWh)
    """
    def __init__(self,K,qmin):
        if K<0:
            raise ValueError("Strike price must be positive")
        if qmin<0:
            raise ValueError("qmin volume must be a positive value")
        self.__strike=K
        #Volume in still in GWh, conversion in MWh
        self.__volume_mwh=qmin*1000

    def daily_payoff(self, daily_ttf_price):
        """
        Compute the daily payoff of the forward at maturity, not discounted, using the forward market prices of the TTF curve (also daily).
        Parameters:
        daily_ttf_price : float, curve price for the delivery day (in EUR/MWh)
        """
        if daily_ttf_price < 0:
            raise ValueError("The daily TTF price cannot be negative.") 
        return (daily_ttf_price - self.__strike) * self.__volume_mwh

    def price(self, daily_ttf_price, rf_rate, T):
        """
        Calculate the discounted Present Value of the forward contract for a specific day.
        Parameters:
        daily_ttf_price : float, curve price for the delivery day (in EUR/MWh)
        rf_rate : float, continuously compounded risk-free interest rate
        T : float, time to maturity in years
        """
        payoff = self.daily_payoff(daily_ttf_price)
        discount_factor = np.exp(-rf_rate * T)
        
        return payoff * discount_factor

    def valuation(self, ttf_curve, rf_rate, T_list):
        """
        Calculate the discounted value of the minimum baseline over the entire period.
        
        Parameters:
        ttf_curve : list, TTF prices regrouped for each delivery day
        rf_rate : float, continuously compounded risk-free interest rate
        T_list : list or array of maturities T for each delivery day
        """
        if len(ttf_curve) != len(T_list):
            raise ValueError("The TTF curve and maturities array must have the same length/size.")
        total_value = 0
        for i in range(len(ttf_curve)):
            # Get the price and maturity both at position i
            daily_price = ttf_curve[i]
            maturity_date = T_list[i]
            maturity = len(T_list[:i])/365
            total_value += self.price(daily_price, rf_rate, maturity)
        return total_value

if __name__ == "__main__":
    #Fixing the different parameters
    K_ATM = 64.815
    qmin = 5.0
    # arbitrary rf number to test the code
    rf = 0.04 
    
    fw_test = Forward(K_ATM, qmin)
    
    # Define random data to check the code
    sample_prices = [60.0, 65.0, 70.0]
    sample_maturities = [1/365, 2/365, 3/365] 
    
    result = fw_test.valuation(sample_prices, rf, sample_maturities)
    
    print("Test Forward price:")
    print(f"K: {K_ATM}, qmin: {qmin}, rf: {rf}")
    print("Total PV =", result)
