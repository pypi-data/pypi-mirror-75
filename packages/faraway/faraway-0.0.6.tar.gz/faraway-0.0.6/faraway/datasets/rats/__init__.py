DESCR = """
Effect of toxic agents on rats

Description:

     An experiment was conducted as part of an investigation to combat
     the effects of certain toxic agents.

Variables:

     A data frame with 48 observations on the following 3 variables.

     ‘time’ survival time in tens of hours

     ‘poison’ the poison type - a factor with levels ‘I’ ‘II’ ‘III’

     ‘treat’ the treatment - a factor with levels ‘A’ ‘B’ ‘C’ ‘D’

Source:

     Box G and Cox D (1964) "An analysis of transformations" J. Roy.
     Stat. Soc. Series B. *26* 211.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'rats.csv.bz2')
    return data
