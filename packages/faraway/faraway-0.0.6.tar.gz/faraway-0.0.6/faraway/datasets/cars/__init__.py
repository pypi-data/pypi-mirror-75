DESCR = """
Speed and Stopping Distances of Cars

Description

The data give the speed of cars and the distances taken to stop. Note that the data were recorded in the 1920s.

A data frame with 50 observations on 2 variables.

speed	numeric	Speed (mph)
dist	numeric	Stopping distance (ft)

Source

Ezekiel, M. (1930) Methods of Correlation Analysis. Wiley.

References

McNeil, D. R. (1977) Interactive Data Analysis. Wiley.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'cars.csv.bz2')
    return data
