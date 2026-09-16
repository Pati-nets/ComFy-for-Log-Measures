import pandas 
import Constants
import numpy as np

latex_command = {'n_traces': r'\length',
                 'n_unique_activities': r'\variety',
                 'n_events': r'\magnitude',
                 'n_unique_start_activities': r'\startactivities',
                 'rel_unique_start_activities': r'\startactivitiesrel',
                 'start_activities_min': r'\startmin',
                 'start_activities_max': r'\startmax',
                 'start_activities_mean': r'\startmean',
                 'start_activities_median': r'\startmedian',
                 'start_activities_std': r'\startdev',
                 'start_activities_variance': r'\startvar',
                 'start_activities_q1': r'\startqone',
                 'start_activities_q3': r'\startqthree',
                 'start_activities_iqr': r'\startiqr',
                 'start_activities_skewness': r'\startskew',
                 'start_activities_kurtosis': r'\startkurt',
                 'n_unique_end_activities': r'\lastactivities',
                 'rel_unique_end_activities': r'\lastactivitiesrel',
                 'end_activities_min': r'\lastmin',
                 'end_activities_max': r'\lastmax',
                 'end_activities_mean': r'\lastmean',
                 'end_activities_median': r'\lastmedian',
                 'end_activities_std': r'\lastdev',
                 'end_activities_variance': r'\lastvar',
                 'end_activities_q1': r'\lastqone',
                 'end_activities_q3': r'\lastqthree',
                 'end_activities_iqr': r'\lastiqr',
                 'end_activities_skewness': r'\lastskew',
                 'end_activities_kurtosis': r'\lastkurt',
                 'trace_len_min': r'\tlmin',
                 'trace_len_max': r'\tlmax',
                 'trace_len_mean': r'\tlavg',
                 'trace_len_median': r'\tlmed',
                 'trace_len_mode': r'\tlmode',
                 'trace_len_std': r'\tldev',
                 'trace_len_variance': r'\tlvar',
                 'trace_len_q1': r'\tlqone',
                 'trace_len_q3': r'\tlqthree',
                 'trace_len_iqr': r'\tliqr',
                 'trace_len_geometric_mean': r'\tlgmean',
                 'trace_len_geometric_std': r'\tlgdev',
                 'trace_len_harmonic_mean': r'\tlhmean',
                 'trace_len_skewness': r'\tlskewness',
                 'trace_len_kurtosis': r'\tlkurtosis',
                 'trace_len_coefficient_variation': r'\tlcvariation',
                 'trace_len_entropy': r'\tlentropy',
                 'trace_len_hist1': r'\tlhistone',
                 'trace_len_hist2': r'\tlhisttwo',
                 'trace_len_hist3': r'\tlhistthree',
                 'trace_len_hist4': r'\tlhistfour',
                 'trace_len_hist5': r'\tlhistfive',
                 'trace_len_hist6': r'\tlhistsix',
                 'trace_len_hist7': r'\tlhistseven',
                 'trace_len_hist8': r'\tlhisteight',
                 'trace_len_hist9': r'\tlhistnine',
                 'trace_len_hist10': r'\tlhistten',
                 'trace_len_skewness_hist': r'\tlskewhist',
                 'trace_len_kurtosis_hist': r'\tlkurthist',
                 'ratio_most_common_variant': r'\freqmaxr',
                 'ratio_top_1_variants': r'\freqmaxone',
                 'ratio_top_5_variants': r'\freqmaxfive',
                 'ratio_top_10_variants': r'\freqmaxten',
                 'ratio_top_20_variants': r'\freqmaxtwenty',
                 'ratio_top_50_variants': r'\freqmaxfifty',
                 'ratio_top_75_variants': r'\freqmaxseventyfive',
                 'mean_variant_occurrence': r'\freqmean',
                 'std_variant_occurrence': r'\freqdev',
                 'skewness_variant_occurrence': r'\freqskew',
                 'kurtosis_variant_occurrence': r'\freqkurt',
                 'activities_min': r'\actfreqmin',
                 'activities_max': r'\actfreqmax',
                 'activities_mean': r'\actfreqmean',
                 'activities_median': r'\actfreqmedian',
                 'activities_std': r'\actfreqdev',
                 'activities_variance': r'\actfreqvar',
                 'activities_q1': r'\actfreqqone',
                 'activities_q3': r'\actfreqqthree',
                 'activities_iqr': r'\actfreqiqr',
                 'activities_skewness': r'\actfreqskew',
                 'activities_kurtosis': r'\actfreqkurt',
                 'n_variants': r'\numberuniquetraces',
                 'ratio_variants_per_number_of_traces': r'\percentageuniquetraces',
                 'coverage_variants': r'\dtcov',
                 'rel_coverage_variants': r'\dtrelcov',
                 'heterogeneity_rate_variants': r'\dthet',
                 'similarity_rate_variants': r'\dtsim',
                 'distinct_activities_min': r'\damin',
                 'distinct_activities_max': r'\damax',
                 'distinct_activities_mean': r'\daavg',
                 'distinct_activities_std': r'\dadev',
                 'event_density': r'\dadens',
                 'distinct_activities_non_overlap': r'\daoverlap',
                 'complexity_factor': r'\complexityfactor',
                 'simple_trace_diversity': r'\simpletracediv',
                 'advanced_trace_diversity': r'\advtracediv',
                 'n_traces_with_loop': r'\loopnum',
                 'avg_traces_with_loop': r'\looprelnum',
                 'avg_loops_per_trace': r'\loopavg',
                 'max_loops_per_trace': r'\loopmax',
                 'avg_loop_size_per_trace': r'\loopavgsize',
                 'max_loop_size_per_trace': r'\loopmaxsize',
                 'n_traces_with_repetition': r'\repnum',
                 'avg_traces_with_repetition': r'\reprelnum',
                 'n_nodes_dfg': r'\dfgnodes',
                 'n_edges_dfg': r'\dfgedges',
                 'coeff_of_connectivity_dfg': r'\dfgcnc',
                 'avg_node_degree_dfg': r'\dfgavgdeg',
                 'max_node_degree_dfg': r'\dfgmaxdeg',
                 'density_dfg': r'\dfgdens',
                 'structure_dfg': r'\dfgstruct',
                 'cyclomatic_number_dfg': r'\dfgcycnumber',
                 'n_cut_vertices_dfg': r'\dfgsepnum',
                 'separability_ratio_dfg': r'\dfgsepratio',
                 'sequentiality_ratio_dfg': r'\dfgseqratio',
                 'cyclicity_dfg': r'\dfgcyc',
                 'number_of_successions': r'\numberofneighborhoods',
                 'number_of_ties': r'\numberofties',
                 'structure': r'\structure',
                 'average_affinity': r'\affinity',
                 'lempel_ziv_complexity': r'\lempelziv',
                 'deviation_from_random': r'\deviationfromrandom',
                 'average_edit_distance': r'\avgdist',
                 'eventropy_trace': r'\enttrace',
                 'eventropy_prefix': r'\entprefix',
                 'eventropy_prefix_flattened': r'\entprefixflat',
                 'eventropy_global_block': r'\entgblock',
                 'eventropy_global_block_flattened': r'\entgblockflat',
                 'eventropy_lempel_ziv': r'\entlempelziv',
                 'eventropy_lempel_ziv_flattened': r'\entlempelzivflat',
                 'eventropy_k_block_diff_1': r'\entkblockdone',
                 'eventropy_k_block_diff_3': r'\entkblockdthree',
                 'eventropy_k_block_diff_5': r'\entkblockdfive',
                 'eventropy_k_block_ratio_1': r'\entkblockrone',
                 'eventropy_k_block_ratio_3': r'\entkblockrthree',
                 'eventropy_k_block_ratio_5': r'\entkblockrfive',
                 'eventropy_knn_3': r'\entknnthree',
                 'eventropy_knn_5': r'\entknnfive',
                 'eventropy_knn_7': r'\entknnseven',
                 'epa_variant_entropy': r'\epavariant',
                 'epa_normalized_variant_entropy': r'\epanormvariant',
                 'epa_sequence_entropy': r'\epasequence',
                 'epa_normalized_sequence_entropy': r'\epanormsequence',
                 'epa_sequence_entropy_linear_forgetting': r'\epasequencel',
                 'epa_normalized_sequence_entropy_linear_forgetting': r'\epanormsequencel',
                 'epa_sequence_entropy_exponential_forgetting': r'\epasequencee',
                 'epa_normalized_sequence_entropy_exponential_forgetting': r'\epanormsequencee'
                 }
log_measures = list(latex_command.keys())
measure_codes =  r'\newcommand{\magnitudename}{\text{mag}}' + "\n"
measure_codes += r'\newcommand{\magnitude}{C_{\magnitudename}}' + "\n"
measure_codes += r'\newcommand{\varietyname}{\text{var}}' + "\n"
measure_codes += r'\newcommand{\variety}{C_{\varietyname}}' + "\n"
measure_codes += r'\newcommand{\lengthname}{\text{len}}' + "\n"
measure_codes += r'\newcommand{\length}{C_{\lengthname}}' + "\n"
measure_codes += r'\newcommand{\startactivitiesname}{\text{A-start-\#}}' + "\n"
measure_codes += r'\newcommand{\startactivities}{C_{\startactivitiesname}}' + "\n"
measure_codes += r'\newcommand{\startactivitiesrelname}{\text{A-start-rel}}' + "\n"
measure_codes += r'\newcommand{\startactivitiesrel}{C_{\startactivitiesrelname}}' + "\n"
measure_codes += r'\newcommand{\startminname}{\text{A-start-min}}' + "\n"
measure_codes += r'\newcommand{\startmin}{C_{\startminname}}' + "\n"
measure_codes += r'\newcommand{\startmaxname}{\text{A-start-max}}' + "\n"
measure_codes += r'\newcommand{\startmax}{C_{\startmaxname}}' + "\n"
measure_codes += r'\newcommand{\startmeanname}{\text{A-start-mean}}' + "\n"
measure_codes += r'\newcommand{\startmean}{C_{\startmeanname}}' + "\n"
measure_codes += r'\newcommand{\startmedianname}{\text{A-start-med}}' + "\n"
measure_codes += r'\newcommand{\startmedian}{C_{\startmedianname}}' + "\n"
measure_codes += r'\newcommand{\startdevname}{\text{A-start-dev}}' + "\n"
measure_codes += r'\newcommand{\startdev}{C_{\startdevname}}' + "\n"
measure_codes += r'\newcommand{\startvarname}{\text{A-start-var}}' + "\n"
measure_codes += r'\newcommand{\startvar}{C_{\startvarname}}' + "\n"
measure_codes += r'\newcommand{\startqonename}{\text{A-start-Q1}}' + "\n"
measure_codes += r'\newcommand{\startqone}{C_{\startqonename}}' + "\n"
measure_codes += r'\newcommand{\startqthreename}{\text{A-start-Q3}}' + "\n"
measure_codes += r'\newcommand{\startqthree}{C_{\startqthreename}}' + "\n"
measure_codes += r'\newcommand{\startiqrname}{\text{A-start-IQR}}' + "\n"
measure_codes += r'\newcommand{\startiqr}{C_{\startiqrname}}' + "\n"
measure_codes += r'\newcommand{\startskewname}{\text{A-start-skew}}' + "\n"
measure_codes += r'\newcommand{\startskew}{C_{\startskewname}}' + "\n"
measure_codes += r'\newcommand{\startkurtname}{\text{A-start-kurt}}' + "\n"
measure_codes += r'\newcommand{\startkurt}{C_{\startkurtname}}' + "\n"
measure_codes += r'\newcommand{\lastactivitiesname}{\text{A-end-\#}}' + "\n"
measure_codes += r'\newcommand{\lastactivities}{C_{\lastactivitiesname}}' + "\n"
measure_codes += r'\newcommand{\lastactivitiesrelname}{\text{A-end-rel}}' + "\n"
measure_codes += r'\newcommand{\lastactivitiesrel}{C_{\lastactivitiesrelname}}' + "\n"
measure_codes += r'\newcommand{\lastminname}{\text{A-end-min}}' + "\n"
measure_codes += r'\newcommand{\lastmin}{C_{\lastminname}}' + "\n"
measure_codes += r'\newcommand{\lastmaxname}{\text{A-end-max}}' + "\n"
measure_codes += r'\newcommand{\lastmax}{C_{\lastmaxname}}' + "\n"
measure_codes += r'\newcommand{\lastmeanname}{\text{A-end-mean}}' + "\n"
measure_codes += r'\newcommand{\lastmean}{C_{\lastmeanname}}' + "\n"
measure_codes += r'\newcommand{\lastmedianname}{\text{A-end-med}}' + "\n"
measure_codes += r'\newcommand{\lastmedian}{C_{\lastmedianname}}' + "\n"
measure_codes += r'\newcommand{\lastdevname}{\text{A-end-dev}}' + "\n"
measure_codes += r'\newcommand{\lastdev}{C_{\lastdevname}}' + "\n"
measure_codes += r'\newcommand{\lastvarname}{\text{A-end-var}}' + "\n"
measure_codes += r'\newcommand{\lastvar}{C_{\lastvarname}}' + "\n"
measure_codes += r'\newcommand{\lastqonename}{\text{A-end-Q1}}' + "\n"
measure_codes += r'\newcommand{\lastqone}{C_{\lastqonename}}' + "\n"
measure_codes += r'\newcommand{\lastqthreename}{\text{A-end-Q3}}' + "\n"
measure_codes += r'\newcommand{\lastqthree}{C_{\lastqthreename}}' + "\n"
measure_codes += r'\newcommand{\lastiqrname}{\text{A-end-IQR}}' + "\n"
measure_codes += r'\newcommand{\lastiqr}{C_{\lastiqrname}}' + "\n"
measure_codes += r'\newcommand{\lastskewname}{\text{A-end-skew}}' + "\n"
measure_codes += r'\newcommand{\lastskew}{C_{\lastskewname}}' + "\n"
measure_codes += r'\newcommand{\lastkurtname}{\text{A-end-kurt}}' + "\n"
measure_codes += r'\newcommand{\lastkurt}{C_{\lastkurtname}}' + "\n"
measure_codes += r'\newcommand{\tlminname}{\text{TL-min}}' + "\n"
measure_codes += r'\newcommand{\tlmin}{C_{\tlminname}}' + "\n"
measure_codes += r'\newcommand{\tlavgname}{\text{TL-mean}}' + "\n"
measure_codes += r'\newcommand{\tlavg}{C_{\tlavgname}}' + "\n"
measure_codes += r'\newcommand{\tlmaxname}{\text{TL-max}}' + "\n"
measure_codes += r'\newcommand{\tlmax}{C_{\tlmaxname}}' + "\n"
measure_codes += r'\newcommand{\tlmedname}{\text{TL-med}}' + "\n"
measure_codes += r'\newcommand{\tlmed}{C_{\tlmedname}}' + "\n"
measure_codes += r'\newcommand{\tlmodename}{\text{TL-mode}}' + "\n"
measure_codes += r'\newcommand{\tlmode}{C_{\tlmodename}}' + "\n"
measure_codes += r'\newcommand{\tldevname}{\text{TL-dev}}' + "\n"
measure_codes += r'\newcommand{\tldev}{C_{\tldevname}}' + "\n"
measure_codes += r'\newcommand{\tlvarname}{\text{TL-var}}' + "\n"
measure_codes += r'\newcommand{\tlvar}{C_{\tlvarname}}' + "\n"
measure_codes += r'\newcommand{\tlqonename}{\text{TL-Q1}}' + "\n"
measure_codes += r'\newcommand{\tlqone}{C_{\tlqonename}}' + "\n"
measure_codes += r'\newcommand{\tlqthreename}{\text{TL-Q3}}' + "\n"
measure_codes += r'\newcommand{\tlqthree}{C_{\tlqthreename}}' + "\n"
measure_codes += r'\newcommand{\tliqrname}{\text{TL-IQR}}' + "\n"
measure_codes += r'\newcommand{\tliqr}{C_{\tliqrname}}' + "\n"
measure_codes += r'\newcommand{\tlgmeanname}{\text{TL-g-mean}}' + "\n"
measure_codes += r'\newcommand{\tlgmean}{C_{\tlgmeanname}}' + "\n"
measure_codes += r'\newcommand{\tlgdevname}{\text{TL-g-dev}}' + "\n"
measure_codes += r'\newcommand{\tlgdev}{C_{\tlgdevname}}' + "\n"
measure_codes += r'\newcommand{\tlhmeanname}{\text{TL-h-mean}}' + "\n"
measure_codes += r'\newcommand{\tlhmean}{C_{\tlhmeanname}}' + "\n"
measure_codes += r'\newcommand{\tlskewnessname}{\text{TL-skew}}' + "\n"
measure_codes += r'\newcommand{\tlskewness}{C_{\tlskewnessname}}' + "\n"
measure_codes += r'\newcommand{\tlkurtosisname}{\text{TL-kurt}}' + "\n"
measure_codes += r'\newcommand{\tlkurtosis}{C_{\tlkurtosisname}}' + "\n"
measure_codes += r'\newcommand{\tlcvariationname}{\text{TL-cvar}}' + "\n"
measure_codes += r'\newcommand{\tlcvariation}{C_{\tlcvariationname}}' + "\n"
measure_codes += r'\newcommand{\tlentropyname}{\text{TL-ent}}' + "\n"
measure_codes += r'\newcommand{\tlentropy}{C_{\tlentropyname}}' + "\n"
measure_codes += r'\newcommand{\tlhistonename}{\text{TL-hist1}}' + "\n"
measure_codes += r'\newcommand{\tlhistone}{C_{\tlhistonename}}' + "\n"
measure_codes += r'\newcommand{\tlhisttwoname}{\text{TL-hist2}}' + "\n"
measure_codes += r'\newcommand{\tlhisttwo}{C_{\tlhisttwoname}}' + "\n"
measure_codes += r'\newcommand{\tlhistthreename}{\text{TL-hist3}}' + "\n"
measure_codes += r'\newcommand{\tlhistthree}{C_{\tlhistthreename}}' + "\n"
measure_codes += r'\newcommand{\tlhistfourname}{\text{TL-hist4}}' + "\n"
measure_codes += r'\newcommand{\tlhistfour}{C_{\tlhistfourname}}' + "\n"
measure_codes += r'\newcommand{\tlhistfivename}{\text{TL-hist5}}' + "\n"
measure_codes += r'\newcommand{\tlhistfive}{C_{\tlhistfivename}}' + "\n"
measure_codes += r'\newcommand{\tlhistsixname}{\text{TL-hist6}}' + "\n"
measure_codes += r'\newcommand{\tlhistsix}{C_{\tlhistsixname}}' + "\n"
measure_codes += r'\newcommand{\tlhistsevenname}{\text{TL-hist7}}' + "\n"
measure_codes += r'\newcommand{\tlhistseven}{C_{\tlhistsevenname}}' + "\n"
measure_codes += r'\newcommand{\tlhisteightname}{\text{TL-hist8}}' + "\n"
measure_codes += r'\newcommand{\tlhisteight}{C_{\tlhisteightname}}' + "\n"
measure_codes += r'\newcommand{\tlhistninename}{\text{TL-hist9}}' + "\n"
measure_codes += r'\newcommand{\tlhistnine}{C_{\tlhistninename}}' + "\n"
measure_codes += r'\newcommand{\tlhisttenname}{\text{TL-hist10}}' + "\n"
measure_codes += r'\newcommand{\tlhistten}{C_{\tlhisttenname}}' + "\n"
measure_codes += r'\newcommand{\tlskewhistname}{\text{TL-hist-skew}}' + "\n"
measure_codes += r'\newcommand{\tlskewhist}{C_{\tlskewhistname}}' + "\n"
measure_codes += r'\newcommand{\tlkurthistname}{\text{TL-hist-kurt}}' + "\n"
measure_codes += r'\newcommand{\tlkurthist}{C_{\tlkurthistname}}' + "\n"
measure_codes += r'\newcommand{\freqmaxrname}{\text{FREQ-T-max-r}}' + "\n"
measure_codes += r'\newcommand{\freqmaxr}{C_{\freqmaxrname}}' + "\n"
measure_codes += r'\newcommand{\freqmaxonename}{\text{FREQ-T-max-1\%}}' + "\n"
measure_codes += r'\newcommand{\freqmaxone}{C_{\freqmaxonename}}' + "\n"
measure_codes += r'\newcommand{\freqmaxfivename}{\text{FREQ-T-max-5\%}}' + "\n"
measure_codes += r'\newcommand{\freqmaxfive}{C_{\freqmaxfivename}}' + "\n"
measure_codes += r'\newcommand{\freqmaxtenname}{\text{FREQ-T-max-10\%}}' + "\n"
measure_codes += r'\newcommand{\freqmaxten}{C_{\freqmaxtenname}}' + "\n"
measure_codes += r'\newcommand{\freqmaxtwentyname}{\text{FREQ-T-max-20\%}}' + "\n"
measure_codes += r'\newcommand{\freqmaxtwenty}{C_{\freqmaxtwentyname}}' + "\n"
measure_codes += r'\newcommand{\freqmaxfiftyname}{\text{FREQ-T-max-50\%}}' + "\n"
measure_codes += r'\newcommand{\freqmaxfifty}{C_{\freqmaxfiftyname}}' + "\n"
measure_codes += r'\newcommand{\freqmaxseventyfivename}{\text{FREQ-T-max-75\%}}' + "\n"
measure_codes += r'\newcommand{\freqmaxseventyfive}{C_{\freqmaxseventyfivename}}' + "\n"
measure_codes += r'\newcommand{\freqmeanname}{\text{FREQ-T-mean}}' + "\n"
measure_codes += r'\newcommand{\freqmean}{C_{\freqmeanname}}' + "\n"
measure_codes += r'\newcommand{\freqdevname}{\text{FREQ-T-dev}}' + "\n"
measure_codes += r'\newcommand{\freqdev}{C_{\freqdevname}}' + "\n"
measure_codes += r'\newcommand{\freqskewname}{\text{FREQ-T-skew}}' + "\n"
measure_codes += r'\newcommand{\freqskew}{C_{\freqskewname}}' + "\n"
measure_codes += r'\newcommand{\freqkurtname}{\text{FREQ-T-kurt}}' + "\n"
measure_codes += r'\newcommand{\freqkurt}{C_{\freqkurtname}}' + "\n"
measure_codes += r'\newcommand{\actfreqminname}{\text{FREQ-A-min}}' + "\n"
measure_codes += r'\newcommand{\actfreqmin}{C_{\actfreqminname}}' + "\n"
measure_codes += r'\newcommand{\actfreqmaxname}{\text{FREQ-A-max}}' + "\n"
measure_codes += r'\newcommand{\actfreqmax}{C_{\actfreqmaxname}}' + "\n"
measure_codes += r'\newcommand{\actfreqmeanname}{\text{FREQ-A-mean}}' + "\n"
measure_codes += r'\newcommand{\actfreqmean}{C_{\actfreqmeanname}}' + "\n"
measure_codes += r'\newcommand{\actfreqmedianname}{\text{FREQ-A-med}}' + "\n"
measure_codes += r'\newcommand{\actfreqmedian}{C_{\actfreqmedianname}}' + "\n"
measure_codes += r'\newcommand{\actfreqdevname}{\text{FREQ-A-dev}}' + "\n"
measure_codes += r'\newcommand{\actfreqdev}{C_{\actfreqdevname}}' + "\n"
measure_codes += r'\newcommand{\actfreqvarname}{\text{FREQ-A-var}}' + "\n"
measure_codes += r'\newcommand{\actfreqvar}{C_{\actfreqvarname}}' + "\n"
measure_codes += r'\newcommand{\actfreqqonename}{\text{FREQ-A-Q1}}' + "\n"
measure_codes += r'\newcommand{\actfreqqone}{C_{\actfreqqonename}}' + "\n"
measure_codes += r'\newcommand{\actfreqqthreename}{\text{FREQ-A-Q3}}' + "\n"
measure_codes += r'\newcommand{\actfreqqthree}{C_{\actfreqqthreename}}' + "\n"
measure_codes += r'\newcommand{\actfreqiqrname}{\text{FREQ-A-IRQ}}' + "\n"
measure_codes += r'\newcommand{\actfreqiqr}{C_{\actfreqiqrname}}' + "\n"
measure_codes += r'\newcommand{\actfreqskewname}{\text{FREQ-A-skew}}' + "\n"
measure_codes += r'\newcommand{\actfreqskew}{C_{\actfreqskewname}}' + "\n"
measure_codes += r'\newcommand{\actfreqkurtname}{\text{FREQ-A-kurt}}' + "\n"
measure_codes += r'\newcommand{\actfreqkurt}{C_{\actfreqkurtname}}' + "\n"
measure_codes += r'\newcommand{\numberuniquetracesname}{\text{DT-\#}}' + "\n"
measure_codes += r'\newcommand{\numberuniquetraces}{C_{\numberuniquetracesname}}' + "\n"
measure_codes += r'\newcommand{\percentageuniquetracesname}{\text{DT-\%}}' + "\n"
measure_codes += r'\newcommand{\percentageuniquetraces}{C_{\percentageuniquetracesname}}' + "\n"
measure_codes += r'\newcommand{\dtcovname}{\text{DT-cov}}' + "\n"
measure_codes += r'\newcommand{\dtcov}{C_{\dtcovname}}' + "\n"
measure_codes += r'\newcommand{\dtrelcovname}{\text{DT-cov-\%}}' + "\n"
measure_codes += r'\newcommand{\dtrelcov}{C_{\dtrelcovname}}' + "\n"
measure_codes += r'\newcommand{\dthetname}{\text{DT-het}}' + "\n"
measure_codes += r'\newcommand{\dthet}{C_{\dthetname}}' + "\n"
measure_codes += r'\newcommand{\dtsimname}{\text{DT-sim}}' + "\n"
measure_codes += r'\newcommand{\dtsim}{C_{\dtsimname}}' + "\n"
measure_codes += r'\newcommand{\daminname}{\text{DA-min}}' + "\n"
measure_codes += r'\newcommand{\damin}{C_{\daminname}}' + "\n"
measure_codes += r'\newcommand{\daavgname}{\text{DA-avg}}' + "\n"
measure_codes += r'\newcommand{\daavg}{C_{\daavgname}}' + "\n"
measure_codes += r'\newcommand{\damaxname}{\text{DA-max}}' + "\n"
measure_codes += r'\newcommand{\damax}{C_{\damaxname}}' + "\n"
measure_codes += r'\newcommand{\dadevname}{\text{DA-dev}}' + "\n"
measure_codes += r'\newcommand{\dadev}{C_{\dadevname}}' + "\n"
measure_codes += r'\newcommand{\dadensname}{\text{DA-dens}}' + "\n"
measure_codes += r'\newcommand{\dadens}{C_{\dadensname}}' + "\n"
measure_codes += r'\newcommand{\daoverlapname}{\text{DA-ovrlp}}' + "\n"
measure_codes += r'\newcommand{\daoverlap}{C_{\daoverlapname}}' + "\n"
measure_codes += r'\newcommand{\complexityfactorname}{\text{comp-fact}}' + "\n"
measure_codes += r'\newcommand{\complexityfactor}{C_{\complexityfactorname}}' + "\n"
measure_codes += r'\newcommand{\simpletracedivname}{\text{s-T-div}}' + "\n"
measure_codes += r'\newcommand{\simpletracediv}{C_{\simpletracedivname}}' + "\n"
measure_codes += r'\newcommand{\advtracedivname}{\text{a-T-div}}' + "\n"
measure_codes += r'\newcommand{\advtracediv}{C_{\advtracedivname}}' + "\n"
measure_codes += r'\newcommand{\loopnumname}{\text{loop-\#}}' + "\n"
measure_codes += r'\newcommand{\loopnum}{C_{\loopnumname}}' + "\n"
measure_codes += r'\newcommand{\looprelnumname}{\text{loop-rel-\#}}' + "\n"
measure_codes += r'\newcommand{\looprelnum}{C_{\looprelnumname}}' + "\n"
measure_codes += r'\newcommand{\loopavgname}{\text{loop-avg-\#}}' + "\n"
measure_codes += r'\newcommand{\loopavg}{C_{\loopavgname}}' + "\n"
measure_codes += r'\newcommand{\loopmaxname}{\text{loop-max-\#}}' + "\n"
measure_codes += r'\newcommand{\loopmax}{C_{\loopmaxname}}' + "\n"
measure_codes += r'\newcommand{\loopavgsizename}{\text{loop-avg-size}}' + "\n"
measure_codes += r'\newcommand{\loopavgsize}{C_{\loopavgsizename}}' + "\n"
measure_codes += r'\newcommand{\loopmaxsizename}{\text{loop-max-size}}' + "\n"
measure_codes += r'\newcommand{\loopmaxsize}{C_{\loopmaxsizename}}' + "\n"
measure_codes += r'\newcommand{\repnumname}{\text{rep-\#}}' + "\n"
measure_codes += r'\newcommand{\repnum}{C_{\repnumname}}' + "\n"
measure_codes += r'\newcommand{\reprelnumname}{\text{rep-rel-\#}}' + "\n"
measure_codes += r'\newcommand{\reprelnum}{C_{\repnumname}}' + "\n"
measure_codes += r'\newcommand{\dfgnodesname}{\text{DFG-V}}' + "\n"
measure_codes += r'\newcommand{\dfgnodes}{C_{\dfgnodesname}}' + "\n"
measure_codes += r'\newcommand{\dfgedgesname}{\text{DFG-E}}' + "\n"
measure_codes += r'\newcommand{\dfgedges}{C_{\dfgedgesname}}' + "\n"
measure_codes += r'\newcommand{\dfgcncname}{\text{DFG-cnc}}' + "\n"
measure_codes += r'\newcommand{\dfgcnc}{C_{\dfgcncname}}' + "\n"
measure_codes += r'\newcommand{\dfgavgdegname}{\text{DFG-adeg}}' + "\n"
measure_codes += r'\newcommand{\dfgavgdeg}{C_{\dfgavgdegname}}' + "\n"
measure_codes += r'\newcommand{\dfgmaxdegname}{\text{DFG-mdeg}}' + "\n"
measure_codes += r'\newcommand{\dfgmaxdeg}{C_{\dfgmaxdegname}}' + "\n"
measure_codes += r'\newcommand{\dfgdensname}{\text{DFG-dens}}' + "\n"
measure_codes += r'\newcommand{\dfgdens}{C_{\dfgdensname}}' + "\n"
measure_codes += r'\newcommand{\dfgstructname}{\text{DFG-struct}}' + "\n"
measure_codes += r'\newcommand{\dfgstruct}{C_{\dfgstructname}}' + "\n"
measure_codes += r'\newcommand{\dfgcycnumbername}{\text{DFG-CN}}' + "\n"
measure_codes += r'\newcommand{\dfgcycnumber}{C_{\dfgcycnumbername}}' + "\n"
measure_codes += r'\newcommand{\dfgdiamname}{\text{DFG-diam}}' + "\n"
measure_codes += r'\newcommand{\dfgdiam}{C_{\dfgdiamname}}' + "\n"
measure_codes += r'\newcommand{\dfgsepnumname}{\text{DFG-sep-\#}}' + "\n"
measure_codes += r'\newcommand{\dfgsepnum}{C_{\dfgsepnumname}}' + "\n"
measure_codes += r'\newcommand{\dfgseprationame}{\text{DFG-sep-r}}' + "\n"
measure_codes += r'\newcommand{\dfgsepratio}{C_{\dfgseprationame}}' + "\n"
measure_codes += r'\newcommand{\dfgseqrationame}{\text{DFG-seq-r}}' + "\n"
measure_codes += r'\newcommand{\dfgseqratio}{C_{\dfgseqrationame}}' + "\n"
measure_codes += r'\newcommand{\dfgcycname}{\text{DFG-cyc}}' + "\n"
measure_codes += r'\newcommand{\dfgcyc}{C_{\dfgcycname}}' + "\n"
measure_codes += r'\newcommand{\dfgpathcomplexityname}{\text{DFG-P-comp}}' + "\n"
measure_codes += r'\newcommand{\dfgpathcomplexity}{C_{\dfgpathcomplexityname}}' + "\n"
measure_codes += r'\newcommand{\numberofneighborhoodsname}{\text{succ}}' + "\n"
measure_codes += r'\newcommand{\numberofneighborhoods}{C_{\numberofneighborhoodsname}}' + "\n"
measure_codes += r'\newcommand{\numberoftiesname}{\text{ties}}' + "\n"
measure_codes += r'\newcommand{\numberofties}{C_{\numberoftiesname}}' + "\n"
measure_codes += r'\newcommand{\lempelzivname}{\text{LZ}}' + "\n"
measure_codes += r'\newcommand{\lempelziv}{C_{\lempelzivname}}' + "\n"
measure_codes += r'\newcommand{\structurename}{\text{struct}}' + "\n"
measure_codes += r'\newcommand{\structure}{C_{\structurename}}' + "\n"
measure_codes += r'\newcommand{\affinityname}{\text{affinity}}' + "\n"
measure_codes += r'\newcommand{\affinity}{C_{\affinityname}}' + "\n"
measure_codes += r'\newcommand{\deviationfromrandomname}{\text{dev-R}}' + "\n"
measure_codes += r'\newcommand{\deviationfromrandom}{C_{\deviationfromrandomname}}' + "\n"
measure_codes += r'\newcommand{\avgdistname}{\text{avg-dist}}' + "\n"
measure_codes += r'\newcommand{\avgdist}{C_{\avgdistname}}' + "\n"
measure_codes += r'\newcommand{\enttracename}{\text{ENT-trace}}' + "\n"
measure_codes += r'\newcommand{\enttrace}{C_{\enttracename}}' + "\n"
measure_codes += r'\newcommand{\entprefixname}{\text{ENT-pref}}' + "\n"
measure_codes += r'\newcommand{\entprefix}{C_{\entprefixname}}' + "\n"
measure_codes += r'\newcommand{\entprefixflatname}{\text{ENT-pref-F}}' + "\n"
measure_codes += r'\newcommand{\entprefixflat}{C_{\entprefixflatname}}' + "\n"
measure_codes += r'\newcommand{\entgblockname}{\text{ENT-g-block}}' + "\n"
measure_codes += r'\newcommand{\entgblock}{C_{\entgblockname}}' + "\n"
measure_codes += r'\newcommand{\entgblockflatname}{\text{ENT-g-block-F}}' + "\n"
measure_codes += r'\newcommand{\entgblockflat}{C_{\entgblockflatname}}' + "\n"
measure_codes += r'\newcommand{\entlempelzivname}{\text{ENT-LZ}}' + "\n"
measure_codes += r'\newcommand{\entlempelziv}{C_{\entlempelzivname}}' + "\n"
measure_codes += r'\newcommand{\entlempelzivflatname}{\text{ENT-LZ-F}}' + "\n"
measure_codes += r'\newcommand{\entlempelzivflat}{C_{\entlempelzivflatname}}' + "\n"
measure_codes += r'\newcommand{\entkblockdonename}{\text{ENT-k-block-d1}}' + "\n"
measure_codes += r'\newcommand{\entkblockdone}{C_{\entkblockdonename}}' + "\n"
measure_codes += r'\newcommand{\entkblockdthreename}{\text{ENT-k-block-d3}}' + "\n"
measure_codes += r'\newcommand{\entkblockdthree}{C_{\entkblockdthreename}}' + "\n"
measure_codes += r'\newcommand{\entkblockdfivename}{\text{ENT-k-block-d5}}' + "\n"
measure_codes += r'\newcommand{\entkblockdfive}{C_{\entkblockdfivename}}' + "\n"
measure_codes += r'\newcommand{\entkblockronename}{\text{ENT-k-block-r1}}' + "\n"
measure_codes += r'\newcommand{\entkblockrone}{C_{\entkblockronename}}' + "\n"
measure_codes += r'\newcommand{\entkblockrthreename}{\text{ENT-k-block-r3}}' + "\n"
measure_codes += r'\newcommand{\entkblockrthree}{C_{\entkblockrthreename}}' + "\n"
measure_codes += r'\newcommand{\entkblockrfivename}{\text{ENT-k-block-r5}}' + "\n"
measure_codes += r'\newcommand{\entkblockrfive}{C_{\entkblockrfivename}}' + "\n"
measure_codes += r'\newcommand{\entknnthreename}{\text{ENT-knn-3}}' + "\n"
measure_codes += r'\newcommand{\entknnthree}{C_{\entknnthreename}}' + "\n"
measure_codes += r'\newcommand{\entknnfivename}{\text{ENT-knn-5}}' + "\n"
measure_codes += r'\newcommand{\entknnfive}{C_{\entknnfivename}}' + "\n"
measure_codes += r'\newcommand{\entknnsevenname}{\text{ENT-knn-7}}' + "\n"
measure_codes += r'\newcommand{\entknnseven}{C_{\entknnsevenname}}' + "\n"
measure_codes += r'\newcommand{\epavariantname}{\text{epa-var}}' + "\n"
measure_codes += r'\newcommand{\epavariant}{C_{\epavariantname}}' + "\n"
measure_codes += r'\newcommand{\epanormvariantname}{\text{epa-n-var}}' + "\n"
measure_codes += r'\newcommand{\epanormvariant}{C_{\epanormsequencename}}' + "\n"
measure_codes += r'\newcommand{\epasequencename}{\text{epa-seq}}' + "\n"
measure_codes += r'\newcommand{\epasequence}{C_{\epasequencename}}' + "\n"
measure_codes += r'\newcommand{\epanormsequencename}{\text{epa-n-seq}}' + "\n"
measure_codes += r'\newcommand{\epanormsequence}{C_{\epanormsequencename}}' + "\n"
measure_codes += r'\newcommand{\epasequencelname}{\text{epa-seq-L}}' + "\n"
measure_codes += r'\newcommand{\epasequencel}{C_{\epasequencelname}}' + "\n"
measure_codes += r'\newcommand{\epanormsequencelname}{\text{epa-n-seq-L}}' + "\n"
measure_codes += r'\newcommand{\epanormsequencel}{C_{\epanormsequencelname}}' + "\n"
measure_codes += r'\newcommand{\epasequenceename}{\text{epa-seq-E}}' + "\n"
measure_codes += r'\newcommand{\epasequencee}{C_{\epasequenceename}}' + "\n"
measure_codes += r'\newcommand{\epanormsequenceename}{\text{epa-n-seq-E}}' + "\n"
measure_codes += r'\newcommand{\epanormsequencee}{C_{\epanormsequenceename}}' + "\n"

class LatexExporter():
    def __init__(self, complexityFactorAnalysis, log_measures, sample_size):
        self.CFA = complexityFactorAnalysis
        self.measures = log_measures
        self.sample_size = sample_size

    def get_latex_filename(self, topic: str):
        return Constants.LATEX_REPORT_PATH + topic + "-" + str(self.CFA.number_of_factors) + "-factors-" + str(self.CFA.rotation) + ".tex"

    def export_factor_analysis_info(self, filename: str):
        f = open(filename, "w")
        f.write("\\documentclass[a4paper]{article}\n\n")
        f.write("\\usepackage[margin=1in]{geometry}\n")
        f.write(r'\usepackage{tikz}' + "\n")
        f.write(r'\usepackage{pgfplots}' + "\n")
        f.write(r'\usepackage{paralist}' + "\n")
        f.write(r'\usepackage{amsmath}' + "\n")
        f.write(measure_codes + "\n")
        f.write(r'\begin{document}' + "\n\n")
        f.write("\\section*{Information About the Performed Analysis}\n")
        f.write("\nYou chose to analyze the following complexity measures:\n")
        f.write("\\begin{compactenum}\n")
        for measure in self.measures:
            f.write("\\item $" + latex_command[str(measure)] + "$ (" + str(measure).replace("_", " ") + ")\n")
        f.write("\\end{compactenum}\n\n")
        f.write("\\bigskip\n")
        f.write("\\noindent\nOut of these measures, the following were excluded because they returned non-numeric values:\n")
        f.write("\\begin{compactenum}\n")
        for measure in self.CFA.non_numeric_variables:
            f.write("\\item $" + latex_command[str(measure)] + "$ (" + str(measure).replace("_", " ") + ")\n")
        f.write("\\end{compactenum}\n\n")
        f.write("\\bigskip\n")
        f.write("\\noindent\nFurthermore, the following measures were excluded because their variance is $0$ in the analyzed data:\n")
        f.write("\\begin{compactenum}\n")
        for measure in self.CFA.zero_variance_variables:
            f.write("\\item $" + latex_command[str(measure)] + "$ (" + str(measure).replace("_", " ") + ")\n")
        f.write("\\end{compactenum}\n\n")
        f.write("\\bigskip\n")
        f.write("\\noindent\nAdditionally, the following measures were excluded because they are correlated with other measures:\n")
        f.write("\\begin{compactenum}\n")
        for measure in self.CFA.correlated_variables:
            f.write("\\item $" + latex_command[str(measure)] + "$ (" + str(measure).replace("_", " ") + ")\n")
        f.write("\\end{compactenum}\n\n")
        f.write("\\bigskip\n")
        n_remaining_measures = len(self.measures) - len(self.CFA.non_numeric_variables) - len(self.CFA.zero_variance_variables) - len(self.CFA.correlated_variables)
        f.write("\\noindent\nThis leaves us with a total of $" + str(n_remaining_measures) + "$ log measures to analyze.\n\n")

        f.write("\\subsection*{Validity of the Factor Analysis}\n")
        f.write("Your sample size in this analysis was $" + str(self.sample_size) + "$.\n")
        f.write("It is recommended to have a sample size of at least $5 \\cdot " + str(len(self.measures)) + " = " + str(5*len(self.measures)) + "$.\n\n")
        f.write("\\noindent \nBartlett's test of sphericity returned a $\\chi^2$ value of $" + str(self.CFA.bartlett_chi_squared) + "$ and a $p$-value of $" + str(self.CFA.bartlett_p_value) + "$.\n")
        if self.CFA.bartlett_p_value < Constants.bartlett_p_value_threshold:
            f.write("This means, the variables are probably correlated and we can perform a factor analysis.\n\n")
        else:
            f.write("This means, the variables are probably not correlated and performing a factor analysis is \\textbf{not} advised.\n\n")
        f.write("\\noindent\nThe measure of sampling adequacy (MSA) returned the following results:\n")
        f.write("\\begin{compactitem}\n")
        index = 0
        for measure in list(self.CFA.complexity_data):
            f.write("\\item $" + latex_command[str(measure)] + "$: $" + str(round(self.CFA.msa_per_variable[index], Constants.number_of_decimals)) + "$\n")
            index += 1
        f.write("\\item overall MSA: $" + str(self.CFA.overall_msa) + "$\n")
        f.write("\\end{compactitem}\n\n")
        if len(self.CFA.msa_insufficient_variables.keys()) > 0:
            f.write("\\bigskip\n")
            f.write("\\noindent\nDuring the analysis, the MSA values of the following complexity measures were too low:\n")
            f.write("\\begin{compactitem}\n")
            for measure in self.CFA.msa_insufficient_variables.keys():
                f.write("\\item $" + latex_command[str(measure)] + "$: $" + str(round(self.CFA.msa_insufficient_variables[measure], Constants.number_of_decimals)) + "$\n")
            f.write("\\end{compactitem}\n")
            f.write("These complexity measures were left out of the analysis to produce dependable results.\n\n")

        f.write("\\subsection*{Chosen Number of Factors}\n")
        f.write("\\noindent\nThe Scree test resulted in the following Eigenvalue plot:\n")
        f.write("\\begin{center}\n")
        f.write("\\begin{tikzpicture}\n")
        f.write("\\begin{axis}[width=15cm,height=8cm]\n")
        f.write("\\addplot [draw=cyan!50!blue, mark=*] coordinates {")
        if len(self.CFA.pca_explained_variance_ratio) == 0:
            self.CFA.calculate_scree_plot()
        for index in range(len(self.CFA.pca_explained_variance_ratio)):
            f.write(" (" + str(index + 1) + "," + str(round(self.CFA.pca_explained_variance_ratio[index], Constants.number_of_decimals)) + ")")
        f.write("};\n")
        f.write("\\end{axis}\n")
        f.write("\\end{tikzpicture}\n")
        f.write("\\end{center}\n")
        f.write("\\noindent\nYou choose to set the number of expected factors to $" + str(self.CFA.number_of_factors) + "$.\n\n")
        f.write(r'\end{document}')
        f.close()

    def export_descriptive_statistics(self, filename: str):
        f = open(filename, "w")
        f.write(r'\documentclass{standalone}' + "\n")
        f.write(r'\usepackage{booktabs}' + "\n")
        f.write(r'\usepackage{amsmath}' + "\n")
        f.write(measure_codes + "\n")
        f.write(r'\begin{document}' + "\n\n")
        rows = len(self.CFA.descriptive_statistics.index)
        columns = len(self.CFA.descriptive_statistics.columns)
        f.write("\\begin{tabular}{l")
        for i in range(columns):
            f.write("c")
        f.write("} \\toprule \n")
        for column in self.CFA.descriptive_statistics.columns:
            f.write(" & \\textbf{" + str(column) + "}")
        f.write(" \\\\ \\midrule \n")
        for i in range(rows):
            f.write("$" + latex_command[str(list(self.CFA.descriptive_statistics.index)[i])] + "$")
            for j in range(columns):
                value = round(self.CFA.descriptive_statistics.iat[i, j], Constants.number_of_decimals)
                f.write(" & $" + str(value) + "$")
            f.write(" \\\\ \n")
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n\n")
        f.write("\n")
        f.write(r'\end{document}')
        f.close()

    def export_communality_info(self, filename: str):
        f = open(filename, "w")
        f.write(r'\documentclass{standalone}' + "\n")
        f.write(r'\usepackage{tikz}' + "\n")
        f.write(r'\usepackage{pgfplots}' + "\n")
        f.write(r'\usepackage{amsmath}' + "\n")
        f.write(measure_codes + "\n")
        f.write(r'\begin{document}' + "\n\n")
        f.write("\\begin{tikzpicture}\n")
        x_coords = ""
        for measure in list(self.CFA.complexity_data):
            x_coords += "$" + latex_command[str(measure)] + "$,"
        x_coords = x_coords[0:-1]
        width = 3 * len(list(self.CFA.complexity_data)) / 4
        f.write("\\begin{axis}[ybar,enlarge x limits=0.01,symbolic x coords={" + x_coords + "},xtick=data,xticklabel style={rotate=45, anchor=east},nodes near coords={\\pgfmathprintnumber{\\pgfplotspointmeta}},width=" + str(width) + "cm,height=8cm]\n")
        f.write("\\addplot [draw=cyan!50!blue, fill=cyan!50!blue] plot coordinates {")
        communalities = pandas.Series(self.CFA.communalities, index=list(self.CFA.complexity_data))
        index = 0
        for c in communalities:
            f.write(" ($" + str(latex_command[list(self.CFA.complexity_data)[index]]) + "$," + str(round(c, Constants.number_of_decimals)) + ")")
            index += 1
        f.write(" };\n")
        f.write("\\path (axis cs:{[normalized]1}," + str(Constants.communality_threshold) + ") coordinate (threshold);")
        f.write("\\end{axis}\n")
        f.write("\\draw[red, dashed, thick] (current axis.west |- threshold) -- (current axis.east |- threshold);")
        f.write("\\end{tikzpicture}\n\n")
        f.write(r'\end{document}')
        f.close()

    def export_factor_loadings_table(self, filename: str):
        f = open(filename, "w")
        f.write(r'\documentclass{standalone}' + "\n\n")
        f.write(r'\usepackage{booktabs}' + "\n")
        f.write(r'\usepackage{tikz}' + "\n")
        f.write(r'\usepackage{amsmath}' + "\n\n")
        f.write(measure_codes + "\n")
        f.write(r'\begin{document}' + "\n\n")
        rows = len(self.CFA.factor_loadings)
        columns = len(self.CFA.factor_loadings[0])
        f.write("\\begin{tabular}{l")
        for i in range(columns):
            f.write("c")
        f.write("} \\toprule \n")
        for i in range(columns):
            f.write(" & \\textbf{Factor " + str(i+1) + "}")
        f.write(" \\\\ \\midrule \n")
        for i in range(rows):
            if self.CFA.communalities[i] >= Constants.communality_threshold:
                f.write("$" + latex_command[str(list(self.CFA.complexity_data)[i])] + "$")
                for j in range(columns):
                    value = round(self.CFA.factor_loadings[i][j], Constants.number_of_decimals)
                    if abs(value) < Constants.ignore_threshold:
                        f.write(" & \\textcolor{lightgray}{$" + str(value) + "$}")
                    else:
                        f.write(" & $" + str(value) + "$")
                f.write(" \\\\ \n")
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n\n")
        f.write(r'\end{document}')
        f.close()

    def export(self):
        filename = self.get_latex_filename("analysis-info")
        print("Exporting info about the factor analysis to " + str(filename) + "...")
        self.export_factor_analysis_info(filename)
        filename = self.get_latex_filename("descriptive-stats")
        print("Exporting descriptive statistics of the measures to " + str(filename) + "...")
        self.export_descriptive_statistics(filename)
        filename = self.get_latex_filename("communalities")
        print("Exporting the variables' communalities to " + str(filename) + "...")
        self.export_communality_info(filename)
        filename = self.get_latex_filename("factor-loadings")
        print("Exporting table of factor loadings to " + str(filename) + "...")
        self.export_factor_loadings_table(filename)
