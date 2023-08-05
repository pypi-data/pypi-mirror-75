DESCR = """
Species diversity on the Galapagos Islands

Description

There are 30 Galapagos islands and 7 variables in the dataset. The relationship between the number of plant species and several geographic variables is of interest. The original dataset contained several missing values which have been filled for convenience.

Usage

data(gala)
Format

The dataset contains the following variables

Species
the number of plant species found on the island

Area
the area of the island (km$^2$)

Elevation
the highest elevation of the island (m)

Nearest
the distance from the nearest island (km)

Scruz
the distance from Santa Cruz island (km)

Adjacent
the area of the adjacent island (square km)

Source

M. P. Johnson and P. H. Raven (1973) "Species number and endemism: The Galapagos Archipelago revisited" Science, 179, 893-895
"""


def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'galapagos.csv.bz2')
    return data
