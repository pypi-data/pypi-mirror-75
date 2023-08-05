from typing import List
import pandas as pd


def filter_required_cell_lines(cell_lines: List[str], cell_lines_codes: pd.DataFrame) -> pd.DataFrame:
    """Return filtered cell lines codes, keeping only required cell lines.

    Parameters
    ---------------------------------------
    cell_lines:List[str], the cell lines required.
    cell_lines_codes:pd.DataFrame, the dataframe containing all the cell lines and codes.

    Raises
    ---------------------------------------
    ValueError:
        If one of the required cell lines is not currently available.

    Returns
    ---------------------------------------
    Cell lines codes dataframe with only required cell lines.
    """
    filtered_cell_lines = cell_lines_codes[
        cell_lines_codes.cell_line.isin(cell_lines)
    ]
    for cell_line in cell_lines:
        if not filtered_cell_lines.cell_line.isin([cell_line]).any():
            raise ValueError("Given cell line {cell_line} is not currently available.".format(
                cell_line=cell_line
            ))
    return filtered_cell_lines[["cell_line", "code"]]