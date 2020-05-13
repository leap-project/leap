// This file contains the code for the different algorithms in
// Leap and the different types of functions that are available.

// Algo Code
export const COUNT_ALGO = "count_fn"
export const PRIVATE_SITE_COUNT_ALGO = "count_fn_site_dp" // Adds privacy at site layer
export const PRIVATE_CLOUD_COUNT_ALGO = "count_fn_cloud_dp" // Adds privacy at cloud layer
export const SUM_ALGO = "sum_fn"
export const VARIANCE_ALGO = "var_fn"
export const FEDERATED_LEARNING_ALGO = "fl_fn"
export const QUANTILE_ALGO = "quantile_fn"

// Leap Types
export const UDF = 1
export const LAPLACE_UDF = 2
export const EXPONENTIAL_UDF = 3
export const PREDEFINED = 4
export const PRIVATE_PREDEFINED = 5
export const FEDERATED_LEARNING = 6