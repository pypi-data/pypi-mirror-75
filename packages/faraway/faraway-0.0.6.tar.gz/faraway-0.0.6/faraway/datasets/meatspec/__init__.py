DESCR = """
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, 'meatspec.csv.bz2')
    return data
