DESCR = """
Mayer's 1750 data on the Manilius crater on the moon

Description

In 1750, Tobias Mayer collected data on various landmarks on the moon in order to determine its orbit. The data involving the position of the Manilius crater resulted in a least squares like problem. The example is discussed in Steven Stigler's History of Statistics.

Usage

data(manilius)
Format

A data frame with 27 observations on the following 4 variables.

arc
an angle known as h in Stigler's notation

sinang
the sin(g-k) where g and k are two angles in Stigler

cosang
the cos(g-k) where g and k are two angles in Stigler

group
one of three groups determined by Mayer

Details

See Stigler for a detailed description.

Source

Stigler, S. (1986) History of Statistics. Belknap Press, Harvard.

References

Mayer, T. (1750) Abhandlung uber die Umwaltzung des Monds um seine Axe und die scheinbare Bewegung der Mondsflecken published in the Kosmographische Nachrichten und Sammlungen auf das Jahr 1748. 52-183
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'manilius.csv.bz2')
    return data
