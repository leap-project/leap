# This file contains the code for the different algorithms in
# Leap and the different types of functions that are available.

# Algo Code
COUNT_ALGO = "count_fn"
COUNT_ALGO_RC = "count_fn_redcap"
COUNT_ALGO_RC_QUERY = "count_fn_redcap_query"
PRIVATE_SITE_COUNT_ALGO = "count_fn_site_dp" # Adds privacy at site layer
PRIVATE_CLOUD_COUNT_ALGO = "count_fn_cloud_dp" # Adds privacy at cloud layer
SUM_ALGO = "sum_fn"
VARIANCE_ALGO = "var_fn"
FEDERATED_LEARNING_ALGO = "fl_fn"
QUANTILE_ALGO = "quantile_fn"
LOG_REG = "log_reg_fn"

# Leap Types
UDF = 1
LAPLACE_UDF = 2
EXPONENTIAL_UDF = 3
PREDEFINED = 4
PRIVATE_PREDEFINED = 5
FEDERATED_LEARNING = 6