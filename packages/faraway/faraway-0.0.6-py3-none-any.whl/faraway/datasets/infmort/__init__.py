DESCR = """
Infant mortality according to income and region

Description:

     The ‘infmort’ data frame has 105 rows and 4 columns.  The infant
     mortality in regions of the world may be related to per capita
     income and whether oil is exported. The dataset is not recent.

Variables:

     This data frame contains the following columns:

     ‘region’ Region of the world, Africa, Europe, Asia or the Americas

     ‘income’ Per capita annual income in dollars

     ‘mortality’ Infant mortality in deaths per 1000 births

     ‘oil’ Does the country export oil or not?

Source:

     Unknown
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'infmort.csv.bz2')
    return data
