import pandas # for handling collections of log complexity data

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
