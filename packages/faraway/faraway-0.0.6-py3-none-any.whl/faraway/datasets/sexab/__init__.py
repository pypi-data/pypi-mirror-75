DESCR = """
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'sexab.csv.bz2')
    return data
