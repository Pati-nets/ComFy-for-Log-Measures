import os
from gedi import gedi

target_folder = 'targets'
output_folder = 'data/'

chosen_intervals = {'n_traces': [10, 50000],
                    'n_unique_activities': [3, 400],
                    'n_events': [100, 500000],
                    'n_unique_start_activities': [1, 10],
                    'rel_unique_start_activities': [0, 1],
                    'start_activities_min': [1, 10000],
                    'start_activities_max': [1, 100000],
                    'start_activities_mean': [1, 10000],
                    'start_activities_median': [1, 10000],
                    'start_activities_std': [0, 10000],
                    'start_activities_variance': [0, 1000000],
                    'start_activities_q1': [1, 10000],
                    'start_activities_q3': [1, 10000],
                    'start_activities_iqr': [1, 10000],
                    'start_activities_skewness': [-1, 3],
                    'start_activities_kurtosis': [-2, 4],
                    'n_unique_end_activities': [1, 100],
                    'rel_unique_end_activities': [0, 1],
                    'end_activities_min': [1, 1400],
                    'end_activities_max': [1, 50000],
                    'end_activities_mean': [1, 5000],
                    'end_activities_median': [1, 3000],
                    'end_activities_std': [0, 10000],
                    'end_activities_variance': [0, 1000000],
                    'end_activities_q1': [1, 1000],
                    'end_activities_q3': [1, 5000],
                    'end_activities_iqr': [0, 4000],
                    'end_activities_skewness': [-1, 5],
                    'end_activities_kurtosis': [-2, 50],
                    'trace_len_min': [1, 20],
                    'trace_len_max': [1, 2000],
                    'trace_len_mean': [2, 50],
                    'trace_len_median': [1, 50],
                    'trace_len_mode': [1, 50],
                    'trace_len_std': [0, 30],
                    'trace_len_variance': [0, 1000],
                    'trace_len_q1': [1, 40],
                    'trace_len_q3': [1, 60],
                    'trace_len_iqr': [1, 20],
                    'trace_len_geometric_mean': [1, 50],
                    'trace_len_geometric_std': [0, 2],
                    'trace_len_harmonic_mean': [1, 50],
                    'trace_len_skewness': [-1, 20],
                    'trace_len_kurtosis': [-2, 1000],
                    'trace_len_coefficient_variation': [0, 2],
                    'trace_len_entropy': [0, 10],
                    'trace_len_hist1': [0, 1],
                    'trace_len_hist2': [0, 1],
                    'trace_len_hist3': [0, 1],
                    'trace_len_hist4': [0, 1],
                    'trace_len_hist5': [0, 1],
                    'trace_len_hist6': [0, 1],
                    'trace_len_hist7': [0, 1],
                    'trace_len_hist8': [0, 1],
                    'trace_len_hist9': [0, 1],
                    'trace_len_hist10': [0, 1],
                    'trace_len_skewness_hist': [-1, 2],
                    'trace_len_kurtosis_hist': [-2, 5],
                    'ratio_most_common_variant': [0, 1],
                    'ratio_top_1_variants': [0, 1],
                    'ratio_top_5_variants': [0.05, 1],
                    'ratio_top_10_variants': [0.1, 1],
                    'ratio_top_20_variants': [0.2, 1],
                    'ratio_top_50_variants': [0.5, 1],
                    'ratio_top_75_variants': [0.75, 1],
                    'mean_variant_occurrence': [1, 100],
                    'std_variant_occurrence': [0, 500],
                    'skewness_variant_occurrence': [-1, 50],
                    'kurtosis_variant_occurrence': [-2, 1000],
                    'activities_min': [1, 500],
                    'activities_max': [1, 100000],
                    'activities_mean': [1, 50000],
                    'activities_median': [1, 10000],
                    'activities_std': [0, 100000],
                    'activities_variance': [0, 1000000],
                    'activities_q1': [1, 100],
                    'activities_q3': [1, 10000],
                    'activities_iqr': [0, 10000],
                    'activities_skewness': [-1, 2],
                    'activities_kurtosis': [-2, 5],
                    'n_variants': [1, 10000],
                    'ratio_variants_per_number_of_traces': [0, 1],
                    'coverage_variants': [0, 10000],
                    'rel_coverage_variants': [0, 1],
                    'heterogeneity_rate_variants': [0, 1],
                    'similarity_rate_variants': [0, 1],
                    'distinct_activities_min': [1, 5],
                    'distinct_activities_max': [1, 100],
                    'distinct_activities_mean': [1, 50],
                    'distinct_activities_std': [0, 15],
                    'event_density': [0, 1],
                    'distinct_activities_non_overlap': [0, 1],
                    'complexity_factor': [0, 1000],
                    'simple_trace_diversity': [0, 1],
                    'advanced_trace_diversity': [0, 5],
                    'n_traces_with_loop': [0, 10000],
                    'avg_traces_with_loop': [0, 1],
                    'avg_loops_per_trace': [0, 5],
                    'max_loops_per_trace': [0, 100],
                    'avg_loop_size_per_trace': [0, 10],
                    'max_loop_size_per_trace': [0, 500],
                    'n_traces_with_repetition': [0, 10000],
                    'avg_traces_with_repetition': [0, 1],
                    'n_nodes_dfg': [0, 400],
                    'n_edges_dfg': [0, 5000],
                    'coeff_of_connectivity_dfg': [0, 15],
                    'avg_node_degree_dfg': [0, 30],
                    'max_node_degree_dfg': [0, 150],
                    'density_dfg': [0, 1],
                    'structure_dfg': [0, 1],
                    'cyclomatic_number_dfg': [0, 1000],
                    'n_cut_vertices_dfg': [0, 2],
                    'separability_ratio_dfg': [0, 1],
                    'sequentiality_ratio_dfg': [0, 1],
                    'cyclicity_dfg': [0, 1],
                    'number_of_successions': [1, 1000],
                    'number_of_ties': [1, 1000],
                    'structure': [0, 50],
                    'average_affinity': [0, 1],
                    'lempel_ziv_complexity': [1, 100000],
                    'deviation_from_random': [0, 10],
                    'average_edit_distance': [0, 50],
                    'eventropy_trace': [0, 10],
                    'eventropy_prefix': [0, 10],
                    'eventropy_prefix_flattened': [0, 10],
                    'eventropy_global_block': [0, 10],
                    'eventropy_global_block_flattened': [0, 10],
                    'eventropy_lempel_ziv': [0, 3],
                    'eventropy_lempel_ziv_flattened': [0, 3],
                    'eventropy_k_block_diff_1': [0, 5],
                    'eventropy_k_block_diff_3': [0, 2],
                    'eventropy_k_block_diff_5': [0, 5],
                    'eventropy_k_block_ratio_1': [0, 5],
                    'eventropy_k_block_ratio_3': [0, 3],
                    'eventropy_k_block_ratio_5': [0, 2],
                    'eventropy_knn_3': [0, 5],
                    'eventropy_knn_5': [0, 5],
                    'eventropy_knn_7': [0, 5],
                    'epa_variant_entropy': [0, 100000],
                    'epa_normalized_variant_entropy': [0, 1],
                    'epa_sequence_entropy': [0, 1000000],
                    'epa_normalized_sequence_entropy': [0, 1],
                    'epa_sequence_entropy_linear_forgetting': [0, 1000000],
                    'epa_normalized_sequence_entropy_linear_forgetting': [0, 1],
                    'epa_sequence_entropy_exponential_forgetting': [0, 1000000],
                    'epa_normalized_sequence_entropy_exponential_forgetting': [0, 1]
                    }

def generate_targets(log_measures: list):
    steps = 10
    outpath = 'data'
    n_trials = 50
    for measure in log_measures:
        f = open(target_folder + "/targets_" + str(measure) + ".json", "w")
        f.write("[\n")
        f.write("    {\n")
        f.write("        \"pipeline_step\": \"event_logs_generation\",\n")
        f.write("        \"output_path\": \"" + str(outpath) + "\",\n")
        f.write("        \"targets\": [\n")
        [min, max] = chosen_intervals[measure]
        for iteration in range(steps):
            value = min + iteration * ((max - min) / (steps - 1))
            f.write("            {\n")
            f.write("                \"" + str(measure) + "\": " + str(value) + "\n")
            f.write("            }")
            if iteration != steps - 1:
                f.write(",\n")
            else:
                f.write("\n")
        f.write("        ],\n")
        f.write("        \"config_space\": {\n")
        f.write("            \"mode\": [\n")
        f.write("                5,\n")
        f.write("                20\n")
        f.write("            ],\n")
        f.write("            \"sequence\": [\n")
        f.write("                0.01,\n")
        f.write("                1\n")
        f.write("            ],\n")
        f.write("            \"choice\": [\n")
        f.write("                0.01,\n")
        f.write("                1\n")
        f.write("            ],\n")
        f.write("            \"parallel\": [\n")
        f.write("                0.01,\n")
        f.write("                1\n")
        f.write("            ],\n")
        f.write("            \"loop\": [\n")
        f.write("                0.01,\n")
        f.write("                1\n")
        f.write("            ],\n")
        f.write("            \"silent\": [\n")
        f.write("                0.01,\n")
        f.write("                1\n")
        f.write("            ],\n")
        f.write("            \"lt_dependency\": [\n")
        f.write("                0.01,\n")
        f.write("                1\n")
        f.write("            ],\n")
        f.write("            \"num_traces\": [\n")
        f.write("                10,\n")
        f.write("                10001\n")
        f.write("            ],\n")
        f.write("            \"duplicate\": [\n")
        f.write("                0\n")
        f.write("            ],\n")
        f.write("            \"or\": [\n")
        f.write("                0\n")
        f.write("            ]\n")
        f.write("        },\n")
        f.write("        \"system_params\": {\n")
        f.write("            \"output_path\": \"" + str(outpath) + "\",\n")
        f.write("            \"n_trials\": " + str(n_trials) + "\n")
        f.write("        }\n")
        f.write("    }\n")
        f.write("]\n")
        f.close()

def generate_event_logs(log_measures: list):
    for measure in log_measures:
        target_file = os.path.join(target_folder, "targets_" + str(measure) + ".json")
        gedi(target_file)
        for folder in os.listdir(output_folder):
            if os.path.isdir(os.path.join(output_folder, folder)):
                if str(folder).startswith("1"):
                    os.rename(os.path.join(output_folder, folder), os.path.join(output_folder, measure))


if __name__ == "__main__":
    #####
    simple_stats = ['n_traces', 'n_variants', 'ratio_variants_per_number_of_traces', 'n_events']
    #####
    trace_length = ['trace_len_min', 'trace_len_max', 'trace_len_mean', 'trace_len_median', 'trace_len_mode',
                    'trace_len_std', 'trace_len_variance', 'trace_len_q1', 'trace_len_q3', 'trace_len_iqr',
                    'trace_len_geometric_mean',
                    #'trace_len_geometric_std', # throws exception
                    'trace_len_harmonic_mean',
                    #'trace_len_skewness', # throws exception
                    'trace_len_kurtosis', 'trace_len_coefficient_variation',
                    'trace_len_entropy', 'trace_len_hist1', 'trace_len_hist2', 'trace_len_hist3',
                    'trace_len_hist4', 'trace_len_hist5', 'trace_len_hist6', 'trace_len_hist7',
                    'trace_len_hist8', 'trace_len_hist9', 'trace_len_hist10', 'trace_len_skewness_hist',
                    'trace_len_kurtosis_hist']
    #####
    trace_variant = ['ratio_most_common_variant', 'ratio_top_1_variants', 'ratio_top_5_variants',
                     'ratio_top_10_variants', 'ratio_top_20_variants', 'ratio_top_50_variants',
                     'ratio_top_75_variants', 'mean_variant_occurrence', 'std_variant_occurrence',
                     #'skewness_variant_occurrence', # throws exception
                     #'kurtosis_variant_occurrence', # throws exception
                     'coverage_variants',
                     'rel_coverage_variants', 'heterogeneity_rate_variants',
                     #'similarity_rate_variants' # throws exception
                     ]
    #####
    activities = ['n_unique_activities', 'activities_min', 'activities_max',
                  'activities_mean', 'activities_median',
                  #'activities_std', # blocks
                  'activities_variance', 'activities_q1',
                  'activities_q3', 'activities_iqr',
                  #'activities_skewness', # throws exception
                  #'activities_kurtosis' # throws exception
                  ]
    #####
    start_activities = ['n_unique_start_activities', 'start_activities_min', 'start_activities_max',
                        'start_activities_mean', 'start_activities_median', 'start_activities_std',
                        'start_activities_variance', 'start_activities_q1', 'start_activities_q3',
                        'start_activities_iqr',
                        #'start_activities_skewness', # throws excetpion
                        #'start_activities_kurtosis', # throws exception
                        'rel_unique_start_activities']
    #####
    end_activities = ['n_unique_end_activities', 'end_activities_min', 'end_activities_max',
                      'end_activities_mean', 'end_activities_median', 'end_activities_std',
                      'end_activities_variance', 'end_activities_q1', 'end_activities_q3',
                      'end_activities_iqr',
                      #'end_activities_skewness', # throws exception
                      #'end_activities_kurtosis', # throws exception
                      'rel_unique_end_activities']
    #####
    eventropies = ['eventropy_trace', 'eventropy_prefix', 'eventropy_prefix_flattened',
                   #'eventropy_global_block', # waits for infinity
                   #'eventropy_global_block_flattened', # waits for infinity
                   'eventropy_lempel_ziv', 'eventropy_lempel_ziv_flattened',
                   'eventropy_k_block_diff_1', 'eventropy_k_block_diff_3', 'eventropy_k_block_diff_5',
                   'eventropy_k_block_ratio_1', 'eventropy_k_block_ratio_3', 'eventropy_k_block_ratio_5',
                   #'eventropy_knn_3', # many list indices out of range and throws exception
                   #'eventropy_knn_5', # many list indices out of range and throws exception
                   #'eventropy_knn_7' # many list indices out of range and throws exception
                   ]
    #####
    epa_based = ['epa_variant_entropy', 'epa_normalized_variant_entropy', 'epa_sequence_entropy',
                 'epa_normalized_sequence_entropy', 'epa_sequence_entropy_linear_forgetting',
                 'epa_normalized_sequence_entropy_linear_forgetting', 'epa_sequence_entropy_exponential_forgetting',
                 'epa_normalized_sequence_entropy_exponential_forgetting']
    #####
    trace_diversity = ['simple_trace_diversity', 'advanced_trace_diversity']
    #####
    distinct_activities = ['distinct_activities_min', 'distinct_activities_max',
                           #'distinct_activities_mean', # hangs up during export
                           'distinct_activities_std', 'event_density',
                           #'distinct_activities_non_overlap', # throws many exceptions
                           #'complexity_factor' # throws exception
                           ]
    #####
    repetitions = ['n_traces_with_loop', 'avg_traces_with_loop', 'avg_loops_per_trace', 'max_loops_per_trace',
                   'avg_loop_size_per_trace', 'max_loop_size_per_trace', 'n_traces_with_repetition', 'avg_traces_with_repetition']
    #####
    comparison_based = ['number_of_successions', 'number_of_ties', 'structure', 'average_affinity',
                        'lempel_ziv_complexity', 'deviation_from_random',
                        #'average_edit_distance' # waits for infinity
                        ]
    #####
    dfg_based = [#'n_nodes_dfg', # throws exception
                 #'n_edges_dfg', # throws exception
                 #'coeff_of_connectivity_dfg', # throws exception
                 'avg_node_degree_dfg', 'max_node_degree_dfg',
                 'density_dfg', 'structure_dfg', 'cyclomatic_number_dfg', 'n_cut_vertices_dfg', 'separability_ratio_dfg',
                 'sequentiality_ratio_dfg', 'cyclicity_dfg']

    log_measures = comparison_based
    generate_event_logs(log_measures)
