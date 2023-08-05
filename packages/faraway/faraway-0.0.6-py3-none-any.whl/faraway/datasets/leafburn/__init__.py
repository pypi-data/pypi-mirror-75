DESCR = """
Data on the burning time of samples of tobacco leaves


A data frame with 30 observations on the following 4 variables.

nitrogen: nitrogen content by percentage weight

chlorine: chlorine content by percentage weight

potassium: potassium content by percentage weight

burntime: burn time in seconds

Source

Steel, R. G. D. and Torrie, J. H. (1980), Principles and Procedures of Statistics, Second Edition, New York: McGraw-Hill
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'leafburn.csv.bz2')
    return data
