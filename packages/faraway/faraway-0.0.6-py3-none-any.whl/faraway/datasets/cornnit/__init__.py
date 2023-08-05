DESCR = """
Corn yields from nitrogen application

Description:

     The relationship between corn yield (bushels per acre) and
     nitrogen (pounds per acre) fertilizer application were studied in
     Wisconsin.

Variables:

     A data frame with 44 observations on the following 2 variables.

     yield corn yield in bushels per acre

     nitrogen pounds per acre

Source:

     Unknown
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'cornnit.csv.bz2')
    return data
