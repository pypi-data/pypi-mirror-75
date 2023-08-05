DESCR = """
Sonoluminescence

Description:

     The ‘sono’ data frame has 16 rows and 8 columns.  Sonoluminescence
     is the process of turning sound energy into light.  An experiment
     was conducted to study factors affecting this process.

Variables:

     This data frame contains the following columns:

     ‘Intensity’ Sonoluminescent light intensity

     ‘Molarity’ Amount of Solute. The coding is "low" for 0.10 mol and
          "high" for 0.33 mol.

     ‘Solute’ Solute type. The coding is "low" for sugar and "high" for
          glycerol.

     ‘pH’ The coding is "low" for 3 and "high" for 11.

     ‘Gas’ Gas type in water. The coding is "low" for helium and "high"
          for air.

     ‘Water’ Water depth. The coding is "low" for half and "high" for
          full.

     ‘Horn’ Horn depth. The coding is "low" for 5 mm and "high" for 10
          mm.

     ‘Flask’ Flask clamping. The coding is "low" for unclamped and
          "high" for clamped.

Source:

     Eva Wilcox and Ken Inn of the NIST Physics Laboratory conducted
     this experiment during 1999 and published in NIST/SEMATECH
     e-Handbook of Statistical Methods,
     http://www.itl.nist.gov/div898/handbook/
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'sono.csv.bz2')
    return data
