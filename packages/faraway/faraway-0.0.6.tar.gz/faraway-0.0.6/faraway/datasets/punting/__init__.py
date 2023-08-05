DESCR = """
Leg strength and punting

Description:

     Investigators studied physical characteristics and ability in 13
     (American) football punters. Each volunteer punted a football ten
     times. The investigators recorded the average distance for the ten
     punts, in feet.

Variables:

     A data frame with 13 observations on the following 7 variables.

     ‘Distance’ average distance over 10 punts

     ‘Hang’ hang time

     ‘RStr’ right leg strength in pounds

     ‘LStr’ left leg strength in pounds

     ‘RFlex’ right hamstring muscle flexibility in degrees

     ‘LFlex’ left hamstring muscle flexibility in degrees

     ‘OStr’ overall leg strength in foot pounds

Source:

     Department of Health, Physical Education and Recreation at the Virginia Polytechnic Institute and State University, 1983.
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'punting.csv.bz2')
    return data
