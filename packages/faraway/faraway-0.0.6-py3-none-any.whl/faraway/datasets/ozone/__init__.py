DESCR = """
Ozone in LA in 1976

Description:

     A study the relationship between atmospheric ozone concentration
     and meteorology in the Los Angeles Basin in 1976.  A number of
     cases with missing variables have been removed for simplicity.

Variables:

     A data frame with 330 observations on the following 10 variables.

     ‘O3’ Ozone conc., ppm, at Sandbug AFB.

     ‘vh’ a numeric vector

     ‘wind’ wind speed

     ‘humidity’ a numeric vector

     ‘temp’ temperature

     ‘ibh’ inversion base height

     ‘dpg’ Daggett pressure gradient

     ‘ibt’ a numeric vector

     ‘vis’ visibility

     ‘doy’ day of the year

Source:

     Breiman, L. and J. H. Friedman (1985). Estimating optimal
     transformations for multiple regression and correlation. Journal
     of the American Statistical Association 80, 580-598.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'ozone.csv.bz2')
    return data
