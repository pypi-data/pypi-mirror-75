DESCR = """
Strength of a thermoplastic composite depending on two factors
Description
The composite data frame has 9 rows and 3 columns. Data comes from an experiment to test the strength of a thermoplastic composite depending on the power of a laser and speed of a tape.

Usage
data(composite)
Format
This data frame contains the following columns:

strength
interply bond strength of the composite

laser
laser power at 40, 50 or 60W

tape
tape speed, slow=6.42 m/s, medium=13m/s and fast=27m/s

Source
Mazumdar, S and Hoa S (1995) "Application of a Taguchi Method for Process enhancement of an online consolidation technique" Composites 26, 669-673
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'composite.csv.bz2')
    return data
