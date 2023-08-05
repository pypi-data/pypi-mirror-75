DESCR = """
Carbon dioxide effects on peanut oil extraction

Description:

     The ‘peanut’ data frame has 16 rows and 6 columns. Carbon dioxide
     effects on peanut oil extraction

Variables:

     This data frame contains the following columns:

     ‘press’ CO2 pressure - two levels low=0, high=1

     ‘temp’ CO2 temperature - two levels low=0, high=1

     ‘moist’ peanut moisture - two levels low=0, high=1

     ‘flow’ CO2 flow rate - two levels low=0, high=1

     ‘size’ peanut particle size - two levels low=0, high=1

     ‘solubility’ the amount of oil that could dissolve in the CO2

Source:

     Kilgo, M (1989) "An Application of Fractional Factorial
     Experimental Designs" Quality Engineering, 1, 45-54
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'peanut.csv.bz2')
    return data
