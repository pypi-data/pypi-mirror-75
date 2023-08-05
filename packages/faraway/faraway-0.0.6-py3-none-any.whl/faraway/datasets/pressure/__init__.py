DESCR = """
Vapor Pressure of Mercury as a Function of Temperature

Description:

     Data on the relation between temperature in degrees Celsius and
     vapor pressure of mercury in millimeters (of mercury).

Variables:

     A data frame with 19 observations on 2 variables.

       [, 1]  temperature  numeric  temperature (deg C) 
       [, 2]  pressure     numeric  pressure (mm)       
      
Source:

     Weast, R. C., ed. (1973) _Handbook of Chemistry and Physics_.  CRC
     Press.

References:

     McNeil, D. R. (1977) _Interactive Data Analysis_.  New York:
     Wiley.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'pressure.csv.bz2')
    return data
