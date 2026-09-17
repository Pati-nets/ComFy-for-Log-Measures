from feeed import extract_features # for calculating the scores of log measures
import os # for finding .xes files on the file system
import pandas # for handling collections of log complexity data

import Constants # to know where to look for input and where to export output

def collect_log_measure_data(measures: list):
    """
    Collects the complexity scores for all of the measures passed in a list.
    This function goes through all .xes files in the path specified at
    Constants.INPUT_PATH, imports the .xes file using the library pm4py, and
    adds the complexity scores of the event log to a panda DataFrame.
    The resulting table of complexity scores is automatically stored in a .csv
    file found at the path specified by Constants.OUTPUT_PATH. Furthermore, the
    resulting panda DataFrame is returned alongside the number of imported
    .xes files.

    Parameters
    ----------
    measures : list
        the list of measures whose complexity score should be calculated

    Returns
    -------
    DataFrame
        a panda DataFrame whose header contains the names of the specified
        complexity measures, and where each row contains the complexity scores
        according to these measures for one of the .xes files located at the
        folder specified in Constants.INPUT_PATH
    int
        the number of event logs that were imported from Constants.INPUT_PATH
        and whose complexity scores were calculated
    """
    header = measures
    collected_data = []
    filenames = []
    iteration = 1
    for file in os.listdir(Constants.INPUT_PATH):
        # make sure that we only consider event log files in XES format.
        full_file_path = os.path.join(Constants.INPUT_PATH, file)
        if os.path.isfile(full_file_path) and file.endswith(".xes"):
            filenames += [str(os.path.basename(file))]
            complexity_scores = extract_features(full_file_path, measures)
            data = []
            for measure in header:
                data += [complexity_scores[measure]]
            collected_data += [data]
            iteration += 1
    complexity = pandas.DataFrame(collected_data, index=filenames, columns=header)
    complexity.to_csv(Constants.OUTPUT_PATH + "log_complexity_scores.csv", mode='w', encoding='utf-8')
    return complexity, iteration-1

def import_data_from_csv_file(filepath: str, complexity_measures: list = [], silent=True):
    """
    Imports the complexity data in a .csv file to the program.
    It assumes that the first column of the .csv file specifies the used measures.
    The resulting internal table of complexity scores is a DataFrame from the
    library pandas. The program returns this DataFrame, the number of rows in
    the table (ignoring the header), and the header of the table.

    Returns
    -------
    DataFrame
        a pandas DataFrame that contains the complexity data in the .csv file
    int
        the number of rows in the imported DataFrame, excluding the header
    list
        the header of the .csv file, containing the analyzed complexity measures
    """
    if not filepath.endswith(".csv"):
        raise Exception("The specified file " + str(filepath) + " is not a CSV file.")
    imported_csv = pandas.read_csv(filepath, index_col=0)
    # if the user did not specify complexity measures to keep
    if len(complexity_measures) == 0:
        # return all data, the population size and the list of imported measures
        return imported_csv, len(imported_csv), list(imported_csv)
    # otherwise, remove all imported columns that do not appear in the specified measure list
    imported_measures = list(imported_csv)
    to_delete = []
    for measure in imported_measures:
        if measure not in complexity_measures:
            to_delete += [measure]
    complexity = imported_csv.drop(columns=to_delete)
    if not silent:
        # inform the user which columns were dropped
        print("Your file contains the following additional measures that I will ignore: ")
        print(to_delete)
    # return the resulting data, the population size and the list of measures
    population_size = len(complexity)
    measure_list = list(complexity)
    return complexity, population_size, measure_list
