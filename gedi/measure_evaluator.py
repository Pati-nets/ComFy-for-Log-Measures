from feeed.feature_extractor import extract_features
import os
import pandas

import constants

def calculate_measure_results(log_measures: list, parent_dir: str):
    for f in os.scandir(parent_dir):
        if f.is_dir():
            directory = f.path
            print("Evaluating event logs in folder " + str(directory) + "...")
            folder_name = ""
            dir_parts = directory.split("/")
            if dir_parts[-1] != "":
                folder_name = dir_parts[-1]
            else:
                folder_name = dir_parts[-2]
            number_of_event_logs = 0
            log_names = []
            collected_data = []
            # go through all subdirectories in the specified directory
            for subdir, dirs, files in os.walk(directory):
                for file in files:
                    file_path = os.path.join(subdir, file)
                    # process the file if it is an .xes file
                    if file_path.endswith(".xes"):
                        print("Calculating log measures for file " + str(file_path) + ".")
                        log_names += [str(file_path)]
                        # calculate the scores of the specified log measures
                        complexity_scores = extract_features(file_path, log_measures)
                        data = []
                        for measure in log_measures:
                            data += [complexity_scores[measure]]
                        collected_data += [data]
                        number_of_event_logs += 1
            complexity = pandas.DataFrame(collected_data, index = log_names, columns = log_measures)
            complexity.to_csv(constants.measure_calculation_output_folder + "log_complexity_scores_" + folder_name + ".csv", mode='w', encoding='utf-8')
    return complexity, number_of_event_logs

def import_measure_results(filepath: str, log_measures: list = []):
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

if __name__ == "__main__":
    calculate_measure_results(constants.log_measures, "./data/")
