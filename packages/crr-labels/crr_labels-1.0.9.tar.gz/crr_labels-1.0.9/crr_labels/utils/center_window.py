import pandas as pd


def center_window(data: pd.DataFrame, window_size: int, center: pd.Series=None) -> pd.DataFrame:
    """Returns dataframe with updated regions for given window size and center.

    Parameters
    -----------------------------
    data:pd.DataFrame,
        The dataframe containing the regions.
    window_size:int,
        Window size to use for the various regions.
    center:pd.Series=None,
        Series representing the center of the new window. By default, use the pre-existing center.

    Returns
    ------------------------------
    Updated dataframe.
    """
    if center is None:
        center = data.start + (data.end - data.start)/2
    data["start"] = (center - window_size/2).astype(int)
    data["end"] = (center + window_size/2).astype(int)
    return data
