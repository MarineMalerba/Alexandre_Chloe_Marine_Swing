# Part 1 

## 2. Is it correct to use only the ATM vol? if not why?
No, it is not correct to use only the ATM vol. We use the ATM implied volatility as a simplification, since vols are the most liquid ATM.
First, it assumes there is no skew, as we use ATM vol for all options, even for OTM or ITM options. The thing is, a swing option is a strip of options with different maturities and some of them are ITM (in the data, some days are below 64 EUR/MWh on the curve)and some others OTM and should thus not be priced using ATM vol.
Second, only using one ATM vol means that we are underestimating the short-term volatility—the volatility when it is highest, where the most trades take place.
Third, the model relies on a static correlation based on past data and keeps it fixed, whereas in reality it should be variable.

## 3. TTF is the most liquid hub in europe, how would you use TTF volatility surface to get an implied volatility surface of another hub ?



## 4. Do we need to alter the code to take into Qmin and Qmax if they exist ? How would you alter the code to take into account a Qmin and Qmax ? 

## 5. Price a Put Swing Option using the same methods.
