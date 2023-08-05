DESCR = """
Star temperatures and light intensites

Description

Data on the log of the surface temperature and the log of the light intensity of 47 stars in the star cluster CYG OB1, which is in the direction of Cygnus,

A data frame with 47 observations on the following 3 variables.

index: a numeric vector

temp: temperature

light: light intensity

Source

Rousseeuw, P. and A. Leroy (1987). Robust Regression and Outlier Detection. New York: Wiley.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'star.csv.bz2')
    return data
