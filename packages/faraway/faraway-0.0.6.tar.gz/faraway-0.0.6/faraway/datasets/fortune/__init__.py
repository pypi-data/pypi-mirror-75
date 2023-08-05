DESCR = """
Billionaires' wealth and age

Description:

     Fortune magazine publishes a list of the world's billionaires each
     year. The 1992 list includes 233 individuals. Their wealth, age,
     and geographic location (Asia, Europe, Middle East, United States,
     and Other) are reported.

Variables:

     A data frame with 232 observations on the following 3 variables.

     ‘wealth’ Billions of dollars

     ‘age’ age in years

     ‘region’ a factor with levels ‘A’, Asia, ‘E’, Europe, ‘M’, Middle
          East, ‘O’ Other, ‘U’ USA
Source:
     Fortune magazine
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'fortune.csv.bz2')
    return data
