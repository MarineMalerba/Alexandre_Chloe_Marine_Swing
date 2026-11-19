import numpy as np
from forward import Forward
from european_options import EuropeanOption

class Swing_Option:
  """
  We define a method to price lower bound call swing options, options that we can define as "take or pay options".
  We use the Keppo method here.
  option_type = "call": the holder buys gas at K (long forward on qmin + strip of calls on qmax - qmin)
  option_type = "put" : the holder sells gas at K (short forward on qmin + strip of puts on qmax - qmin)
  """
  def __init__(self, K, qmin, qmax, Qn, option_type="call"):
        if option_type.lower() not in ["call", "put"]:
            raise ValueError("option_type must be 'call' or 'put'.")
        self.option_type = option_type.lower()
        self.K = K
        self.qmin = qmin
        self.qmax = qmax
        self.Qn = Qn
        # The daily flexibility, the volume that we are allowed to buy additionally every day
        self.add_daily_limit = qmax - qmin

  def valuation(self, ttf_curve, rf_rate, T_list, sigma):
        nb_days = len(ttf_curve)
        
        # We compute the guaranteed qmin volume given by the forwards
        fw = Forward(self.K, self.qmin)
        baseline_pv = fw.valuation(ttf_curve, rf_rate, T_list)
        # For a put swing the mandatory qmin volume is sold at K, so we are short the forward: (K - F) * qmin
        if self.option_type == "put":
            baseline_pv = -baseline_pv
        
        # Then check how much flexibility volume we have left after having taken into account qmin
        total_mandatory_vol = self.qmin * nb_days
        flex_vol_left = self.Qn - total_mandatory_vol
        
        if flex_vol_left < 0:
            raise ValueError("Qn is too small to cover the qmin volume ")

        # Calculate daily call option prices
        # We store them in a list of tuples (call_price, day_index)
        daily_calls = []
        for i in range(nb_days):
            daily_price = ttf_curve[i]
            
            maturity_date = T_list[i]
            maturity = len(T_list[:i])/365
            
            # We instantiate the option for that specific day
            opt = EuropeanOption(S=daily_price, K=self.K, T=maturity, r=rf_rate, sigma=sigma, option_type=self.option_type)
            # Append the price and the index 'i' to remember which day it was
            daily_calls.append((opt.price(), i))
            
        # We sort the days to prioritize the ones where exercising the option gives the highest payoff
        daily_calls.sort(reverse=True, key=lambda x: x[0])
        
        # Initialize the total present value of the flexibility to 0 and will accumulate the payoff of the options exercised on the best days
        flex_pv = 0
        
        for i in range(len(daily_calls)):
            c_price = daily_calls[i][0]
            
            if flex_vol_left <= 0:
                break # We used all our global volume available, stop the loop
                
            # To decide how much volume we exercise on this day
            if flex_vol_left >= self.add_daily_limit:
                vol_to_exercise = self.add_daily_limit
            else:
                vol_to_exercise = flex_vol_left
                
            # Update the remaining total volume after the exercise
            flex_vol_left -= vol_to_exercise
            
            # Convert GWh to MWh and add to total flex PV
            flex_pv += c_price * (vol_to_exercise * 1000)
            
        # Keppo Lower Bound formula, the final lower bound value is the sum of the mandatory baseline forwards and the flexibility
        total_swing_pv = baseline_pv + flex_pv
        
        return total_swing_pv, baseline_pv, flex_pv

if __name__ == "__main__":
    K_ATM = 64.815 # EUR/MWh
    qmin = 5.0 # GWh
    qmax = 50.0 # GWh
    Qn = 600.0 # GWh
    IV_ATM = 0.40
    rf = 0.03
    
    swing_pricer = Swing_Option(K_ATM, qmin, qmax, Qn)
  
    # Dummy data to test the code
    sample_curve = [60.0, 70.0, 64.815, 80.0, 55.0]
    sample_maturities = [1/365, 2/365, 3/365, 4/365, 5/365] 
    #Final Pricing
    total_val, base_val, flex_val = swing_pricer.valuation(sample_curve, rf, sample_maturities, IV_ATM)
    
    print("Test swing call")
    print("total:", total_val)
    print("base:", base_val)
    print("flex:", flex_val)

    # Put swing: same Keppo method, short forward on qmin + strip of puts on (qmax - qmin)
    put_pricer = Swing_Option(K_ATM, qmin, qmax, Qn, option_type="put")
    total_put, base_put, flex_put = put_pricer.valuation(sample_curve, rf, sample_maturities, IV_ATM)

    print("Test swing put")
    print("total:", total_put)
    print("base:", base_put)
    print("flex:", flex_put)
