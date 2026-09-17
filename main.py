import Constants # for responses that the user can give on the required data
import UserInteraction # to ask the user questions about how to perform the analysis
import MeasureEvaluator # to calculate the scores returned by log measures
import FactorAnalysis # to perform the factor analysis on log measure data
import LatexExporter # to export the results of the factor analysis to LaTeX

def perform_factor_analysis():
    n_xes, n_csv = UserInteraction.print_welcome_message()
    source = UserInteraction.ask_user_for_source(n_xes)
    complexity = None
    population = 0
    measures = None
    measures_to_analyze = None
    if source == Constants.calculate_scores:
        measures = UserInteraction.ask_user_for_log_measures()
        complexity, population = MeasureEvaluator.collect_log_measure_data(measures)
    elif source == Constants.use_data_from_file:
        file = UserInteraction.ask_user_for_csv_file()
        complexity, population, measures = MeasureEvaluator.import_data_from_csv_file(file)
        selected_measures = UserInteraction.ask_user_for_log_measures(measures)
        exclude = [measure for measure in measures if measure not in selected_measures]
        complexity = complexity.drop(columns=exclude)
        measures = selected_measures
    else:
        raise Exception("Sorry, I do not know the command " + str(source) + ".")
    CFA = FactorAnalysis.ComplexityFactorAnalysis(complexity)
    CFA.prepare_data_for_factor_analysis()
    bartlett_ok = CFA.execute_Bartletts_test_of_sphericity()
    if not bartlett_ok:
        response = UserInteraction.ask_user_yes_no_question("Do you wish to proceed anyway?")
        if response == "no":
            print("Exiting program. Goodbye!")
            exit()
    msa_ok = CFA.repeat_calculate_measure_of_sampling_adequacy()
    print("\nNow, let us perform the statistical analysis.")
    print("I will next ask you for the number of factors you expect.")
    show_scree_answer = UserInteraction.ask_user_yes_no_question("Do you want to see a Scree plot to make an informed decision about the number of factors?")
    show_scree_plot = False
    if show_scree_answer == "yes":
        show_scree_plot = True
    CFA.calculate_scree_plot(show_scree_plot)
    expected_factors = UserInteraction.ask_user_for_integer("Please enter the number of factors you expect.")
    rotation_answer = UserInteraction.ask_user_for_rotation("Which rotation do you want to perform on the data?")
    rotation = None
    if rotation_answer != 'no rotation':
        rotation = rotation_answer
    print("\nI will now perform the factor analysis.")
    response = UserInteraction.ask_user_yes_no_question("Do you want the results to appear on the command line?")
    show_results = False
    if response == "yes":
        show_results = True
    CFA.perform_factor_analysis(expected_factors, rotation=rotation, show_plot=show_results)
    print("\nI will now export the results of the factor analysis to a LaTeX file.")
    latex_exporter = LatexExporter.LatexExporter(CFA, measures, population)
    latex_exporter.export()

if __name__ == "__main__":
    perform_factor_analysis()
