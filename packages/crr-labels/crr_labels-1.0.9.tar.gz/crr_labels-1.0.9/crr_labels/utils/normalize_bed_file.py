from typing import List
import pandas as pd


def normalize_bed_file(cell_lines: List[str], bed_file: pd.DataFrame) -> pd.DataFrame:
    """Return normalized bed file.

    Parameters
    ---------------------------
    cell_lines:List[str],
        The cell lines to be maintained in the bed file.
    bed_file:pd.DataFrame,
        The bed file to normalized.

    Returns
    ----------------------------
    The normalized bed file.
    """
    if "strand" not in bed_file:
        bed_file["strand"] = "."
    cell_lines = [
        cell_line
        for cell_line in cell_lines
        if cell_line in bed_file.columns
    ]
    df = bed_file[["chromosome", "start",
                   "end", "strand", *sorted(cell_lines)]]
    return df.rename(columns={
        "chromosome": "chrom",
        "start": "chromStart",
        "end": "chromEnd"
    })
