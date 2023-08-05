DESCR = """
Airline passengers

Description

Monthly totals of airline passengers from 1949 to 1951

Usage

data(airpass)
Format

A data frame with 144 observations on the following 2 variables.

pass
number of passengers in thousands

year
the date as a decimal

Details

Well known time series example dataset

Source

Brown, R.G.(1962) Smoothing, Forecasting and Prediction of Discrete Time Series. Englewood Cliffs, N.J.: Prentice-Hall.

References

Box, G.E.P., Jenkins, G.M. and Reinsel, G.C. (1994) Time Series Analysis, Forecasting and Control, 3rd edn. Englewood Cliffs, N.J.: Prentice-Hall.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'air.csv.bz2')
    return data
