DESCR = """
Annual mean temperatures in Ann Arbor, Michigan

Description:

     The data comes from the U.S. Historical Climatology Network.

Variables:

     A data frame with 115 observations on the following 2 variables.

     year year from 1854 to 2000

     temp annual mean temperatures in degrees F in Ann Arbor

Source:

     United States Historical Climatology Network: <URL:
     http://www.ncdc.noaa.gov/oa/climate/research/ushcn/ushcn.html>
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'aatemp.csv.bz2')
    return data
