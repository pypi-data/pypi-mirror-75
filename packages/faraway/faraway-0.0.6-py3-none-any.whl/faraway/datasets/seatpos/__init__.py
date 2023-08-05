DESCR = """
Car seat position depending driver size

Description

Car drivers like to adjust the seat position for their own comfort. Car designers would find it helpful to know where different drivers will position the seat depending on their size and age. Researchers at the HuMoSim laboratory at the University of Michigan collected data on 38 drivers.

Usage

data(seatpos)
Format

The dataset contains the following variables

Age
Age in years

Weight
Weight in lbs

HtShoes
Height in shoes in cm

Ht
Height bare foot in cm

Seated
Seated height in cm

Arm
lower arm length in cm

Thigh
Thigh length in cm

Leg
Lower leg length in cm

hipcenter
horizontal distance of the midpoint of the hips from a fixed location in the car in mm

Source

"Linear Models in R" by Julian Faraway, CRC Press, 2004
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'seatpos.csv.bz2')
    return data
