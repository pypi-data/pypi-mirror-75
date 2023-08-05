DESCR = """
Snail production

Description:

     A study was conducted to optimize snail production for
     consumption. The percentage water content of the tissues of snails
     grown under three different levels of relative humidity and two
     different temperatures was recorded. For each combination, 4
     snails were observed.

Variables:

     A data frame with 24 observations on the following 3 variables.

     ‘water’ percentage water content

     ‘temp’ temperature in C

     ‘humid’ relative humidity

Source:

     Unknown
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'snail.csv.bz2')
    return data
