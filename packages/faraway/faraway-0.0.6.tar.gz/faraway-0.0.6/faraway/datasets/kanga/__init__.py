DESCR = """
Kangaroo skull measurements

Description:

     Sex and species of an specimens of kangaroo.

Variables:

     A data frame with 148 observations on the following 20 variables.

     ‘species’ a factor with levels ‘fuliginosus’ ‘giganteus’
          ‘melanops’

     ‘sex’ a factor with levels ‘Female’ ‘Male’

     ‘basilar.length’ a numeric vector

     ‘occipitonasal.length’ a numeric vector

     ‘palate.length’ a numeric vector

     ‘palate.width’ a numeric vector

     ‘nasal.length’ a numeric vector

     ‘nasal.width’ a numeric vector

     ‘squamosal.depth’ a numeric vector

     ‘lacrymal.width’ a numeric vector

     ‘zygomatic.width’ a numeric vector

     ‘orbital.width’ a numeric vector

     ‘.rostral.width’ a numeric vector

     ‘occipital.depth’ a numeric vector

     ‘crest.width’ a numeric vector

     ‘foramina.length’ a numeric vector

     ‘mandible.length’ a numeric vector

     ‘mandible.width’ a numeric vector

     ‘mandible.depth’ a numeric vector

     ‘ramus.height’ a numeric vector

Source:

     Andrews and Herzberg (1985) Chapter 53.

References:

     Andrews, D. F. and Herzberg, A. M. (1985). Data. Springer-Verlag,
     New York.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'kanga.csv.bz2')
    return data
