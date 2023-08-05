from typing import List

def normalize_cell_lines(cell_lines:List[str])->List[str]:
    return [
        cell_line.upper() for cell_line in cell_lines
    ]