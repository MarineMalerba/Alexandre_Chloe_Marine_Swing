# Part 1 

## 2. Is it correct to use only the ATM vol? if not why?
No, it is not correct to use only the ATM vol. We use the ATM implied volatility as a simplification, since vols are the most liquid ATM.
First, it assumes there is no skew, as we use ATM vol for all options, even for OTM or ITM options. The thing is, a swing option is a strip of options with different maturities and some of them are ITM (in the data, some days are below 64 EUR/MWh on the curve)and some others OTM and should thus not be priced using ATM vol.
Second, only using one ATM vol means that we are underestimating the short-term volatility, precisely when it is highest and where the largest number of trades take place.
Third, the model relies on a static correlation based on past data and keeps it fixed, whereas in reality it should be variable.

## 3. TTF is the most liquid hub in europe, how would you use TTF volatility surface to get an implied volatility surface of another hub ?
Since TTF is the most liquid hub in Europe, we can use its volatility surface to reproduce the implied volatility surface of a less liquid hub (just like we used Germany's volatility surface to build France's in the course).
First, we need to compare the historical volatilities of TTF and the target hub month by month across the different maturities. Since there is usually more volatility on the short term, we use historical data on the front month to estimate the short-term part of the curve.
Then, we determine the 50 delta (ATM) volatilities for the target hub, as ATM options are the most liquid. To get the rest of the smile (OTM/ITM strikes), we compute the ratio of OTM and ITM volatilities relative to the ATM volatility on TTF, and apply those same ratios to the target hub's vols.
However, we still have to keep in mind the limits mentionned in question 2.

## 4. Do we need to alter the code to take into Qmin and Qmax if they exist ? How would you alter the code to take into account a Qmin and Qmax ? 

## 5. Price a Put Swing Option using the same methods.
