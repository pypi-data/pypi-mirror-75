DESCR = """
Truck leaf spring experiment

Description:

     Data on an experiment concerning the production of leaf springs
     for trucks.  A 2^{5-1} fractional factorial experiment with 3
     replicates was carried out with objective of recommending
     production settings to achieve a free height as close as possible
     to 8 inches.

Variables:

     A data frame with 48 observations on the following 6 variables.

     ‘B’ furnace temperature - a factor with levels ‘+’ ‘-’

     ‘C’ heating time - a factor with levels ‘+’ ‘-’

     ‘D’ transfer time - a factor with levels ‘+’ ‘-’

     ‘E’ hold-down time - a factor with levels ‘+’ ‘-’

     ‘O’ quench oil temperature - a factor with levels ‘+’ ‘-’

     ‘height’ leaf spring free height in inches

Source:

     J. J. Pignatiello and J. S. Ramberg (1985) Contribution to
     discussion of offline quality control, parameter design and the
     Taguchi method, Journal of Quality Technology, *17* 198-206.

References:

     P. McCullagh and J. Nelder (1989) "Generalized Linear Models"
     Chapman and Hall, 2nd ed.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'truck.csv.bz2')
    return data
