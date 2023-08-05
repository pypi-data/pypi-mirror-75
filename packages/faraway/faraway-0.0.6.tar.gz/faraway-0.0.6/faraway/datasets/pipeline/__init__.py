DESCR = """
NIST data on ultrasonic measurements of defects in the Alaska pipeline

Description:

     Researchers at National Institutes of Standards and Technology
     (NIST) collected data on ultrasonic measurements of the depths of
     defects in the Alaska pipeline in the field. The depth of the
     defects were then remeasured in the laboratory. These measurements
     were performed in six different batches. The laboratory
     measurements are more accurate than the in-field measurements, but
     more time consuming and expensive.

Variables:

     A data frame with 107 observations on the following 3 variables.

     Field measurement of depth of defect on site

     Lab measurement of depth of defect in the lab

     Batch the batch of measurements

Source:

     Office of the Director of the Institute of Materials Research (now
     the Materials Science and Engineering Laboratory) of NIST
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'pipeline.csv.bz2')
    return data
