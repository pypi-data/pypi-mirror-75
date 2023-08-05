DESCR = """
resitivity of wafer in semiconductor experiment

Description:

     A full factorial experiment with four two-level predictors.

Variables:

     A data frame with 16 observations on the following 5 variables.

     x1 a factor with levels ‘-’ ‘+’

     x2 a factor with levels ‘-’ ‘+’

     x3 a factor with levels ‘-’ ‘+’

     x4 a factor with levels ‘-’ ‘+’

     resist Resistivity of the wafer

Source:

     Myers, R. and Montgomery D. (1997) A tutorial on generalized
     linear models, Journal of Quality Technology, 29, 274-291.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'wafer.csv.bz2')
    return data
