import camelot
import tabula
import pandas as pd

def extract_table_from_pdf(path, pages="1-end", flavor="stream"):
    """
    Reads *all* tables on the given pages and concatenates them
    into one DataFrame.
    """
    tables = camelot.read_pdf(path, pages=pages, flavor=flavor)
    if not tables:
        raise ValueError(f"No tables found on pages {pages}")
    df = pd.concat([t.df for t in tables], ignore_index=True)
    return df
