# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Utility methods for validation and conversion."""
import json
import logging
import os
import re
from typing import Any, Dict, List, Optional, Union, cast

from azureml._common._error_response.error_hierarchy import ErrorHierarchy
from azureml._common.exceptions import AzureMLException
from azureml.automl.core.shared import constants
from azureml.automl.core.constants import LanguageUnicodeRanges
from azureml.automl.core.shared.constants import NumericalDtype, DatetimeDtype
from azureml.automl.core.shared.exceptions import ErrorTypes, ClientException, MemorylimitException, ServiceException
from azureml.exceptions import ServiceException as AzureMLServiceException

try:
    from azureml.automl.runtime.shared import utilities as runtime_utilities

    def check_input(df):
        """
        DEPRECATED. Use azureml.automl.runtime.shared.utilities.check_input.

        Check inputs for transformations.

        :param df: Input dataframe.
        :return:
        """
        return runtime_utilities.check_input(df)

    def _get_column_data_type_as_str(array):
        """
        DEPRECATED. Use azureml.automl.runtime.shared.utilities._get_column_data_type_as_str.

        Get the type of ndarray by looking into the ndarray contents.

        :param array: ndarray
        :raise ClientException if array is not ndarray or not valid
        :return: type of column as a string (integer, floating, string etc.)
        """
        return runtime_utilities._get_column_data_type_as_str(array)
except ImportError:
    pass

# For backward compatibility

SOURCE_WRAPPER_MODULE = 'automl.client.core.runtime.model_wrappers'
MAPPED_WRAPPER_MODULE = 'azureml.train.automl.model_wrappers'


logger = logging.getLogger(__name__)


def _check_if_column_data_type_is_numerical(data_type_as_string: str) -> bool:
    """
    Check if column data type is numerical.

    Arguments:
        data_type_as_string {string} -- string carrying the type from infer_dtype().

    Returns:
        bool -- 'True' if the dtype returned is 'integer', 'floating', 'mixed-integer' or 'mixed-integer-float'.
                     'False' otherwise.

    """
    if data_type_as_string in list(NumericalDtype.FULL_SET):
        return True

    return False


def _check_if_column_data_type_is_datetime(data_type_as_string: str) -> bool:
    """
    Check if column data type is datetime.

    Arguments:
        data_type_as_string {string} -- string carrying the type from infer_dtype().

    Returns:
        bool -- 'True' if the dtype returned is 'date', 'datetime' or 'datetime64'. 'False' otherwise.

    """
    return data_type_as_string in DatetimeDtype.FULL_SET


def _check_if_column_data_type_is_int(data_type_as_string: str) -> bool:
    """
    Check if column data type is integer.

    Arguments:
        data_type_as_string {string} -- string carrying the type from infer_dtype().

    Returns:
        boolean -- 'True' if the dtype returned is 'integer'. 'False' otherwise.

    """
    if data_type_as_string == NumericalDtype.Integer:
        return True

    return False


def _check_if_column_data_is_nonspaced_language(unicode_median_value: int) -> bool:
    """
    Check if the median of unicode value belongs to a nonspaced language.

    Arguments:
        unicode_median_value {int} -- median of unicode values of the entire column.

    Returns:
        boolean -- 'True' if the unicode median value is within the unicode ranges of
        languages that has no spaces and supported by bert multilingual.
                        'False' otherwise.

    """
    for range_ in LanguageUnicodeRanges.nonspaced_language_unicode_ranges:
        if range_[0] <= unicode_median_value <= range_[1]:
            return True

    return False


def get_value_int(intstring: str) -> Optional[Union[int, str]]:
    """
    Convert string value to int.

    Arguments:
        intstring {str} -- The input value to be converted.

    Returns:
        int -- The converted value.

    """
    if intstring is not None and intstring != '':
        return int(intstring)
    return intstring


def get_value_float(floatstring: str) -> Optional[Union[float, str]]:
    """
    Convert string value to float.

    Arguments:
        floatstring {str} -- The input value to be converted.

    Returns:
        float -- The converted value.

    """
    if floatstring is not None and floatstring != '':
        return float(floatstring)
    return floatstring


def get_value_from_dict(dictionary: Dict[str, Any], names: List[str], default_value: Any) -> Any:
    """
    Get the value of a configuration item that has a list of names.

    Arguments:
        dictionary {dict} -- Dictionary of settings with key value pair to look the data for.
        names {list of str} -- The list of names for the item looking foi.
        default_value {object} -- Default value to return if no matching key found

    Returns:
        object -- Returns the first value from the list of names.

    """
    for key in names:
        if key in dictionary:
            return dictionary[key]
    return default_value


def _get_max_min_comparator(objective):
    """Return a comparator either maximizing or minimizing two values. Will not handle nans."""
    if objective == constants.OptimizerObjectives.MAXIMIZE:
        def maximize(x, y):
            if x >= y:
                return x
            else:
                return y
        return maximize
    elif objective == constants.OptimizerObjectives.MINIMIZE:
        def minimize(x, y):
            if x <= y:
                return x
            else:
                return y
        return minimize
    else:
        raise ClientException(
            "Maximization or Minimization could not be determined "
            "based on current metric.", has_pii=False)


def subsampling_recommended(num_samples):
    """
    Return whether or not subsampling is recommended for the current scenario.

    Arguments:
        num_samples {int} -- number of samples.

    Returns:
        bool -- True if subsampling is recommended, else False.

    """
    return num_samples >= 50000


def _log_raw_data_stat(raw_feature_stats, prefix_message=None):
    if prefix_message is None:
        prefix_message = ""
    raw_feature_stats_dict = dict()
    for name, stats in raw_feature_stats.__dict__.items():
        try:
            stats_json_str = json.dumps(stats)
        except (ValueError, TypeError):
            stats_json_str = json.dumps(dict())
        raw_feature_stats_dict[name] = stats_json_str
    logger.info(
        "{}RawFeatureStats:{}".format(
            prefix_message, json.dumps(raw_feature_stats_dict)
        )
    )


def _get_ts_params_dict(automl_settings: Any) -> Optional[Dict[str, str]]:
    """
    Get time series parameter data.

    Arguments:
        automl_settings {AutoMLSettings} -- automl settings object

    Returns:
        dict -- a dictionary of time series data info

    """
    if automl_settings.is_timeseries:
        dict_time_series = {
            constants.TimeSeries.TIME_COLUMN_NAME: automl_settings.time_column_name,
            constants.TimeSeries.GRAIN_COLUMN_NAMES: automl_settings.grain_column_names,
            constants.TimeSeries.DROP_COLUMN_NAMES: automl_settings.drop_column_names,
            constants.TimeSeriesInternal.OVERWRITE_COLUMNS: automl_settings.overwrite_columns,
            constants.TimeSeriesInternal.DROP_NA: automl_settings.dropna,
            constants.TimeSeriesInternal.TRANSFORM_DICT: automl_settings.transform_dictionary,
            constants.TimeSeries.MAX_HORIZON: automl_settings.max_horizon,
            constants.TimeSeriesInternal.ORIGIN_TIME_COLUMN_NAME:
                constants.TimeSeriesInternal.ORIGIN_TIME_COLNAME_DEFAULT,
            constants.TimeSeries.COUNTRY_OR_REGION: automl_settings.country_or_region,
            constants.TimeSeriesInternal.CROSS_VALIDATIONS: automl_settings.n_cross_validations,
            constants.TimeSeries.SHORT_SERIES_HANDLING: automl_settings.short_series_handling,
            constants.TimeSeries.MAX_CORES_PER_ITERATION: automl_settings.max_cores_per_iteration,
            constants.TimeSeries.FEATURE_LAGS: automl_settings.feature_lags
        }
        # Set window size and lags only if user did not switched it off by setting to None.
        if automl_settings.window_size is not None:
            dict_time_series[constants.TimeSeriesInternal.WINDOW_SIZE] = automl_settings.window_size
        if automl_settings.lags is not None:
            dict_time_series[constants.TimeSeriesInternal.LAGS_TO_CONSTRUCT] = automl_settings.lags
        if hasattr(automl_settings, constants.TimeSeries.SEASONALITY):
            dict_time_series[constants.TimeSeries.SEASONALITY] = \
                getattr(automl_settings, constants.TimeSeries.SEASONALITY)
        if hasattr(automl_settings, constants.TimeSeries.USE_STL):
            dict_time_series[constants.TimeSeries.USE_STL] = \
                getattr(automl_settings, constants.TimeSeries.USE_STL)
        if hasattr(automl_settings, constants.TimeSeries.FREQUENCY):
            dict_time_series[constants.TimeSeries.FREQUENCY] = \
                getattr(automl_settings, constants.TimeSeries.FREQUENCY)
        return dict_time_series
    else:
        return None


def _get_gpu_training_params_dict(automl_settings: Any) -> Optional[Dict[str, str]]:
    """
    Get gpu training related parameter data.

    Arguments:
        automl_settings {AutoMLSettings} -- automl settings object

    Returns:
        dict -- a dictionary of gpu training info

    """
    if hasattr(automl_settings, 'is_gpu') and automl_settings.is_gpu:
        dict_gpu_training = {
            "processing_unit_type": "gpu"
        }
        return dict_gpu_training
    else:
        return None


def get_primary_metrics(task: str) -> List[str]:
    """
    Get the primary metrics supported for a given task as a list.

    :param task: string "classification" or "regression".
    :return: A list of the primary metrics supported for the task.
    """
    if task == constants.Tasks.CLASSIFICATION:
        return list(constants.Metric.CLASSIFICATION_PRIMARY_SET)
    elif task == constants.Tasks.REGRESSION:
        return list(constants.Metric.REGRESSION_PRIMARY_SET)
    elif task == constants.Tasks.IMAGE_CLASSIFICATION:
        return list(constants.Metric.IMAGE_CLASSIFICATION_PRIMARY_SET)
    elif task == constants.Tasks.IMAGE_MULTI_LABEL_CLASSIFICATION:
        return list(constants.Metric.IMAGE_MULTI_LABEL_CLASSIFICATION_PRIMARY_SET)
    elif task == constants.Tasks.IMAGE_OBJECT_DETECTION:
        return list(constants.Metric.IMAGE_OBJECT_DETECTION_PRIMARY_SET)
    else:
        raise NotImplementedError("Unsupported task.")


def convert_dict_values_to_str(input_dict: Dict[Any, Any]) -> Dict[str, str]:
    """
    Convert a dictionary's values so that every value is a string.

    :param input_dict: the dictionary that should be converted
    :return: a dictionary with all values converted to strings
    """
    fit_output_str = {}
    for key in input_dict:
        if input_dict[key] is None:
            fit_output_str[str(key)] = ''
        else:
            # Cast to string to avoid warnings (PR 143137)
            fit_output_str[str(key)] = str(input_dict[key])
    return fit_output_str


def to_ordinal_string(integer: int) -> str:
    """
    Convert an integer to an ordinal string.

    :param integer:
    :return:
    """
    return "%d%s" % (integer, "tsnrhtdd"[(integer / 10 % 10 != 1) * (integer % 10 < 4) * integer % 10::4])


# Regular expressions for date time detection
date_regex1 = re.compile(r'(\d+/\d+/\d+)')
date_regex2 = re.compile(r'(\d+-\d+-\d+)')


def is_known_date_time_format(datetime_str: str) -> bool:
    """
    Check if a given string matches the known date time regular expressions.

    :param datetime_str: Input string to check if it's a date or not
    :return: Whether the given string is in a known date time format or not
    """
    if date_regex1.search(datetime_str) is None and date_regex2.search(datetime_str) is None:
        return False

    return True


def get_error_code(exception: BaseException, as_hierarchy: bool = False) -> str:
    """
    Build the error code from an exception.

    :param exception: The exception that fails the run.
    :param as_hierarchy: If the complete error hierarchy should be returned
    :return: Return the str containing error_code. If as_hierarchy is True, the hierarchy returned is joined by a '.'
    """
    def get_code_from_hierarchy(hierarchy: ErrorHierarchy) -> str:
        if as_hierarchy:
            return str(hierarchy)
        else:
            return hierarchy.get_leaf() or ErrorTypes.Unclassified

    def get_error_code_from_exception(ex: AzureMLException) -> str:
        if getattr(ex, '_azureml_error', None) is not None:
            if as_hierarchy:
                return ".".join(ex._azureml_error.error_definition.code_hierarchy)
            return cast(str, ex._azureml_error.error_definition.code)

        error_response = ex._serialize_json()
        error_hierarchy = ErrorHierarchy(error_response)
        return get_code_from_hierarchy(error_hierarchy)

    error_code = ErrorTypes.Unclassified
    try:
        if isinstance(exception, MemoryError):
            # create an empty MemoryLimitException to get the right hierarchy
            memory_exception = MemorylimitException()
            error_code = get_error_code_from_exception(memory_exception)
        elif isinstance(exception, AzureMLException):
            error_code = get_error_code_from_exception(exception)
        elif isinstance(exception, AzureMLServiceException):
            if hasattr(exception, 'error'):
                # Extract the ErrorResponse from the exception sent by the service
                error_response = exception.error
                error_hierarchy = ErrorHierarchy(error_response)
                error_code = get_code_from_hierarchy(error_hierarchy)
            else:
                # create an empty ServiceException to get the right hierarchy
                service_exception = ServiceException()
                error_code = get_error_code_from_exception(service_exception)
    except json.decoder.JSONDecodeError:
        logger.warning("Failed to parse the ErrorResponse json from service. "
                       "Setting error_code as {}".format(error_code))
    except ValueError:
        logger.warning("Failed to extract error code from the exception. Setting error_code as {}".format(error_code))
    return str(error_code)


def get_min_points(window_size: int, lags: List[int], max_horizon: int, cv: Optional[int]) -> int:
    """
    Return the minimum number of data points needed for training.

    :param window_size: the rolling window size.
    :param lags: The lag size.
    :param max_horizon: the desired length of forecasting.
    :param cv: the number of cross validations.
    :return: the minimum number of data points.
    """
    min_points = max_horizon + max(window_size, max(lags)) + 1
    if cv is not None:
        min_points = min_points + cv + max_horizon
    return min_points

# from https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions


class suppress_stdout_stderr(object):
    """
    A context manager for doing a "deep suppression" of stdout and stderr.

    Will suppress all print, even if the print originates in a compiled
    C/Fortran sub-function. Will not suppress raised exceptions,
    since exceptions are printed to stderr just before a script exits,
    and after the context manager has exited.
    """

    def __init__(self):
        """Create the context manager."""
        # Open a pair of null files
        self.null_fds = [os.open(os.devnull, os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        """Assign the null pointers to stdout and stderr."""
        os.dup2(self.null_fds[0], 1)
        os.dup2(self.null_fds[1], 2)

    def __exit__(self, *_):
        """Re-assign the real stdout/stderr back to (1) and (2)."""
        os.dup2(self.save_fds[0], 1)
        os.dup2(self.save_fds[1], 2)
        # Close the null files
        for fd in self.null_fds + self.save_fds:
            os.close(fd)


def get_default_metric_with_objective(task):
    """Get the dictionary of metric -> objective for the given task.

    :param task: string "classification" or "regression"
    :return: dictionary of metric -> objective
    """
    if task == constants.Tasks.CLASSIFICATION:
        return constants.MetricObjective.Classification
    elif task == constants.Tasks.REGRESSION:
        return constants.MetricObjective.Regression
    elif task == constants.Tasks.IMAGE_CLASSIFICATION:
        return constants.MetricObjective.ImageClassification
    elif task == constants.Tasks.IMAGE_MULTI_LABEL_CLASSIFICATION:
        return constants.MetricObjective.ImageMultiLabelClassiciation
    elif task == constants.Tasks.IMAGE_OBJECT_DETECTION:
        return constants.MetricObjective.ImageObjectDetection
    elif task == constants.Subtasks.FORECASTING:
        return constants.MetricObjective.Forecast
    else:
        raise NotImplementedError


def minimize_or_maximize(metric, task=None):
    """Select the objective given a metric.

    Some metrics should be minimized and some should be maximized
    :param metric: the name of the metric to look up
    :param task: one of constants.Tasks.
    :return: returns one of constants.OptimizerObjectives.
    """
    if task is None:
        reg_metrics = get_default_metric_with_objective(
            constants.Tasks.REGRESSION)
        class_metrics = get_default_metric_with_objective(
            constants.Tasks.CLASSIFICATION)
        if metric in reg_metrics:
            task = constants.Tasks.REGRESSION
        elif metric in class_metrics:
            task = constants.Tasks.CLASSIFICATION
        else:
            msg = 'Could not find objective for metric "{0}"'
            raise ClientException(msg.format(metric)).with_generic_msg(msg.format("[MASKED]"))
    return get_default_metric_with_objective(task)[metric]
