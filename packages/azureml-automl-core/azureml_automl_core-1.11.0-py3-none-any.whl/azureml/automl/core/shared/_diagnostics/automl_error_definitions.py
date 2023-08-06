# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import Optional

from azureml._common._error_definition import error_decorator
from azureml._common._error_definition.system_error import ClientError
from azureml._common._error_definition.user_error import ArgumentInvalid, ArgumentMismatch, NotReady, NotSupported, \
    BadArgument, NotFound, InvalidDimension, BadData, ArgumentOutOfRange, Authentication, MalformedArgument, Memory, \
    Timeout
from azureml.automl.core.shared._diagnostics.error_strings import AutoMLErrorStrings


# region ArgumentInvalid
@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidArgumentType(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_ARGUMENT_TYPE


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidArgumentWithSupportedValues(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_ARGUMENT_WITH_SUPPORTED_VALUES


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidArgumentWithSupportedValuesForTask(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_ARGUMENT_WITH_SUPPORTED_VALUES_FOR_TASK


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidArgumentForTask(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_ARGUMENT_FOR_TASK


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class TensorflowAlgosAllowedButDisabled(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TENSORFLOW_ALGOS_ALLOWED_BUT_DISABLED


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidCVSplits(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_CV_SPLITS


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InvalidInputDatatype(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_INPUT_DATATYPE


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class InputDataWithMixedType(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INPUT_DATA_WITH_MIXED_TYPE


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class AllAlgorithmsAreBlocked(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.ALL_ALGORITHMS_ARE_BLOCKED


@error_decorator(details_uri="https://aka.ms/AutoMLConfig")
class InvalidComputeTargetForDatabricks(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_COMPUTE_TARGET_FOR_DATABRICKS


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class EmptyLagsForColumns(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.EMPTY_LAGS_FOR_COLUMNS


@error_decorator(use_parent_error_code=True)
class TimeseriesInvalidDateOffsetType(ArgumentInvalid):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_INVALID_DATE_OFFSET_TYPE


@error_decorator(use_parent_error_code=True)
class OnnxNotEnabled(ArgumentInvalid):
    @property
    def message_foramt(self):
        return AutoMLErrorStrings.ONNX_NOT_ENABLED


@error_decorator(use_parent_error_code=True)
class OnnxSplitsNotEnabled(ArgumentInvalid):
    @property
    def message_foramt(self):
        return AutoMLErrorStrings.ONNX_SPLITS_NOT_ENABLED
# endregion


# region ArgumentMismatch
@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class AllowedModelsSubsetOfBlockedModels(ArgumentMismatch):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.ALLOWED_MODELS_SUBSET_OF_BLOCKED_MODELS


@error_decorator(details_uri="https://aka.ms/AutoMLConfig")
class ConflictingValueForArguments(ArgumentMismatch):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.CONFLICTING_VALUE_FOR_ARGUMENTS


@error_decorator(use_parent_error_code=True)
class InvalidDampingSettings(ConflictingValueForArguments):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_DAMPING_SETTINGS
# endregion


# region BadArgument
@error_decorator(details_uri="https://aka.ms/AutoMLConfig")
class InvalidFeaturizer(BadArgument):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_FEATURIZER


@error_decorator(use_parent_error_code=True)
class InvalidSTLFeaturizerForMultiplicativeModel(InvalidFeaturizer):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_STL_FEATURIZER_FOR_MULTIPLICATIVE_MODEL
# endregion


# region ArgumentOutOfRange
@error_decorator(use_parent_error_code=True)
class NCrossValidationsExceedsTrainingRows(ArgumentOutOfRange):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.N_CROSS_VALIDATIONS_EXCEEDS_TRAINING_ROWS
# endregion


# region MalformedArgument
class MalformedJsonString(MalformedArgument):
    @property
    def message_format(self):
        return AutoMLErrorStrings.MALFORMED_JSON_STRING
# endregion


# region NotReady
class ComputeNotReady(NotReady):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.COMPUTE_NOT_READY
# endregion


# region NotFound
class MethodNotFound(NotFound):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.METHOD_NOT_FOUND


class DatastoreNotFound(NotFound):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.DATASTORE_NOT_FOUND


class DataPathNotFound(NotFound):
    @property
    def message_format(self):
        return AutoMLErrorStrings.DATA_PATH_NOT_FOUND


class MissingSecrets(NotFound):
    @property
    def message_format(self):
        return AutoMLErrorStrings.MISSING_SECRETS


@error_decorator(use_parent_error_code=True)
class NoMetricsData(NotFound):
    @property
    def message_format(self):
        return AutoMLErrorStrings.NO_METRICS_DATA
# endregion


# region NotSupported
@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class LargeDataAlgorithmsWithUnsupportedArguments(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.LARGE_DATA_ALGORITHMS_WITH_UNSUPPORTED_ARGUMENTS


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class FeatureUnsupportedForIncompatibleArguments(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.FEATURE_UNSUPPORTED_FOR_INCOMPATIBLE_ARGUMENTS


@error_decorator(use_parent_error_code=True, details_uri="https://aka.ms/AutoMLConfig")
class NonDnnTextFeaturizationUnsupported(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.NON_DNN_TEXT_FEATURIZATION_UNSUPPORTED


class InvalidOperationOnRunState(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INVALID_OPERATION_ON_RUN_STATE


class RemoteInferenceUnsupported(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.REMOTE_INFERENCE_UNSUPPORTED


# A package is either missing or has an incompatible version installed.
class IncompatibleOrMissingDependency(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INCOMPATIBLE_OR_MISSING_DEPENDENCY


# Snapshot is either larger than 300MB or exceeds max allowed files.
@error_decorator(use_parent_error_code=False, details_uri="http://aka.ms/aml-largefiles")
class SnapshotLimitExceeded(NotSupported):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.SNAPSHOT_LIMIT_EXCEED
# endregion


# region InvalidDimension
class DatasetsFeatureCountMismatch(InvalidDimension):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.DATASETS_FEATURE_COUNT_MISMATCH
# endregion


# region BadData
@error_decorator(details_uri="https://aka.ms/datasetfromdelimitedfiles")
class InconsistentNumberOfSamples(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.INCONSISTENT_NUMBER_OF_SAMPLES


class MissingColumnsInData(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.MISSING_COLUMNS_IN_DATA


class PandasDatetimeConversion(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.PANDAS_DATETIME_CONVERSION_ERROR


class TimeseriesColumnNamesOverlap(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_COLUMN_NAMES_OVERLAP


class TimeseriesTypeMismatchFullCV(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TIMESERIES_TYPE_MISMATCH_FULL_CV


class TooManyLabels(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.TOO_MANY_LABELS


class BadDataInWeightColumn(BadData):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.BAD_DATA_IN_WEIGHT_COLUMN
# endregion


# region Authentication
class DataPathInaccessible(Authentication):
    @property
    def message_format(self):
        return AutoMLErrorStrings.DATA_PATH_INACCESSIBLE
# endregion


# region ClientError
@error_decorator(details_uri="https://docs.microsoft.com/en-us/azure/machine-learning/"
                             "resource-known-issues#automated-machine-learning")
class AutoMLInternal(ClientError):
    """Base class for all AutoML system errors."""
    @property
    def message_format(self):
        return AutoMLErrorStrings.AUTOML_INTERNAL
# endregion


# region Memory
class Memorylimit(Memory):
    @property
    def message_format(self):
        return AutoMLErrorStrings.DATA_MEMORY_ERROR


@error_decorator(use_parent_error_code=True)
class MemoryExhausted(Memory):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.MEMORY_EXHAUSTED
# endregion


# region Timeout
@error_decorator(is_transient=True, details_uri="https://aka.ms/storageoptimization")
class DatasetFileRead(Timeout):
    @property
    def message_format(self) -> str:
        return AutoMLErrorStrings.DATASET_FILE_READ
# endregion
