from .tools import *
from .influence import *
from .quantile import *

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

class PyPlotLm:
    def __init__(self, reg, X, y, intercept=False):
        """ regression analysis for a sklearn linear regression model, reproduction of R summary.lm and plot.lm

            Core functionalities:
            A. generate a R style regression model summary
            B. plot six available diagnostic plots:
                1. Residuals vs Fitted
                2. Normal Q-Q
                3. Scale-Location
                4. Cook's Distance
                5. Residuals vs Leverage
                6. Cook's Distance vs Leverage / (1-Leverage)

        Parameters: reg (sklearn.linear_model) - a fitted sklearn.linear_model or similar, such as lasso, object
                    X (nd-array) - the design matrix
                    y (array) - the response
                    intercept (boo) - if the X data has intercept or not
                                      optional, default is False

        Arributes: X (nd-array) - the design matrix, with intercept
                   y (nd-array) - the raw response
                   fitted_values (array) - fitted values, aka y_hat
                   residuals (array) - raw residuals, i.e y - y_hat
                   resid_max_3 (array) - top max 3 of raw residuals

                   h (array) - leverage
                   p (int) - total numbers of features, including intercept
                   n (int) - total numbers of observations

                   standard_residuals (array) - internally studentized residuals
                   root_standard_residuals (array) - square root of the absolute values of the
                                                     internally studentized residuals

                   theo_quantiles (array) - theorectical quantiles

                   cooks (array) - Cook's Distance
                   cooks_max_3 (array) - top max 3 of Cook's Distance

                   rse (float) - residual standard error
                   se (array) - coefficient standard error
                   coef (array) - regression coefficients
                   t_stat_ (array) - coefficient t-statistics
                   t_p_val (array) - coefficient p-values from t-statistics
                   f_stat_ (float) - regression f-statistic
                   f_p_val (float) - p-value from regression f-statistic
                   r2 (float) - r-squared
                   adj_r2 (float) - adjusted r-squared

        Methods: summary(self) - print model report
                 plot(self, which=None) - plot diagnostic plots
                                          if which is None, will plot plot # 1,2,3,5
                                          a specific plot can be plot separately using the which parameters
                                          or use the below methods
                       - residuals_fitted(self) - plot 1
                       - normal_qq(self) - plot 2
                       - scale_location(self) - plot 3
                       - cooks_distance(self) - plot 4
                       - residual_leverage(self) - plot 5
                       - cooks_leverage(self) - plot 6

        Examples:
        >>> from sklearn.datasets import load_diabetes
        >>> from sklearn.linear_model import LinearRegression
        >>> from pyplotlm import *

        >>> X, y = load_diabetes(return_X_y=True)

        >>> reg = LinearRegression().fit(X, y)

        >>> obj = PyPlotLm(reg, X, y, intercept=False)
        >>> obj.summary()
        Residuals:
               Min        1Q   Median       3Q       Max
         -155.8290  -38.5339  -0.2269  37.8061  151.3550

        Coefficients:
                       Estimate Std. Error     t value   Pr(>|t|)
        (Intercept)   1.521e+02  2.576e+00   5.906e+01        0.0  ***
        X0           -1.001e+01  5.975e+01  -1.676e-01      0.867
        X1           -2.398e+02  6.122e+01  -3.917e+00  0.0001041  ***
        X2            5.198e+02  6.653e+01   7.813e+00  4.308e-14  ***
        X3            3.244e+02  6.542e+01   4.958e+00  1.024e-06  ***
        X4           -7.922e+02  4.167e+02  -1.901e+00    0.05795  .
        X5            4.767e+02  3.390e+02   1.406e+00     0.1604
        X6            1.010e+02  2.125e+02   4.754e-01     0.6347
        X7            1.771e+02  1.615e+02   1.097e+00     0.2735
        X8            7.513e+02  1.719e+02   4.370e+00  1.556e-05  ***
        X9            6.763e+01  6.598e+01   1.025e+00      0.306
        ---
        Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1

        Residual standard error: 54.154 on 431 degrees of freedom
        Multiple R-squared: 0.5177,     Adjusted R-squared: 0.5066
        F-statistic: 4.6e+01 on 10 and 431 DF,  p-value: 1.11e-16
        >>> obj.plot()

        References:
        1. Regression Deletion Diagnostics (R)
        https://stat.ethz.ch/R-manual/R-devel/library/stats/html/influence.measures.html
        https://www.rdocumentation.org/packages/stats/versions/3.6.2/topics/lm
        https://www.rdocumentation.org/packages/stats/versions/3.6.2/topics/plot.lm

        2. Residuals and Influence in Regression
        https://conservancy.umn.edu/handle/11299/37076
        https://en.wikipedia.org/wiki/Leverage_(statistics)
        https://en.wikipedia.org/wiki/Studentized_residual

        3. Cook's Distance
        https://en.wikipedia.org/wiki/Cook%27s_distance
        """

        if not isinstance(X, np.ndarray):
            raise TypeError('input design matrix must be a numpy array object')

        if X.shape[0] != len(y):
            raise DimensionError('X dimension must match with y dimension')

        self.reg = reg

        # total number of observations
        self.n = X.shape[0]

        # define self.X
        if intercept:
            self.X = X

        else:
            self.X = np.concatenate([np.ones(self.n).reshape(-1,1), X], 1)

        # total dimension, including intercept
        self.p = self.X.shape[-1]

        self.y = np.array(y)

        # fitted values from model
        self.fitted_values = self.reg.predict(X)
        # raw residuals from model
        self.residuals = self.y - self.fitted_values

        # top 3 max residuals
        self.resid_max_3 = np.argsort(abs(self.residuals))[::-1][:3]

        # leverage
        self.h = leverage(self.X)

        # studentized residuals
        self.standard_residuals = internally_studentized(self.residuals, self.h, self.p, self.n)

        # square root of absolute studentized residuals
        self.root_standard_residuals = np.sqrt(abs(self.standard_residuals))

        # theorectical quantiles
        self.theo_quantiles = theorectical_quantiles(self.standard_residuals)

        # Cook's Distance
        self.cooks = cooks_distance(self.standard_residuals, self.h, self.p)
        self.cooks_max_3 = np.argsort(self.cooks)[::-1][:3]

        #################### coefficient tests ####################

        # residual standard error
        self.rse = np.sqrt(np.dot(self.residuals.T, self.residuals) / (self.n-self.p))

        # t-test
        # coefficient standard errors
        self.se = coef_standard_error(self.residuals, self.X)

        self.coef = np.append(self.reg.intercept_, self.reg.coef_)

        # t-statistics
        self.t_stat_ = self.coef / self.se
        # t p-values
        self.t_p_val = 2 * (1 - stats.t.cdf(np.abs(self.t_stat_), self.n-self.p))

        # f-test
        # f-statistics
        self.f_stat_ = f_stat(self.residuals, self.fitted_values, self.y, self.p)
        # f p-values
        self.f_p_val = 1-stats.f.cdf(self.f_stat_, self.p-1, self.n-self.p)

        # r-squared & adjusted r-squared
        self.r2, self.adj_r2 = r_squared(self.y, self.residuals, self.p)

    def plot(self, which=None, size=(12,10)):
        """ by default this method plots the most common 4 plots, which are 1, 2, 3 and 5
            i.e.
            1. Residuals vs Fitted
            2. Normal Q-Q
            3. Scale-Location
            5. Residuals vs Leverage

        4. Cook's Distance and 6. Cook's Distance vs Leverage plot aren't as common, so we will exclude from default
        But, we can create these plots by using the 'which' parameters

        Parameters: which (int) - by default, it will plot the most common 4 plots, if 'which' is specified, it will create the specified plot
                    size (tuple) - the size for the 2x2 default plots
        """
        if which is not None:
            if which == 1:
                self.residuals_fitted()
            elif which == 2:
                self.normal_qq()
            elif which == 3:
                self.scale_location()
            elif which == 4:
                self.cooks_distance()
            elif which == 5:
                self.residual_leverage()
            elif which == 6:
                self.cooks_leverage()

        else:
            plt.figure(figsize=size)
            plt.subplots_adjust(hspace=0.3)

            plt.subplot(221)
            self.residuals_fitted()

            plt.subplot(222)
            self.normal_qq()

            plt.subplot(223)
            self.scale_location()

            plt.subplot(224)
            self.residual_leverage()

    def residuals_fitted(self):
        """ plot 1. Residuals vs Fitted
        """
        sns.residplot(self.fitted_values, self.residuals,
              lowess=True,
              scatter_kws={'alpha': 0.5},
              line_kws={'color': 'red', 'lw': 1})

        for i in self.resid_max_3:
            plt.annotate(i, xy=(self.fitted_values[i], self.residuals[i]))

        plt.title('Residuals vs Fitted', size=20)
        plt.xlabel('Fitted values', size=15)
        plt.ylabel('Residuals', size=15)

    def normal_qq(self):
        """ plot 2. Normal Q-Q
        """
        sns.regplot(self.theo_quantiles, sorted(self.standard_residuals),
            lowess=True,
            scatter_kws={'alpha': 0.5},
            line_kws={'color': 'red', 'lw': 1})

        pos_idx = 0
        neg_idx = 0
        for i in self.resid_max_3:
            if self.standard_residuals[i] < 0:
                plt.annotate(i, xy=[self.theo_quantiles[neg_idx], sorted(self.standard_residuals)[neg_idx]])
                neg_idx += 1
            else:
                pos_idx += -1
                plt.annotate(i, xy=[self.theo_quantiles[pos_idx], sorted(self.standard_residuals)[pos_idx]])

                plt.title('Normal Q-Q', size=20)
                plt.xlabel('Theoretical Quantiles', size=15)
                plt.ylabel('Standardized residuals', size=15)

    def scale_location(self):
        """ plot 3. Scale-Location
        """
        sns.regplot(self.fitted_values, self.root_standard_residuals,
            lowess=True,
            scatter_kws={'alpha': 0.5},
            line_kws={'color': 'red', 'lw': 1})

        for i in self.resid_max_3:
            plt.annotate(i, xy=[self.fitted_values[i], self.root_standard_residuals[i]])

        plt.title('Scale-Location', size=20)
        plt.xlabel('Fitted values', size=15)
        plt.ylabel('$\sqrt{|Standardized residuals|}$', size=15)

    def cooks_distance(self):
        """ plot 4. Cook's Distance
        """
        plt.bar(range(len(self.cooks)), self.cooks)

        # cook's distance max 3 annotation
        for i in self.cooks_max_3:
            plt.annotate(i, xy=[i, self.cooks[i]])

        plt.title("Cook's distance", size=20)
        plt.xlabel('Obs. number', size=15)
        plt.ylabel("Cook's distance", size=15)

    def residual_leverage(self):
        """ plot 5. Residuals vs Leverage
        """
        min_y = min(self.standard_residuals) + min(self.standard_residuals)*0.15
        max_y = max(self.standard_residuals) + max(self.standard_residuals)*0.15

        # define cook's distance components
        cooks_x = np.linspace(min(self.h), max(self.h), 50)
        cooks_y_1 = np.sqrt((self.p*(1-cooks_x)) / cooks_x)

        cooks_y_05_ = np.sqrt(0.5*(self.p*(1-cooks_x)) / cooks_x)

        cooks_y_1_neg = -np.sqrt((self.p*(1-cooks_x)) / cooks_x)
        cooks_y_05_neg = -np.sqrt(0.5*(self.p*(1-cooks_x)) / cooks_x)

        # main plot
        sns.regplot(self.h, self.standard_residuals,
            lowess=True,
            scatter_kws={'alpha': 0.5},
            line_kws={'color': 'red', 'lw': 1})

        for i in self.cooks_max_3:
            plt.annotate(i, xy=[self.h[i], self.standard_residuals[i]])

        # plot cook's distance
        if any(cooks_y_1 < max_y):
            plt.plot(cooks_x, cooks_y_1, ls = ':', color = 'r', label="Cooks's distance")

            for i in [cooks_y_1[-1], cooks_y_1_neg[-1]]:
                plt.annotate(1, xy=[cooks_x[-1], i], color='red')

            plt.legend(frameon=False)

        if any(cooks_y_05_ < max_y):
            plt.plot(cooks_x, cooks_y_05_, ls = ':', color = 'r')

            for i in [cooks_y_05_[-1], cooks_y_05_neg[-1]]:
                plt.annotate(0.5, xy=[cooks_x[-1], i], color='red')

        if any(cooks_y_1_neg > min_y):
            plt.plot(cooks_x, cooks_y_1_neg, ls = ':', color = 'r')

            for i in [cooks_y_1_neg[-1], cooks_y_05_neg[-1]]:
                plt.annotate(1, xy=[cooks_x[-1], i], color='red')

        if any(cooks_y_05_neg > min_y):
            plt.plot(cooks_x, cooks_y_05_neg, ls = ':', color = 'r')

            for i in [cooks_y_05_neg[-1], cooks_y_05_neg[-1]]:
                plt.annotate(1, xy=[cooks_x[-1], i], color='red')

        plt.ylim(min_y, max_y)

        plt.title('Residuals vs Leverage', size=20)
        plt.xlabel('Leverage', size=15)
        plt.ylabel('Standardized residuals', size=15)

    def cooks_leverage(self):
        """ plot 6. Cook's Distance vs Leverage
        """
        # define contour lines values
        h_ = self.h/(1-self.h)
        max_x = max(h_) + max(h_)*0.05
        max_y = max(self.cooks) + max(self.cooks)*0.05

        bval = [round(i*2) / 2 for i in np.linspace(0, max(self.standard_residuals), 5)]

        sns.regplot(h_, self.cooks,
                    lowess=True,
                    scatter_kws={'alpha': 0.5},
                    line_kws={'color': 'red', 'lw': 1})

        for i in self.cooks_max_3:
            plt.annotate(i, xy=[h_[i], self.cooks[i]])

        for i in bval:
            bi2 = i**2
            if max_y > bi2*max_x:
                xi = max_x + 0.00035
                yi = bi2*xi
                abline(0, bi2, x_max=max_x)
                plt.annotate(i, xy=[xi, yi])
            else:
                yi = max_y - 1.5*0.002
                xi = yi / bi2
                plt.plot([0, xi], [0, yi], ':', color='black')
                plt.annotate(i, xy=[xi, max_y-max_y*0.05])

        plt.title("Cook's dist vs Leverage $h_{ii}/(1-h_{ii})$", size=20)
        plt.xlabel('Leverage $h_{ii}$', size=15)
        plt.ylabel("Cook's distance", size=15)

    def summary(self):
        """ print model report, similar to R summary.lm
        """
        # residual quantiles
        resid_quantiles = np.array([format(i, '.4f') for i in np.quantile(self.residuals, [0, 0.25, 0.5, 0.75, 1])])
        resid_quantiles_df = pd.DataFrame(resid_quantiles.reshape(1,-1), columns=['Min','1Q','Median', '3Q', 'Max'])

        # coefficients
        clean_coef = [format(i, '.4f') for i in self.coef]
        clean_std_e = [format(i, '.4f') for i in self.se]
        clean_t_stat = [format(i, '.4f') for i in self.t_stat_]
        clean_t_p = [format(i, '.4f') for i in self.t_p_val]
        p_sign = ['***' if i <= 0.001 else '** ' if i <= 0.01 else '*  ' if i <= 0.05 else '.  ' if i <= 0.1 else '' for i in self.t_p_val]

        t_dict = {'Estimate':clean_coef, 'Std. Error': clean_std_e, 't value': clean_t_stat, 'Pr(>|t|)':clean_t_p, '':p_sign}
        t_df = pd.DataFrame(t_dict, index=['(Intercept)']+[f'X{i}' for i in range(self.p-1)])

        # residual standard error
        clean_rse = format(self.rse, '.3f')

        # r2 & adj r2
        clean_r2 = format(self.r2, '.4f')
        clean_adj_r2 = format(self.adj_r2, '.4f')

        # f
        clean_f_stat = format(self.f_stat_, '.2f')
        clean_f_p = format(self.f_p_val, '.2e')

        # print
        print('Residuals:')
        print(resid_quantiles_df.to_string(index=False))
        print()
        print('Coefficients:')
        print(t_df.to_string())
        print('---')
        print("Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1")
        print()
        print(f'Residual standard error: {clean_rse} on {self.n-self.p} degrees of freedom')
        print(f'Multiple R-squared: {clean_r2},     Adjusted R-squared: {clean_adj_r2}')
        print(f'F-statistic: {clean_f_stat} on {self.p-1} and {self.n-self.p} DF,  p-value: {clean_f_p}')

def summary(obj):
    """ generate summary from a PyPlotLm.pyplotlm object
    """
    obj.summary()

def plot(obj, which=None):
    """ plot diagnostic plots from a PyPlotLm.pyplotlm object
    """
    obj.plot(which=which)
