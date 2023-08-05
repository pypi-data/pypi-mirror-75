DESCR = """
Percentage of Body Fat and Body Measurements

Description

Age, weight, height, and 10 body circumference measurements are recorded for 252 men. Each man's percentage of body fat was accurately estimated by an underwater weighing technique.

Usage

data(fat)
Format

A data frame with 252 observations on the following 18 variables.

brozek
Percent body fat using Brozek's equation, 457/Density - 414.2

siri
Percent body fat using Siri's equation, 495/Density - 450

density
Density (gm/$cm^3$)

age
Age (yrs)

weight
Weight (lbs)

height
Height (inches)

adipos
Adiposity index = Weight/Height$^2$ (kg/$m^2$)

free
Fat Free Weight = (1 - fraction of body fat) * Weight, using Brozek's formula (lbs)

neck
Neck circumference (cm)

chest
Chest circumference (cm)

abdom
Abdomen circumference (cm) at the umbilicus and level with the iliac crest

hip
Hip circumference (cm)

thigh
Thigh circumference (cm)

knee
Knee circumference (cm)

ankle
Ankle circumference (cm)

biceps
Extended biceps circumference (cm)

forearm
Forearm circumference (cm)

wrist
Wrist circumference (cm) distal to the styloid processes

Source

Johnson R. Journal of Statistics Education v.4, n.1 (1996)
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'fat.csv.bz2')
    return data
