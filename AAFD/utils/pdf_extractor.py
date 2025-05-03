import camelot
import tabula
import pandas as pd


def extract_table_from_pdf(path: str,
                           pages: str = "1",
                           engine: str = "camelot") -> pd.DataFrame:
    """
    Extract the first table from a PDF and return it as a pandas DataFrame.

    :param path: path to the PDF file
    :param pages: pages to scan, e.g. "1", "1-3", or "1-end"
    :param engine: "camelot" or "tabula"
    """
    if engine == "camelot":
        tables = camelot.read_pdf(path, pages=pages)
        if not tables:
            raise ValueError(f"No tables found on pages {pages} with Camelot")
        return tables[0].df
    elif engine == "tabula":
        dfs = tabula.read_pdf(path, pages=pages, multiple_tables=True)
        if not dfs:
            raise ValueError(f"No tables found on pages {pages} with Tabula")
        return dfs[0]
    else:
        raise ValueError("Engine must be 'camelot' or 'tabula'")
