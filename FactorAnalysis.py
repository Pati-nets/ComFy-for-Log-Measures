import pandas # for collecting data
import inspect
import factor_analyzer.factor_analyzer as factor_analyzer_module
from factor_analyzer.factor_analyzer import calculate_kmo, FactorAnalyzer
from factor_analyzer.utils import corr as compute_correlation_matrix
from scipy.stats import chi2
from sklearn.decomposition import FactorAnalysis, PCA
from sklearn.preprocessing import StandardScaler
from sklearn.utils import check_array as sklearn_check_array
import matplotlib.pyplot as plt
import math
import numpy as np
import numbers
import Constants

def _check_array_compat(x, force_all_finite=None, **kwargs):
    # Patch force_all_finite kwarg to recent name in scikit learn after 1.8.
    if force_all_finite is not None:
        accepted_parameters = inspect.signature(sklearn_check_array).parameters
        if "ensure_all_finite" in accepted_parameters:
            kwargs["ensure_all_finite"] = force_all_finite
        elif "force_all_finite" in accepted_parameters:
            kwargs["force_all_finite"] = force_all_finite
    return sklearn_check_array(x, **kwargs)

# FactorAnalyzer.fit()/transform() call check_array through this module-level name.
factor_analyzer_module.check_array = _check_array_compat

def find_non_numeric_variables(data: pandas.DataFrame):
    to_remove = []
    for column in list(data.columns):
        values = list(data[column])
        for index in range(len(values)):
            if column not in to_remove and (not isinstance(values[index], numbers.Number) or math.isnan(values[index]) or math.isinf(values[index])):
                print("The measure " + Constants.FAILURE_COLOR + str(column) + Constants.RESET_COLOR + " features the non-numeric value " + str(values[index]) + ".")
                to_remove += [column]
    return to_remove

def find_variables_with_no_variance(data: pandas.DataFrame):
    to_remove = []
    for column in list(data.columns):
        std = data[column].std(ddof=0)
        if column not in to_remove and np.isclose(std, 0.0):
            print("The measure " + Constants.FAILURE_COLOR + str(column) + Constants.RESET_COLOR + " has standard deviation " + str(std) + " and thus does not feature enough variance.")
            to_remove += [column]
    return to_remove

def find_perfectly_correlated_variables(data: pandas.DataFrame):
    to_remove = []
    pairwise_absolute_correlations = data.corr().abs()
    columns = list(pairwise_absolute_correlations.columns)
    rows = list(pairwise_absolute_correlations)
    for i in range(0, len(rows)):
        row = rows[i]
        if row not in to_remove:
            for j in range(i+1, len(columns)):
                column = columns[j]
                if column not in to_remove:
                    if np.isclose(pairwise_absolute_correlations[row][column], 1.0):
                        print("The measure " + Constants.FAILURE_COLOR + str(column) + Constants.RESET_COLOR + " is perfectly correlated with the measure " + str(row) + ".")
                        to_remove += [column]
    return to_remove

class ComplexityFactorAnalysis:
    def __init__(self, complexity_data):
        self.full_complexity_data = complexity_data
        self.complexity_data = complexity_data
        self.non_numeric_variables = []
        self.zero_variance_variables = []
        self.correlated_variables = []
        self.bartlett_chi_squared = None
        self.bartlett_p_value = None
        self.msa_per_variable = []
        self.msa_insufficient_variables = {}
        self.overall_msa = None
        self.factor_analyzer = None
        self.factor_loadings = None
        self.communalities = None
        self.pca_explained_variance_ratio = []
        self.number_of_factors = None
        self.descriptive_statistics = None
        self.rotation = None

    def show_descriptive_stats(self):
        stats = pandas.DataFrame({"Mean": self.full_complexity_data.mean(), "Median": self.full_complexity_data.median(), "Std": self.full_complexity_data.std(), "Min": self.full_complexity_data.min(), "Max": self.full_complexity_data.max()})
        print("\nDescriptive statistics of the data:")
        print(stats)

    def prepare_data_for_factor_analysis(self):
        self.non_numeric_variables = find_non_numeric_variables(self.complexity_data)
        print("Removing non-numeric variables...")
        self.complexity_data = self.complexity_data.drop(columns = self.non_numeric_variables)
        self.zero_variance_variables = find_variables_with_no_variance(self.complexity_data)
        print("Removing variables with no variance...")
        self.complexity_data = self.complexity_data.drop(columns = self.zero_variance_variables)
        self.correlated_variables = find_perfectly_correlated_variables(self.complexity_data)
        print("Removing variables that are correlated with others...")
        self.complexity_data = self.complexity_data.drop(columns = self.correlated_variables)

    def execute_Bartletts_test_of_sphericity(self):
        print("\nNext, I will perform Bartlett's test of sphericity to check whether there are interdependencies between the variables.")
        # initialize a variable to store whether Bartlett's test of spericity succeeded.
        bartlett_ok = True
        # Bartlett's test needs log(det(correlation matrix)). We execute the test with the python library factor_analyzer, but avoiding log(det)--> NaN
        
        correlation_matrix = compute_correlation_matrix(self.complexity_data)
        eigenvalues, eigenvectors = np.linalg.eigh(correlation_matrix)
        near_singular = eigenvalues < Constants.eigenvalue_floor
        if np.any(near_singular):
            print(Constants.FAILURE_COLOR, end="")
            print("Warning: the correlation matrix is numerically (near-)singular (" + str(near_singular.sum()) + " eigenvalue(s) below " + str(Constants.eigenvalue_floor) + ").")
            print("Each near-zero eigenvalue corresponds to a near-perfect linear dependency between a handful of variables.")
            print("The variables with the largest weight in that dependency, per eigenvalue, are:")
            columns = list(self.complexity_data.columns)
            for index in np.where(near_singular)[0]:
                loadings = eigenvectors[:, index]
                # keep the top variables by |loading| until their squared loadings cover the configured fraction of the eigenvector's total.
                order = np.argsort(-np.abs(loadings))
                cumulative_squared_loadings = np.cumsum(loadings[order] ** 2)
                cutoff = np.searchsorted(cumulative_squared_loadings, Constants.eigenvector_loading_coverage_threshold) + 1
                top_variables = ", ".join(str(columns[i]) for i in order[:cutoff])
                print("  - eigenvalue " + str(eigenvalues[index]) + ": " + top_variables)
            print("Clamping the offending eigenvalue(s) to " + str(Constants.eigenvalue_floor) + " to keep the test result well-defined and reproducible.")
            print(Constants.RESET_COLOR, end="")
            eigenvalues = np.clip(eigenvalues, Constants.eigenvalue_floor, None)
        # Bartlett formula using the new eigenvalues.
        n, p = self.complexity_data.shape
        log_determinant = np.sum(np.log(eigenvalues))
        self.bartlett_chi_squared = -log_determinant * (n - 1 - (2 * p + 5) / 6)
        degrees_of_freedom = p * (p - 1) / 2
        self.bartlett_p_value = chi2.sf(self.bartlett_chi_squared, degrees_of_freedom)
        # inform the user about the resulting values.
        print("chi squared value:", self.bartlett_chi_squared)
        print("p-value:", self.bartlett_p_value)
        # inform the user whether Bartlett's test of spericity succeeded or not.
        if self.bartlett_p_value < Constants.bartlett_p_value_threshold:
            print(Constants.SUCCESS_COLOR, end="")
            print("Bartlett's test of sphericity succeeded!")
            print("Since the p-value " + str(self.bartlett_p_value) + " is lower than " + str(Constants.bartlett_p_value_threshold) + ", we can be fairly certain that the variables are correlated.")
            print(Constants.RESET_COLOR, end="")
        else:
            print(Constants.FAILURE_COLOR, end="")
            print("Bartlett's test of sphericity failed!")
            print("Since the p-value " + str(self.bartlett_p_value) + " is higher than " + str(Constants.bartlett_p_value_threshold) + ", we cannot be sure that the variables are correlated.")
            print("Performing a factor analysis on these data is not recommended.")
            # store that Bartlett's test of sphericity did not succeed
            bartlett_ok = False
            print(Constants.RESET_COLOR, end="")
        # return whether the test was successful or not.
        return bartlett_ok

    def calculate_measure_of_sampling_adequacy(self):
        # check if the data set does not contain any entries.
        if len(self.complexity_data) == 0:
            # if so, return a boolean indicating that the MSA is insufficient.
            return False
        # create a list for the variables with insufficient MSA.
        insufficient_msa = []
        # create a boolean indicating whether the overall MSA is sufficient.
        overall_msa_sufficient = True
        # calculate the measure of sampling adequacy using the python library factor_analyzer.
        self.msa_per_variable, self.overall_msa = calculate_kmo(self.complexity_data)
        # inform the user about the results.
        print("variable-specific MSA:")
        index = 0
        # go through all complexity measures.
        for column in self.complexity_data:
            # collect the msa value of the current complexity measure.
            msa_value = self.msa_per_variable[index]
            # print the name of the complexity measure.
            print("- " + str(column) + ": ", end="")
            # print the value in red if it is below a given threshold
            if msa_value < Constants.msa_threshold:
                print(Constants.FAILURE_COLOR, end="")
                # add the current measure and its msa value to the list of variables with insufficient msa.
                self.msa_insufficient_variables[column] = msa_value
                insufficient_msa += [column]
            # print the value in green if it is above or equal to the given threshold.
            else:
                print(Constants.SUCCESS_COLOR, end="")
            print(self.msa_per_variable[index])
            # increment the index for the next complexity measure.
            index += 1
            print(Constants.RESET_COLOR, end="")
        # inform the user about the overall msa value.
        print("overall MSA: ", end="")
        # print the value in red if it is below the given threshold.
        if self.overall_msa < Constants.msa_threshold:
            print(Constants.FAILURE_COLOR, end="")
            # store that the overall msa was not sufficient.
            overall_msa_sufficient = False
        # print the value in green if it is above or equal to the given threshold.
        else:
            print(Constants.SUCCESS_COLOR, end="")
        print(self.overall_msa)
        print(Constants.RESET_COLOR, end="")
        # check if the msa returned only positive values.
        if len(insufficient_msa) == 0 and self.overall_msa >= Constants.msa_threshold:
            # if so, inform the user that performing a factor analysis will be valid.
            print(Constants.SUCCESS_COLOR, end="")
            print("Since all MSA values are greater than or equal to " + str(Constants.msa_threshold) + ", we can be fairly certain that the variables are correlated.")
            print(Constants.RESET_COLOR, end="")
        return overall_msa_sufficient, insufficient_msa

    def repeat_calculate_measure_of_sampling_adequacy(self):
        print("\nNext, I will calculate the measure of sampling adequacy...")
        # calculate the measure of sampling adequacy for the given dataset.
        msa_ok, insufficient_msa = self.calculate_measure_of_sampling_adequacy()
        # repeat the calculation until no new variables with insufficient msa emerged.
        while len(insufficient_msa) != 0:
            print("It seems there is a variable whose MSA value is too low.")
            print("I will now remove this variable from the analysis.")
            # remove the variables with insufficient msa values from the analysis.
            self.complexity_data = self.complexity_data.drop(columns=insufficient_msa)
            if len(self.complexity_data) <= 1:
                print("There is at most one variable left, so the MSA test failed.")
                return False
            print("Now, I will recalculate the measure of sampling adequacy...")
            # calculate the new msa values.
            msa_ok, insufficient_msa = self.calculate_measure_of_sampling_adequacy()
            # abort if the overall msa value is below the threshold at any time.
            if not msa_ok:
                print(Constants.FAILURE_COLOR, end="")
                print("Sorry, the overall measure of sampling adequacy is too low.")
                print("Since the overall msa value " + str(self.overall_msa) + " is lower than " + str(Constants.msa_threshold) + ", we cannot be sure that the variables are correlated.")
                print("Performing a factor analysis on these data is not recommended.")
                print(Constants.RESET_COLOR, end="")
        return msa_ok

    def calculate_scree_plot(self, show_plot=False):
        # fit the standard scaler to the data.
        scaler = StandardScaler()
        scaler.fit(self.complexity_data)
        # transform the data with the scaler.
        # this means: for each column, calculate the mean m and the standard deviation d.
        # then, the new entry of a cell is x_new = (x_old - m) / d.
        transformed_data = scaler.transform(self.complexity_data)
        # initialize a principal component analyzer with components equal to the number of complexity measures.
        principal_component_analyzer = PCA(n_components=len(list(self.complexity_data)))
        # fit the principal component analyzer to the data.
        pca_fit = principal_component_analyzer.fit(transformed_data)
        # store the explained variance ratio returned by the pricipal component analysis.
        self.pca_explained_variance_ratio = principal_component_analyzer.explained_variance_ratio_
        # if the user chose to display the results, create a plot and show it.
        if show_plot:
            PC_values = np.arange(principal_component_analyzer.n_components_) + 1
            plt.plot(PC_values, self.pca_explained_variance_ratio, 'o-', linewidth=2, color='blue')
            plt.title('Scree Plot')
            plt.xlabel('Factor Number')
            plt.ylabel('Variance Explained')
            plt.show()

    def perform_factor_analysis(self, expected_number_of_factors, rotation='varimax', show_plot=False, show_values=False):
        self.number_of_factors = expected_number_of_factors
        # collect descriptive statistics of the complexity values.
        self.descriptive_statistics = pandas.DataFrame({"Mean": self.full_complexity_data.mean(), "Median": self.full_complexity_data.median(), "Std": self.full_complexity_data.std(), "Min": self.full_complexity_data.min(), "Max": self.full_complexity_data.max()})
        # initialize a factor analyzer with the specified number of factors and the specified rotation.
        self.factor_analyzer = FactorAnalyzer(n_factors=expected_number_of_factors, rotation=rotation)
        self.rotation = rotation
        # perform the factor analysis on the complexity data.
        self.factor_analyzer.fit(self.complexity_data)
        # store the resulting factor loadings into a matrix.
        self.factor_loadings = self.factor_analyzer.loadings_
        # store the communalities for each variable in a list.
        self.communalities = self.factor_analyzer.get_communalities()
        if show_plot:
            # plot the data as a heat map.
            fig, axis = plt.subplots(figsize=(7,10))
            im = axis.imshow(self.factor_loadings, cmap="RdBu_r", vmax=1, vmin=-1)
            if show_values:
                # and add the corresponding value to the center of each cell.
                for (i,j), z in np.ndenumerate(self.factor_loadings):
                    axis.text(j, i, str(z.round(2)), ha="center", va="center")
            # tell matplotlib about the metadata of the plot.
            axis.set_yticks(np.arange(len(list(self.complexity_data))))
            if axis.get_subplotspec().is_first_col():
                axis.set_yticklabels(list(self.complexity_data))
            else:
                axis.set_yticklabels([])
            axis.set_title("Varimax Factor Analysis")
            axis.set_xticks(range(expected_number_of_factors))
            factor_names = []
            for i in range(1, expected_number_of_factors + 1):
                factor_names += ["F" + str(i)]
            axis.set_xticklabels(factor_names)
            # and squeeze the axes tight, to save space.
            plt.tight_layout()
            # add a colorbar.
            cb = fig.colorbar(im, ax=axis, location='right', label="loadings")
            # show the plot.
            plt.show()
            # calculate the communalities as the sum of squared values in the loading matrix
            # for each complexity measure. The communalities then show how much of the data
            # for a complexity measure can be explained by the factors.
            communalities = pandas.Series(self.communalities, index=list(self.complexity_data))
            # plot the communalities as a bar diagram.
            communalities.plot(kind="bar", ylabel="Communalities")
            # show the plot.
            plt.show()
