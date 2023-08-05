from .utils import download, load_info, filter_required_cell_lines, validate_common_parameters, center_window, normalize_cell_lines, normalize_bed_file
from typing import List, Dict, Tuple,  Union
import pandas as pd


def fantom_available_cell_lines(genome: str = "hg19") -> pd.DataFrame:
    """Return supported cell lines available within FANTOM dataset.

    Parameters
    ---------------------------------------
    genome: str = "hg19",
        considered genome version. Currently supported only "hg19".

    Returns
    ---------------------------------------
    Return dataframe with the supported cell lines mapped to FANTOM name.
    """
    info = load_info("fantom_data")
    download(info[genome]["cell_lines"], "fantom_data")
    df = pd.read_csv("fantom_data/{filename}".format(
        filename=info[genome]["cell_lines"].split("/")[-1]
    ), sep="\t", header=None)
    cell_lines_names = df[0].str.split("cell line:", expand=True)
    cell_lines_names[1][
        cell_lines_names[0].str.startswith("H1") &
        cell_lines_names[0].str.contains("day00")
    ] = "H1"
    cell_lines_names[1][
        cell_lines_names[0].str.startswith("H9") &
        cell_lines_names[0].str.contains("H9ES")
    ] = "H9"
    nan_mask = pd.notnull(cell_lines_names[1])
    cell_lines_names = cell_lines_names[nan_mask]
    infected_mask = ~cell_lines_names[1].str.contains("infection")
    cell_lines_names = cell_lines_names[infected_mask]
    cell_lines_names[1] = cell_lines_names[1].str.split("/").str[0]
    cell_lines_names[1] = cell_lines_names[1].str.split(",").str[0]
    cell_lines_codes = pd.concat(
        objs=[
            cell_lines_names[1].apply(lambda x: x.split("ENCODE")[
                                      0].strip()).str.upper().str.replace("-", ""),
            df[nan_mask][infected_mask][1],
        ],
        axis=1
    )
    cell_lines_codes.columns = ["cell_line", "code"]
    return cell_lines_codes.reset_index(drop=True).groupby("cell_line").first().reset_index()


def filter_cell_lines(cell_lines: List[str], genome: str) -> pd.DataFrame:
    """Return FANTOM cell lines names for given cell lines.

    Parameters
    ---------------------------------------
    cell_lines: List[str],
        list of cell lines to be considered.
    genome: str,
        considered genome version. Currently supported only "hg19".

    Raises
    ---------------------------------------
    ValueError:
        if a required cell line is not currently available.

    Returns
    ---------------------------------------
    Return dataframe with the cell lines mapped to FANTOM name.
    """
    return filter_required_cell_lines(cell_lines, fantom_available_cell_lines(genome))


def average_cell_lines(cell_lines_names: pd.DataFrame, data: pd.DataFrame) -> pd.DataFrame:
    """Return dataframe with cell line columns averaged.

    Example: for HelaS3 there are 3 experiments, the values for HelaS3 are therefore averaged.

    Parameters
    ----------------------------------
    cell_lines_names: pd.DataFrame, the dataframe with required cell lines mapping.
    data: pd.DataFrame, the data informations to be averaged.

    Returns
    ----------------------------------
    The averaged dataframe.
    """
    for cell_line, group in cell_lines_names.groupby("cell_line"):
        data[cell_line] = data[group.code].astype(
            float
        ).mean(skipna=True, axis=1)
    return data.drop(columns=data.columns[data.columns.str.startswith("CNhs")])


def drop_always_inactives(data: pd.DataFrame, cell_lines: List[str], threshold: float) -> pd.DataFrame:
    """Drops the rows where no activation is present for any of the cell lines.

    Datapoints are considered active when they are ABOVE the threshold.

    Parameters
    -----------------------------------
    data: pd.DataFrame, the data to be considered.
    cell_lines: List[str, list of cell lines to be considered.
    threshold: float, the activation threshold.

    Returns
    -----------------------------------
    The dataset without the inactive rows.
    """
    return data[(data[cell_lines] > threshold).any(axis=1)]


def filter_promoters(
    cell_lines: List[str],
    cell_lines_names: pd.DataFrame,
    genome: str,
    info: Dict,
    window_size: int,
    threshold: float,
    drop_always_inactive_rows: bool,
    nrows: int
):
    """Return DataFrame containing the promoters filtered for given cell lines and adapted to given window size.

    Parameters
    ---------------------------------------
    cell_lines: List[str],
        list of cell lines to be considered.
    cell_lines_names: pd.DataFrame,
        DataFrame containing FANTOM map from cell line name to FANTOM code.
    genome: str,
        considered genome version. Currently supported only "hg19".
    window_size: int,
        window size to use for the various regions.
    center_enhancers: str,
        how to center the enhancer window, either around "peak" or the "center" of the region.
    threshold:float,
        activation threshold.
    drop_always_inactive_rows:bool= True,
        whetever to drop the rows where no activation is detected for every rows.
    nrows:int=None,
        the number of rows to read, usefull when testing pipelines for creating smaller datasets.

    Returns
    ---------------------------------------
    DataFrame containing filtered promoters.
    """
    download(info[genome]["promoters"], "fantom_data")
    promoters = pd.read_csv(
        "fantom_data/{filename}".format(
            filename=info[genome]["promoters"].split("/")[-1]
        ),
        comment="#",
        sep="\t",
        nrows=nrows
    ).drop(index=[0, 1])
    promoters = promoters.drop(columns=[
        c for c in promoters.columns
        if c.endswith("_id")
    ])
    promoters.columns = [
        c.split(".")[2] if c.startswith("tpm") else c for c in promoters.columns
    ]
    promoters = promoters[promoters.description.str.endswith("end")]
    annotation = promoters["00Annotation"].str.replace(
        ":", ",").str.replace(r"\.\.", ",").str.split(",", expand=True)
    promoters["chromosome"] = annotation[0]
    promoters["start"] = annotation[1].astype(int)
    promoters["end"] = annotation[2].astype(int)
    promoters["strand"] = annotation[3]
    positive_strand = promoters.strand == "+"
    negative_strand = promoters.strand == "-"
    promoters.loc[promoters.index[positive_strand], "start"] = promoters[positive_strand]["end"] - window_size
    promoters.loc[promoters.index[negative_strand], "end"] =  promoters[negative_strand]["start"] + window_size
    promoters = average_cell_lines(cell_lines_names, promoters)
    if drop_always_inactive_rows:
        promoters = drop_always_inactives(promoters, cell_lines, threshold)
    return promoters


def load_enhancers_coordinates(genome: str, info: Dict) -> pd.DataFrame:
    """Return enhancers coordinates informations.

    Parameters
    ---------------------------------------
    genome: str,
        considered genome version. Currently supported only "hg19".
    info: Dict,
        informations for FANTOM dataset.

    Returns
    ---------------------------------------
    Dataset containing the enhancers coordinates informations.
    """
    download(info[genome]["enhancers_info"], "fantom_data")
    return pd.read_csv(
        "fantom_data/{filename}".format(
            filename=info[genome]["enhancers_info"].split("/")[-1]
        ),
        sep="\t",
        header=None,
        names=["chromosome", "start", "end", "name", "score", "strand",
               "thickStart", "thickEnd", "itemRgb", "blockCount", "blockSizes", "blockStarts"]
    )


def filter_enhancers(
    cell_lines: List[str],
    cell_lines_names: pd.DataFrame,
    genome: str,
    info: Dict,
    window_size: int,
    center_mode: str,
    threshold: float,
    drop_always_inactive_rows: bool,
    nrows: int
) -> pd.DataFrame:
    """Return DataFrame containing the enhancers filtered for given cell lines and adapted to given window size.

    Parameters
    ---------------------------------------
    cell_lines: List[str],
        list of cell lines to be considered.
    cell_lines_names: pd.DataFrame,
        DataFrame containing FANTOM map from cell line name to FANTOM code.
    genome: str,
        considered genome version. Currently supported only "hg19".
    window_size: int,
        window size to use for the various regions.
    center_enhancers: str,
        how to center the enhancer window, either around "peak" or the "center" of the region.
    threshold:float,
        activation threshold.
    drop_always_inactive_rows:bool= True,
        whetever to drop the rows where no activation is detected for every rows.
    nrows:int=None,
        the number of rows to read, usefull when testing pipelines for creating smaller datasets.

    Returns
    ---------------------------------------
    DataFrame containing filtered enhancers.
    """
    download(info[genome]["enhancers"], "fantom_data")
    enhancers = pd.read_csv(
        "fantom_data/{filename}".format(
            filename=info[genome]["enhancers"].split("/")[-1]
        ),
        comment="#",
        sep="\t",
        nrows=nrows
    )
    coordinates = load_enhancers_coordinates(genome, info)
    enhancers["start"] = coordinates.start
    enhancers["end"] = coordinates.end
    enhancers = center_window(
        enhancers,
        window_size,
        coordinates.thickStart if center_mode == "peak" else None
    )
    enhancers["chromosome"] = coordinates.chromosome
    enhancers = average_cell_lines(cell_lines_names, enhancers)
    if drop_always_inactive_rows:
        enhancers = drop_always_inactives(enhancers, cell_lines, threshold)
    return enhancers


def fantom(
    cell_lines: Union[List[str], str],
    window_size: int,
    genome: str = "hg19",
    center_enhancers: str = "peak",
    enhancers_threshold: float = 0,
    promoters_threshold: float = 5,
    drop_always_inactive_rows: bool = True,
    binarize: bool = True,
    nrows: int = None
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Runs the pipeline over the fantom raw CAGE data.

    Parameters
    ---------------------------------------
    cell_lines: List[str],
        list of cell lines to be considered.
    window_size: int,
        window size to use for the various regions.
    genome: str= "hg19",
        considered genome version. Currently supported only "hg19".
    center_enhancers: str= "peak",
        how to center the enhancer window, either around "peak" or the "center" of the region.
    enhancers_threshold:float= 0,
        activation threshold for the enhancers.
    promoters_threshold:float= 5,
        activation threshold for the promoters.
    drop_always_inactive_rows:bool= True,
        whetever to drop the rows where no activation is detected for every rows.
    binarize: bool= True,
        Whetever to return the data binary-encoded, zero for inactive, one for active.
    nrows:int=None,
        the number of rows to read, usefull when testing pipelines for creating smaller datasets.

    Raises
    ----------------------------------------
    ValueError:
        If given cell lines list is empty.
    ValueError:
        If given cell lines are not strings.
    ValueError:
        If given window size is not an integer.
    ValueError:
        If given window size is not a strictly positive integer.
    ValueError:
        If given genome version is not a string.
    ValueError:
        If given nrows parameter is not None or a strictly positive integer.
    ValueError:
        If given thresholds are not positive real numbers.
    ValueError:
        If given center_enhancers is not "peak" or "center".

    Returns
    ----------------------------------------
    Tuple containining dataframes informations for enhancers and promoters for chosen cell lines.
    """
    if isinstance(cell_lines, str):
        cell_lines = [cell_lines]
    info = load_info("fantom_data")
    validate_common_parameters(cell_lines, window_size, genome, nrows, info)
    cell_lines = normalize_cell_lines(cell_lines)
    for threshold in (enhancers_threshold, promoters_threshold):
        if not isinstance(threshold, (float, int)) or threshold < 0:
            raise ValueError("Threshold must be a positive real number.")
    if center_enhancers not in ("peak", "center"):
        raise ValueError("The given center_enhancers option {center_enhancers} is not supported.".format(
            center_enhancers=center_enhancers
        ))

    cell_lines_names = filter_cell_lines(cell_lines, genome)
    enhancers = filter_enhancers(
        cell_lines=cell_lines,
        cell_lines_names=cell_lines_names,
        genome=genome,
        info=info,
        window_size=window_size,
        center_mode=center_enhancers,
        threshold=enhancers_threshold,
        drop_always_inactive_rows=drop_always_inactive_rows,
        nrows=nrows
    ).reset_index(drop=True)
    promoters = filter_promoters(
        cell_lines=cell_lines,
        cell_lines_names=cell_lines_names,
        genome=genome,
        info=info,
        window_size=window_size,
        threshold=promoters_threshold,
        drop_always_inactive_rows=drop_always_inactive_rows,
        nrows=nrows
    ).reset_index(drop=True)

    if binarize:
        enhancers[cell_lines] = (enhancers[cell_lines]
                                 > enhancers_threshold).astype(int)
        promoters[cell_lines] = (promoters[cell_lines]
                                 > promoters_threshold).astype(int)

    enhancers = normalize_bed_file(cell_lines, enhancers)
    promoters = normalize_bed_file(cell_lines, promoters)
    return enhancers, promoters
