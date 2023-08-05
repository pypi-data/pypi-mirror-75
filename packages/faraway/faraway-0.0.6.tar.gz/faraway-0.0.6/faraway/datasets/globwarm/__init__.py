DESCR = """
Northern Hemisphere temperatures and climate proxies in the last millenia

Description

Average Northen Hemisphere Temperature from 1856-2000 and eight climate proxies from 1000-2000AD. Data can be used to predict temperatures prior to 1856.

A data frame with 1001 observations on the following 10 variables.

nhtemp: Northern hemisphere average temperature (C) provided by the UK Met Office (known as HadCRUT2)

wusa: Tree ring proxy information from the Western USA.

jasper: Tree ring proxy information from Canada.

westgreen: Ice core proxy information from west Greenland

chesapeake: Sea shell proxy information from Chesapeake Bay

tornetrask: Tree ring proxy information from Sweden

urals: Tree ring proxy information from the Urals

mongolia: Tree ring proxy information from Mongolia

tasman: Tree ring proxy information from Tasmania

year: Year 1000-2000AD

Details

See the source and references below for the original data. Only some proxies have been included here. Some missing values have been imputed. The proxy data have been smoothed. This version of the data is intended only for demonstration purposes. If you are specifically interested in the subject matter, use the original data.

Source

P.D. Jones and M.E. Mann (2004) "Climate Over Past Millennia" Reviews of Geophysics, Vol. 42, No. 2, RG2002, doi:10.1029/2003RG000143

References

www.ncdc.noaa.gov/paleo/pubs/jones2004/jones2004.html

"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'globwarm.csv.bz2')
    return data
