DESCR = """
Xray decay from a gamma ray burst

Description:

     The X-ray decay light curve of Gamma ray burst 050525a obtained
     with the X-Ray Telescope (XRT) on board the Swift satellite. The
     dataset has 63 brightness measurements in the 0.4-4.5 keV spectral
     band at times ranging from 2 minutes to 5 days after the burst.

Variables:

     A data frame with 63 observations on the following 3 variables.

     ‘time’ in seconds since burst

     ‘flux’ X-ray flux in units of 10^-11 erg/cm2/s, 2-10 keV

     ‘error’ measurement error of the flux based on detector
          signal-to-noise values

Source:

     A. J. Blustin and 64 coauthors, Astrophys. J. 637, 901-913 2006.
     Available at http://arxiv.org/abs/astro-ph/0507515.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'gammaray.csv.bz2')
    return data
