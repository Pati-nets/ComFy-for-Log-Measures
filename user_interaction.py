import os # for finding .xes and .csv files on the storage
import questionary

import Constants

def print_comfy_logo():
    """
    Prints the logo of the ComFy tool.
    """
    comfy_logo = ""
    comfy_logo += r" ___ -------------------------------------- ___ " + "\n"
    comfy_logo += r"|   |    ______                ______      |   |" + "\n"
    comfy_logo += r"|   |   / ____/___  ____ ___  / ____/_  __ |   |" + "\n"
    comfy_logo += r"|   |  / /   / __ \/ __ `__ \/ /_  / / / / |   |" + "\n"
    comfy_logo += r"|   | / /___/ /_/ / / / / / / __/ / /_/ /  |   |" + "\n"
    comfy_logo += r"|   | \____/\____/_/ /_/ /_/_/    \__, /   |   |" + "\n"
    comfy_logo += r"|   |----------------------------/____/----|   |" + "\n"
    comfy_logo += r"|                              for event logs! |" + "\n"
    comfy_logo += r" ============================================== " + "\n"
    comfy_logo += r" []                                          [] " + "\n"
    print(comfy_logo)

def print_welcome_message():
    """
    Prints a welcome message for the user that explains the use of the tool.
    Then, it inspects the input path and counts the number of .xes files in
    the path that could be used as a population. This number of .xes files
    is then returned by this function.

    Returns
    -------
    int
        the number of .xes files found in Constants.INPUT_PATH
    int
        the number of .csv files found in Constants.INPUT_PATH
    """
    print_comfy_logo()
    print("Welcome to the Complexity Factor Analyzer, ComFy - for event logs!")
    print("This tool allows you to perform a factor analysis on event log complexity measures.")
    print("With the results of such a factor analysis, you can find groups of similar complexity measures.")
    print()
    print("As a population, I will use all .xes files in the folder " + str(Constants.INPUT_PATH) + ".")
    number_of_xes_files = 0
    number_of_csv_files = 0
    for subdir, dirs, files in os.walk(Constants.INPUT_PATH):
        for file in files:
            full_file_path = os.path.join(subdir, file)
            if os.path.isfile(full_file_path):
                if file.endswith(".xes"):
                    number_of_xes_files += 1
                elif file.endswith(".csv"):
                    number_of_csv_files += 1
    print("I found " + str(number_of_xes_files) + " .xes files and " + str(number_of_csv_files) + " .csv files in this folder.")
    print()
    return number_of_xes_files, number_of_csv_files

def ask_user_for_source(number_of_xes_files: int):
    """
    Asks the user how they want to collect the complexity data. The function
    allows two alternatives: Either to calculate the complexity scores of the
    event logs in .xes format in the input folder specified in Constants.INPUT_PATH,
    or to use the complexity data collected in a .csv file. If there are no .xes
    files in the input folder, the user is informed that the tool assumes they
    want to specify a .csv file that contains the complexity data to be analyzed.

    Parameters
    ----------
    number_of_xes_files : int
        the number of .xes files located in the folder specified in Constants.INPUT_PATH

    Returns
    -------
    str
        the command chosen by the user, or "I want to analyze the complexity scores in a .csv file."
        if the folder specified in Constants.INPUT_PATH does not contain any .xes files.
    """
    if number_of_xes_files == 0:
        print("There are no .xes files in the folder " + str(Constants.INPUT_PATH) + ", so I assume that you have the complexity data in a .csv file.")
        return Constants.use_data_from_file
    else:
        question = "How do you wish to collect the log complexity data to analyze?"
        return questionary.select(question, choices=[Constants.calculate_scores, Constants.use_data_from_file]).ask()

def ask_user_for_csv_file():
    """
    Asks the user to specify a path to a .csv file that contains complexity data.
    If the user instead inputs the string "X", the program aborts the execution.
    This function repeatedly asks the user to specify a filepath until they input
    one that ends with ".csv".

    Returns
    -------
    str
        the filepath to a .csv file specified by the user
    """
    selected_filepath = None
    while selected_filepath is None:
        # ask user for the .csv file containing complexity scores
        file_question = "Please specify where the .csv file containing complexity scores can be found."
        selected_filepath = questionary.path(file_question).ask()
        if selected_filepath.endswith("X"):
            print("Exiting the program.")
            exit()
        elif not selected_filepath.endswith(".csv"):
            selected_filepath = None
            print("Sorry, the selected file is not a .csv file. Please try again.")
    return selected_filepath

def ask_user_yes_no_question(question: str):
    """
    Asks the user the specified question and allows them to answer with
    either "yes" or "no". Returns the response chosen by the user.

    Parameters
    ----------
    question : str
        the yes / no question that the user should answer

    Returns
    -------
    str
        either the string "yes" or the string "no", depending on which one
        was chosen by the user
    """
    response = questionary.select(question, choices=["yes","no"]).ask()
    return response

def ask_user_for_integer(question: str):
    """
    Asks the user to input an integer number. If the input number cannot be
    converted into an int, the function asks the user again to input an integer
    number. This procedure is repeated until the user inputs an integer or the
    string "X", which aborts the execution of the program.

    Parameters
    ----------
    question : str
        the question that asks the user to input an integer number

    Returns
    -------
    int
        the integer number input by the user
    """
    response = questionary.text(question).ask()
    while True:
        if response == "X":
            print("Exiting the program.")
            exit()
        try:
            number = int(response)
            return number
        except ValueError:
            print("Invalid input: " + response + " cannot be converted to an integer.")
            print("Please try again.")

def ask_user_for_rotation(question: str):
    """
    Asks the user to choose one out of 8 rotation techniques.
    The available rotation techniques are:
    - varimax
    - promax
    - oblimin
    - oblimax
    - quartimin
    - quartimax
    - equamax
    - no rotation
    The resulting strings are used as a parameter for the functions of the
    library factor-analyzer and should not be altered.

    Parameters
    ----------
    question : str
        the question that asks the user to choose one of the rotation techniques

    Returns
    -------
    str
        one of the strings "varimax", "promax", "oblimin", "oblimax", "quartimin",
        "quartimax", "equamax", or "no rotation", depending on the user's choice
    """
    rotations = ['varimax', 'promax', 'oblimin', 'oblimax', 'quartimin', 'quartimax', 'equamax', 'no rotation']
    response = questionary.select(question, choices=rotations).ask()
    return response

def ask_user_for_log_measures(preselection = None):
    # reduce selectable measures to the passed preselection
    if preselection != None:
        Constants.simple_stats = [measure for measure in Constants.simple_stats if measure in preselection]
        Constants.trace_length = [measure for measure in Constants.trace_length if measure in preselection]
        Constants.trace_variant = [measure for measure in Constants.trace_variant if measure in preselection]
        Constants.activities = [measure for measure in Constants.activities if measure in preselection]
        Constants.start_activities = [measure for measure in Constants.start_activities if measure in preselection]
        Constants.end_activities = [measure for measure in Constants.end_activities if measure in preselection]
        Constants.eventropies = [measure for measure in Constants.eventropies if measure in preselection]
        Constants.epa_based = [measure for measure in Constants.epa_based if measure in preselection]
        Constants.trace_diversity = [measure for measure in Constants.trace_diversity if measure in preselection]
        Constants.distinct_activities = [measure for measure in Constants.distinct_activities if measure in preselection]
        Constants.repetitions = [measure for measure in Constants.repetitions if measure in preselection]
        Constants.comparison_based = [measure for measure in Constants.comparison_based if measure in preselection]
        Constants.dfg_based = [measure for measure in Constants.dfg_based if measure in preselection]
    # store the selectable measures, grouped by their FEEED-type
    measure_types = dict()
    measure_types['simple_stats'] = Constants.simple_stats
    measure_types['trace_length'] = Constants.trace_length
    measure_types['trace_variant'] = Constants.trace_variant
    measure_types['activities'] = Constants.activities
    measure_types['start_activities'] = Constants.start_activities
    measure_types['end_activities'] = Constants.end_activities
    measure_types['eventropies'] = Constants.eventropies
    measure_types['epa_based'] = Constants.epa_based
    measure_types['trace_diversity'] = Constants.trace_diversity
    measure_types['distinct_activities'] = Constants.distinct_activities
    measure_types['repetitions'] = Constants.repetitions
    measure_types['comparison_based'] = Constants.comparison_based
    measure_types['dfg_based'] = Constants.dfg_based
    question = "Please select which measures you would like to analyze."
    options = []
    for measure_type in measure_types.keys():
        options += [str(measure_type) + " (" + str(len(measure_types[measure_type])) + " selected)"]
    options += ["I want to analyze all available log measures."]
    questionary.select(question, choices=options).ask()
