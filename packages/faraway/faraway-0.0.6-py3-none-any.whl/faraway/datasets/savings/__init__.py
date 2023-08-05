DESCR = """
Savings rates in 50 countries

Description

The savings data frame has 50 rows and 5 columns. The data is averaged over the period 1960-1970.

sr: savings rate - personal saving divided by disposable income

pop15: percent population under age of 15

pop75: percent population over age of 75

dpi: per-capita disposable income in dollars

ddpi: percent growth rate of dpi

Details

Now also appears as LifeCycleSavings in the datasets package

Source

Belsley, D., Kuh. E. and Welsch, R. (1980) "Regression Diagnostics" Wiley.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'savings.csv.bz2')
    return data
