DESCR = """
Butterfat content of milk by breed

Description:

     Average butterfat content (percentages) of milk for random samples
     of twenty cows (ten two-year old and ten mature (greater than four
     years old)) from each of five breeds. The data are from Canadian
     records of pure-bred dairy cattle.

Variables:

     A data frame with 100 observations on the following 3 variables.

     ‘Butterfat’ butter fat content by percentage

     ‘Breed’ a factor with levels ‘Ayrshire’ ‘Canadian’ ‘Guernsey’
          ‘Holstein-Fresian’ ‘Jersey’

     ‘Age’ a factor with levels ‘2year’ ‘Mature’

Source:

     Unknown

Examples:

     data(butterfat)
     ## maybe str(butterfat) ; plot(butterfat) ...
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'butterfat.csv.bz2')
    return data
