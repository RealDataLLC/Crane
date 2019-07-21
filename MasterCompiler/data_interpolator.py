import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats.stats import pearsonr
#import matplotlib
#matplotlib.use('TkAgg')
#import matplotlib.pyplot as plt
from typing import List


def line(x, a, b):
    return a * x + b


def poly_2(x, a, b, c):
    return a * x**2 + b * x + c


def poly_3(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d


def logistic(x, a, b, c):
    return a / (1 + b * np.exp(c * x))


def exponential(x, a, b):
    return a * np.exp(b * x)


def interpolate(years: List, values: List, include_raw: bool=True, method: str=None, multiplier: float=1.0,
                shift_adjust: float=1.05981352321757) -> pd.DataFrame:
    """
    :param years: list of years for known values
    :param values: list of known raw values
    :param include_raw: if True, use raw values if available
    :param method: [linear, polynomial 2nd order, polynomial 3rd order, s-curve, exponential]
    default None; specify which curve-fitting method to use
    :param multiplier: default 1.0; multiplier to convert raw values to desired unit. If conversion is more complicated
    than a multiplier, perform interpolation first, then convert output
    :param shift_adjust: for s-curve - constant by which to adjust numerator
    :return:
    """
    # shift_adjust default value comes from Drawdown SolarPVUtility_RRS model. see Sheet Data Interpolator, cell BW21
    start_year = 2005
    end_year = 2060
    base_year = 2014
    curve_options = [line, poly_2, poly_3]
    curve_names = ['linear', 'polynomial 2nd order', 'polynomial 3rd order']
    #removed exponential
    all_years = np.asarray((range(start_year, end_year + 1)))
    years_shifted = np.asarray(years) - base_year
    values_converted = np.asarray(values) * float(multiplier)

    if method in curve_names:
        method_idx = curve_names.index(method)
        func = curve_options[method_idx]
#         if method == 's-curve':
#             # linearize logistic function to constrain curve fit (and be consistent with Drawdown)
#             # note that Drawdown similarly estimates coefficients for the exponential curve by linearizing data,
#             # but I'm choosing to optimize directly with the exponential function because it is more "constrained"
#             # than the logistic function and Python is capable of doing this curve fit
#             a_fixed = max(values_converted) + shift_adjust
#             log_values = np.log(a_fixed / np.asarray(values_converted) - 1)
#             log_popt, pcov = curve_fit(line, years_shifted, log_values)
#             popt = np.array([a_fixed, np.exp(log_popt[1]), log_popt[0]])
#         else:
#             popt, pcov = curve_fit(func, years_shifted, values_converted)
        popt, pcov = curve_fit(func, years_shifted, values_converted)
        func_r2 = pearsonr(values, func(years_shifted, *popt))[0] ** 2
        r2 = func_r2
        #print("Coefficient of determination for {} fit: {}".format(method, func_r2))
        #print("Parameters: {}".format(popt))
        y_interp = func(all_years - base_year, *popt)
        print("other")


    else:
        best_func = None
        best_func_params = None
        r2 = 0
        print("Coefficient of determination:")
        for i, func in enumerate(curve_options):
#             if i == 3:
#                 a_fixed = max(values_converted) + shift_adjust
#                 log_values = np.log(a_fixed / np.asarray(values_converted) - 1)
#                 log_popt, pcov = curve_fit(line, years_shifted, log_values)
#                 popt = np.array([a_fixed, np.exp(log_popt[1]), log_popt[0]])
#             else:
#                 popt, pcov = curve_fit(func, years_shifted, values_converted)
            popt, pcov = curve_fit(func, years_shifted, values_converted)
            func_r2 = pearsonr(values, func(years_shifted, *popt))[0] ** 2
            print('{}: {}'.format(curve_names[i], func_r2))

            if func_r2 > r2:
                r2 = func_r2
                best_func = func
                best_func_name = curve_names[i]                
                best_func_params = popt
        print('Best fit is {} with parameters {}'.format(best_func_name, best_func_params))
        #issue is here
        try:
            y_interp = best_func(all_years-base_year, *best_func_params)
        except TypeError:
            y_interp = best_func(all_years-base_year)
    result = pd.DataFrame(y_interp, index=all_years)

    #plt.plot(result.index, result, 'b-', years, values_converted, 'ko')
    #plt.xlabel('Year')
    #plt.show()

    if include_raw:
        for y_idx, y in enumerate(years):
            result.loc[result.index == y] = values_converted[y_idx]
    result["r2"] = r2
    return result


def main():
    years = [2012, 2020, 2025, 2030, 2040, 2050]
    values = [22604, 27586, 31297, 36867, 51939, 67535]
    test = interpolate(years, values, include_raw=False)
    print(test)


if __name__ == '__main__':
    main()
