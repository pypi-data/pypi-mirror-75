# pyplotlm - R style linear regression summary and diagnostic plots for sklearn
This package is a reproduction of the `summary.lm` and `plot.lm` function in R but for a python environment and is meant to support the sklearn library by adding model summary and diagnostic plots for linear regression.
In the R environment, we can fit a linear model and generate a model summary and diagnostic plots by doing the following: <br>
```
> fit = lm(y ~ ., data=data)

> summary(fit)


Call:
lm(formula = y ~ ., data = data)

Residuals:
     Min       1Q   Median       3Q      Max
-155.829  -38.534   -0.227   37.806  151.355

Coefficients:
            Estimate Std. Error t value Pr(>|t|)    
(Intercept)  152.133      2.576  59.061  < 2e-16 ***
X0           -10.012     59.749  -0.168 0.867000    
X1          -239.819     61.222  -3.917 0.000104 ***
X2           519.840     66.534   7.813 4.30e-14 ***
X3           324.390     65.422   4.958 1.02e-06 ***
X4          -792.184    416.684  -1.901 0.057947 .  
X5           476.746    339.035   1.406 0.160389    
X6           101.045    212.533   0.475 0.634721    
X7           177.064    161.476   1.097 0.273456    
X8           751.279    171.902   4.370 1.56e-05 ***
X9            67.625     65.984   1.025 0.305998    
---
Signif. codes:  0 ‘***’ 0.001 ‘**’ 0.01 ‘*’ 0.05 ‘.’ 0.1 ‘ ’ 1

Residual standard error: 54.15 on 431 degrees of freedom
Multiple R-squared:  0.5177,	Adjusted R-squared:  0.5066
F-statistic: 46.27 on 10 and 431 DF,  p-value: < 2.2e-16

> par(mfrow=c(2,2))
> plot(fit)
```
![](https://github.com/esmondhkchu/pyplotlm/blob/dev/plots/R_plot.png) <br>
The goal of this package is to make this process as simple as it is in R for a sklearn LinearRegression object.

## Install
```bash
pip install pyplotlm
```

## Introduction
There are two core functionalities:

A. generate a R style regression model summary (R summary.lm) <br>

B. plot six available diagnostic plots (R plot.lm): <br>
    1. Residuals vs Fitted <br>
    2. Normal Q-Q <br>
    3. Scale-Location <br>
    4. Cook's Distance <br>
    5. Residuals vs Leverage <br>
    6. Cook's Distance vs Leverage / (1-Leverage) <br>

## Usage
Below is how you would produce the summary and diagnostic plots in Python:
```
>>> from sklearn.datasets import load_diabetes
>>> from sklearn.linear_model import LinearRegression
>>> import matplotlib.pyplot as plt
>>> from pyplotlm import *

>>> X, y = load_diabetes(return_X_y=True)

>>> reg = LinearRegression().fit(X, y)

>>> obj = PyPlotLm(reg, X, y, intercept=False)
>>> obj.summary() # or summary(obj)
Residuals:
       Min        1Q   Median       3Q       Max
 -155.8290  -38.5339  -0.2269  37.8061  151.3550

Coefficients:
              Estimate Std. Error  t value Pr(>|t|)     
(Intercept)   152.1335     2.5759  59.0614   0.0000  ***
X0            -10.0122    59.7492  -0.1676   0.8670     
X1           -239.8191    61.2223  -3.9172   0.0001  ***
X2            519.8398    66.5336   7.8132   0.0000  ***
X3            324.3904    65.4219   4.9584   0.0000  ***
X4           -792.1842   416.6839  -1.9012   0.0579  .  
X5            476.7458   339.0345   1.4062   0.1604     
X6            101.0446   212.5326   0.4754   0.6347     
X7            177.0642   161.4756   1.0965   0.2735     
X8            751.2793   171.9020   4.3704   0.0000  ***
X9             67.6254    65.9842   1.0249   0.3060     
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

Residual standard error: 54.154 on 431 degrees of freedom
Multiple R-squared: 0.5177,     Adjusted R-squared: 0.5066
F-statistic: 46.27 on 10 and 431 DF,  p-value: 1.11e-16

>>> obj.plot() or plot(obj)
>>> plt.show()
```
This will produce the same set of diagnostic plots: <br>
![](https://github.com/esmondhkchu/pyplotlm/blob/dev/plots/python_plot.png) <br>

## References:
1. Regression Deletion Diagnostics (R) <br>
https://stat.ethz.ch/R-manual/R-devel/library/stats/html/influence.measures.html <br>
https://www.rdocumentation.org/packages/stats/versions/3.6.2/topics/lm <br>
https://www.rdocumentation.org/packages/stats/versions/3.6.2/topics/plot.lm <br>

2. Residuals and Influence in Regression <br>
https://conservancy.umn.edu/handle/11299/37076 <br>
https://en.wikipedia.org/wiki/Leverage_(statistics) <br>
https://en.wikipedia.org/wiki/Studentized_residual <br>

3. Cook's Distance <br>
https://en.wikipedia.org/wiki/Cook%27s_distance <br>
