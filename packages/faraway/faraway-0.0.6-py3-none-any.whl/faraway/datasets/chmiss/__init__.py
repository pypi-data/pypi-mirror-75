DESCR = """
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'chmiss.csv.bz2')
    return data
