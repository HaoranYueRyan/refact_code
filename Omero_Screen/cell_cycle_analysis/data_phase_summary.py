import os
import pandas as pd
from cell_cycle_distribution_functions import fun_normalise, fun_CellCycle
from os import listdir

def plate_get_well(plate_list,conn):
    """  get the corresponding well_id according to plate and stored in dictionary

    :param plate_list: the list of plate id
    :param conn: connect to omero
    :return: A dictionary, the keys are plate id, the values are list of well id

    for example myDict['948']=[10620,10621,...]
    """
    plate_well_dict={}
    for plate in plate_list:
        plate_well_dict[str(plate)]=list()
        plate = conn.getObject("Plate", plate)
        for well in plate.listChildren():
            plate_well_dict[str(plate)].append(well.id)
    return plate_well_dict


def dict_wells_corr(F_dir):
    """
    # %% Importing RAW data from path of file & excluding inconsistent wells

    :param F_dir: the path of RAW
    :return: A dataframe and adding a columns called the cell_id that group by "plate_id", "well_id", "image_id", "Cyto_ID", which make sure that each segmented cell will have individual number.
    """

    list_files = list(filter(lambda file: ".csv" in file, listdir(F_dir + "/data/")))
    data_raw = pd.DataFrame()
    for file in list_files:
        tmp_data = pd.read_csv(F_dir + "data/" + file, sep=",")
        try:
            if "plate_id" and "well_id" in tmp_data.columns:
                tmp_plate = tmp_data["plate_id"].unique()[0]
                Dict_plate_well = plate_get_well(tmp_plate)

                if tmp_plate in Dict_plate_well.keys():
                   tmp_data = tmp_data.copy().loc[tmp_data["well_id"].isin(Dict_plate_well[tmp_plate])]
                data_raw = pd.concat([data_raw, tmp_data])
        except KeyError:
            print('Not Exist: plate_id, well_id')
        del ([tmp_data, file])
    data_raw.loc[:, "cell_id"] = data_raw.groupby(["plate_id", "well_id", "image_id", "Cyto_ID"]).ngroup()
    return data_raw


def assign_cell_cycle_phase(data, *args,):
    """
    # %% Selecting parameters of interest and aggregating counts of nuclei and total cellular DAPI signal
      %% Normalising selected parameters & assigning cell cycle phases

    :param data:A data frame that including the necessary parameters
    :param args:interesting parameters used for group data frame to aggregating counts of nuclei and total cellular DAPI signal
    :return: data_IF (A dataframe assigned a cell cycle phase to each cell), data_thresholds (threshold values of normalised integrated DAPI intensities)
    """
    try:
        data_IF = data.groupby(list(args)).agg(
        nuclei_count=("label", "count"),
        nucleus_area=("area_nucleus", "sum"),
        DAPI_total=("integrated_int_DAPI", "sum")).reset_index()
        data_IF["condition"] = data_IF["condition"].astype(str)
    except KeyError:
        print('Not Exist: label, area_nucleus,integrated_int_DAPI,condition')
    data_IF = fun_normalise(data=data_IF, values=["DAPI_total", "intensity_mean_EdU_cell", "intensity_mean_H3P_cell",
                                                  "area_cell"])
    data_IF, data_thresholds = fun_CellCycle(data=data_IF, ctr_col="condition", ctr_cond="0.0")
    return data_IF, data_thresholds

def cell_cycle_summary(data_dir):
    """
    # %% Establishing proportions (%) of cell cycle phases
    calling functions of dict_wells_corr and assign_cell_cycle_phase to get the data_IF, data_thresholds

    :param data_dir: the path of RAW data frame
    :return: A dataframe summarized each cell cycle phase
    """
    data_IF, data_thresholds = assign_cell_cycle_phase(dict_wells_corr(data_dir))
    data_cell_cycle = pd.DataFrame()
    for experiment in data_IF["experiment"].unique():
        for cell_line in data_IF.loc[data_IF["experiment"] == experiment]["cell_line"].unique():
            for condition in data_IF.loc[(data_IF["experiment"] == experiment) &
                                             (data_IF["cell_line"] == cell_line)]["condition"].unique():
                tmp_data = data_IF.loc[(data_IF["experiment"] == experiment) &
                                           (data_IF["cell_line"] == cell_line) &
                                           (data_IF["condition"] == condition)]
                n = len(tmp_data)

                tmp_data = tmp_data.groupby(["experiment", "plate_id", "cell_line", "condition", "cell_cycle"],
                                                as_index=False).agg(
                        count=("cell_id", "count"),
                        nuclear_area_mean=("nucleus_area", "mean"),
                        DAPI_total_mean=("DAPI_total_norm", "mean"),
                        area_cell_mean=("area_cell_norm", "mean"))
                # calculate proportions for each cell cycle phase
            tmp_data["n"] = n
            tmp_data["percentage"] = (tmp_data["count"] / tmp_data["n"]) * 100
            data_cell_cycle = pd.concat([data_cell_cycle, tmp_data])
    data_cell_cycle_summary = data_cell_cycle.groupby(["cell_line", "cell_cycle", "condition"], as_index=False).agg(
            percentage_mean=("percentage", "mean"),
            percentage_sd=("percentage", "std"))
    return data_cell_cycle_summary


def save_folder(Path_data,exist_ok=True):
    """  Establishing path to the data and creating a folder to save exported .pdf files

    :param Path_data: the path used to save the exported .pdf files
    :return: This method does not return any value.
    """
    # path_data = "/Users/Lab/Desktop/CDK1ArrestCheck_20hr_1/"
    path_export = Path_data+ "/Figures/"
    if exist_ok==True:
        os.makedirs(path_export, exist_ok=True)
    else:
        isExist = os.path.exists(path_export)
        try:
            if isExist==False:
                os.makedirs(path_export)
        except FileExistsError:
            print('File already exists')









def local_data(data_IF,*args,):
    for experiment in data_IF[args[0]].unique():
        for cell_line in data_IF.loc[data_IF[args[0]] == experiment][args[1]].unique():
            for condition in data_IF.loc[(data_IF[args[0]] == experiment) &
                                         (data_IF[args[1]] == cell_line)][args[2]].unique():
                tmp_data = data_IF.loc[(data_IF[args[0]] == experiment) &
                                       (data_IF[args[1]] == cell_line) &
                                       (data_IF[args[2]] == condition)]



def _local(data,*args,**kwargs):
    for arg in args:
        for i in data[arg].unique():
            data.loc[data["experiment"] == i][0].unique()




def dict_wells_corr(list_files_path,):
    """
    # %% Establishing inconsistent wells which should be excluded from the analysis
    :param list_files_path:
    :return:
    """
    # %% Importing RAW data & excluding inconsistent wells
    list_files = list(filter(lambda file: ".csv" in file, listdir(list_files_path + "/data/")))

    data_raw = pd.DataFrame()

    for file in list_files:

        tmp_data = pd.read_csv(list_files_path + "data/" + file, sep=",")
        tmp_plate = tmp_data["plate_id"].unique()[0]
        Dict_plate_well=plate_get_well(tmp_plate)

        if tmp_plate in Dict_plate_well.keys():
            tmp_data = tmp_data.copy().loc[tmp_data["well_id"].isin(Dict_plate_well[tmp_plate])]

        # if tmp_plate in wells_exclude.keys():
        #     tmp_data = tmp_data.copy().loc[~tmp_data["well_id"].isin(wells_exclude[tmp_plate])]
        data_raw = pd.concat([data_raw, tmp_data])
        del ([tmp_data, file])
    data_raw.loc[:, "cell_id"] = data_raw.groupby(["plate_id", "well_id", "image_id", "Cyto_ID"]).ngroup()
    return data_raw



def assign_cell_cycle_phase(data_raw,*args,):
    """

    :param data_raw:
    :return:
    """
    data_IF = data_raw.groupby(list(args)).agg(
    nuclei_count=("label", "count"),
    nucleus_area=("area_nucleus", "sum"),
    DAPI_total=("integrated_int_DAPI", "sum")).reset_index()
    data_IF["condition"] = data_IF["condition"].astype(str)
    data_IF = fun_normalise(data=data_IF,values=["DAPI_total", "intensity_mean_EdU_cell", "intensity_mean_H3P_cell", "area_cell"])    # %% Normalising selected parameters & assigning cell cycle phases
    data_IF, data_thresholds = fun_CellCycle(data=data_IF, ctr_col="condition", ctr_cond="0.0")
    return data_IF, data_thresholds



def cell_cycle_percentage(data_IF,*args):
    """
    # %% Establishing proportions (%) of cell cycle phases

    :param data_IF:
    :return: A dataframe
    """
    data_cell_cycle = pd.DataFrame()
    for experiment in data_IF["experiment"].unique():
        for cell_line in data_IF.loc[data_IF["experiment"] == experiment]["cell_line"].unique():
            for condition in data_IF.loc[(data_IF["experiment"] == experiment) &
                                     (data_IF["cell_line"] == cell_line)]["condition"].unique():
                tmp_data = data_IF.loc[(data_IF["experiment"] == experiment) &
                                     (data_IF["cell_line"] == cell_line) &
                                     (data_IF["condition"] == condition)]
                n = len(tmp_data)

                tmp_data = tmp_data.groupby(list(args),
                                        as_index=False).agg(
                count=("cell_id", "count"),
                nuclear_area_mean=("nucleus_area", "mean"),
                DAPI_total_mean=("DAPI_total_norm", "mean"),
                area_cell_mean=("area_cell_norm", "mean"))
            # calculate proportions for each cell cycle phase
            tmp_data["n"] = n
            tmp_data["percentage"] = (tmp_data["count"] / tmp_data["n"]) * 100
            data_cell_cycle = pd.concat([data_cell_cycle, tmp_data])
    data_cell_cycle_summary = data_cell_cycle.groupby(["cell_line", "cell_cycle", "condition"], as_index=False).agg(
                                     percentage_mean=("percentage", "mean"),
                                     percentage_sd=("percentage", "std"))
    return data_cell_cycle_summary
