DESCR = """
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'statedata.csv.bz2')
    return data
