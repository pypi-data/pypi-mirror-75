DESCR = """
"""

def load():
    from faraway import datasets
    data = datasets.loaddata(__file__, '.csv.bz2')
    return data
