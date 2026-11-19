# Part 1 

## 2. Is it correct to use only the ATM vol? if not why?
This is incorrect for multiple reasons. 
First, it assumes there is no skew as we use ATM vol for all options. The thing is, a swing option is a strip of options with different maturities and some of them are ITM (in the data, some days are below 64 EUR/MWh on the curve)and some others OTM and should thus not be priced using ATM vol.
Also, we are using one vol but the vol should differ with the maturity of the options from the strip.

## 3. TTF is the most liquid hub in europe, how would you use TTF volatility surface to get an implied volatility surface of another hub ?

## 4. Do we need to alter the code to take into Qmin and Qmax if they exist ? How would you alter the code to take into account a Qmin and Qmax ? 

## 5. Price a Put Swing Option using the same methods.