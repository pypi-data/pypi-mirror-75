DESCR = """
Treatment and block effects on egg production

Description:

     The ‘composite’ data frame has 12 rows and 3 columns.  Six pullets
     were placed into each of 12 pens. Four blocks were formed from
     groups of 3 pens based on location. Three treatments were applied.
     The number of eggs produced was recorded

Variables:

     This data frame contains the following columns:

     ‘treat’ Three treatments: O, E or F

     ‘block’ Four blocks labeled 1-4

     ‘eggs’ Number of eggs produced

Source:

     Mead, R., R.N. Curnow, and A.M. Hasted. 1993. Statistical Methods
     in Agriculture and Experimental Biology. Chapman and Hall, London,
     p. 64. 1993
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'eggprod.csv.bz2')
    return data
