DESCR = """
Time in minutes to eye opening after reversal of anaesthetic.

Description:

     A doctor at major London hospital compared the effects of 4
     anaesthetics used in major operations. 80 patients were divided
     into groups of 20.

Variables:

     A data frame with 80 observations on the following 2 variables.

     ‘breath’ time in minutes to start breathing unassisted

     ‘tgrp’ Four treatment groups ‘A’ ‘B’ ‘C’ ‘D’

Source:

     Chatfield C. (1995) Problem Solving: A Statistician's Guide, 2ed
     Chapman Hall.

Examples:

     data(anaesthetic)
     ## maybe str(anaesthetic) ; plot(anaesthetic) ...
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'anaesthetic.csv.bz2')
    return data
