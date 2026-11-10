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
      raise ValueError("Strike price must be positve")
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
        ttf_curve : list or array of TTF prices for each delivery day
        rf_rate : float, continuously compounded risk-free interest rate
        T_list : list or array of maturities (T) for each delivery day
        """
        if len(ttf_curve) != len(T_list):
            raise ValueError("The TTF curve and maturities array must have the same length.")
            
        total_value = 0
        for daily_ttf_price, T in zip(ttf_curve, T_list):
            total_value += self.price(daily_ttf_price, rf_rate, T)
            
        return total_value


if __name__ == "__main__":
    # Fixing the different parameters
    K_ATM = 64.815 # EUR/MWh
    qmin = 5.0 # GWh/day
    rf = 0.03  
    
    forward_baseline = Forward(K=K_ATM, qmin=qmin)
    
    # Test with data
    dummy_ttf_curve = [65.0,64.815,66.0]
    dummy_maturities = [1.0,1.0+1/365,1.0+2/365] 
    
    total_val = forward_baseline.valuation(ttf_curve=dummy_ttf_curve, rf_rate=rf, T_list=dummy_maturities
    )
    
    print("Pricing of the Forward")
    print(f"Strike (K)    : {K_ATM} EUR/MWh")
    print(f"Volume (qmin) : {qmin} GWh/day")
    # Correction de la variable ici (rf au lieu de risk_free_rate)
    print(f"Risk-Free Rate: {rf * 100}%")
    print("-" * 38)
    print(f"Total Discounted PV : {total_val:,.2f} EUR")
