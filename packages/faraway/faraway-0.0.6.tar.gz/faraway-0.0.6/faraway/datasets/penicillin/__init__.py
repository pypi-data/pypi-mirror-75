DESCR = """
Penicillin yield by block and treatment

Description:

     The production of penicillin uses a raw material, corn steep
     liquor, is quite variable and can only be made in blends
     sufficient for four runs. There are four processes, A, B, C and D,
     for the production.

Variables:

     A data frame with 20 observations on the following 3 variables.

     ‘treat’ a factor with levels ‘A’ ‘B’ ‘C’ ‘D’

     ‘blend’ a factor with levels ‘Blend1’ ‘Blend2’ ‘Blend3’ ‘Blend4’
          ‘Blend5’

     ‘yield’ a numeric vector

Source:

     Box, G., W. Hunter, and J. Hunter (1978). Statistics for
     Experimenters. New York: Wiley.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'penicillin.csv.bz2')
    return data
