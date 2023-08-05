import os
from azureml.designer.modules.vowpal_wabbit.common.dataset import Dataset
from azureml.designer.modules.vowpal_wabbit.common.entry_utils import params_loader
from azureml.designer.modules.vowpal_wabbit.common.vowpal_wabbit_model_wrapper import VowpalWabbitModelWrapper, \
    DataFormat, VowpalWabbitTrainer
from azureml.designer.modules.vowpal_wabbit.common.entry_param import Boolean
from azureml.studio.core.io.data_frame_directory import load_data_frame_from_directory
from azureml.studio.core.logger import module_logger
from azureml.studio.core.schema import ColumnTypeName
from azureml.studio.internal.error import InvalidDatasetError, ErrorMapping, NullOrEmptyError, \
    TooFewRowsInDatasetError, UnexpectedNumberOfColumnsError, InvalidColumnTypeError
from azureml.studio.core.io.model_directory import save_model_to_directory

TRAINING_DATASET_NAME = "Training data"
NAME_OF_THE_TRAINING_DATA_PARAM = "Name of the training data file"


class TrainVowpalWabbitModelModule:
    @staticmethod
    def _prepare_training_dataset(training_data: str, name_of_the_training_data_file: str = None):
        """Prepare training data.

        Training data can be of two types:
        1. AnyDirectory, where there is a plain text file, named 'name_of_the_training_data_file'. Each line of this
        file is an example of VW/SVMLight format. For VW format details, please refer to:
        https://github.com/VowpalWabbit/vowpal_wabbit/wiki/Input-format
        2. DataFrameDirectory, which has only one column, and each row of which is an example with VW/SVMLight format.
        """
        # try to load DataFrameDirectory
        ErrorMapping.verify_not_null_or_empty(training_data, name=TRAINING_DATASET_NAME)
        try:
            dfd = load_data_frame_from_directory(load_from_dir=training_data)
            training_dataset = Dataset(df=dfd.data, column_attributes=dfd.schema_instance.column_attributes,
                                       name=TRAINING_DATASET_NAME)
            module_logger.info("Loaded training data from DataFrameDirectory.")
            TrainVowpalWabbitModelModule._validate_training_dataset(training_dataset)
            return training_dataset
        except Exception as e:
            if isinstance(e, (TooFewRowsInDatasetError, InvalidColumnTypeError, UnexpectedNumberOfColumnsError)):
                raise e
            module_logger.warning(
                f"Failed to load the path as DataFrameDirectory, will try to load it as file dataset.")

        if os.path.isfile(training_data):
            # AnyDirectory can also be a file path
            return training_data
        elif os.path.isdir(training_data):
            if name_of_the_training_data_file is None:
                ErrorMapping.throw(NullOrEmptyError(
                    name=NAME_OF_THE_TRAINING_DATA_PARAM,
                    troubleshoot_hint=f'Load data from a directory without a training data file name specified.'))
            else:
                # if load dfd failed, then the input is an AnyDirectory, which training data file with specified name in
                training_dataset = os.path.join(training_data, name_of_the_training_data_file)
                if not os.path.exists(training_dataset):
                    ErrorMapping.throw(InvalidDatasetError(dataset1=TRAINING_DATASET_NAME,
                                                           reason=f'"{name_of_the_training_data_file}" does not exist'))
                if not os.path.isfile(training_dataset):
                    ErrorMapping.throw(InvalidDatasetError(dataset1=TRAINING_DATASET_NAME,
                                                           reason=f'"{name_of_the_training_data_file}" is not a file'))
                module_logger.info("Loaded training data from AnyDirectory.")
                return training_dataset
        else:
            raise InvalidDatasetError(dataset1=TRAINING_DATASET_NAME,
                                      reason=f"cannot load {training_data} as {type(training_data)} type.")

    @staticmethod
    def _validate_training_dataset(training_dataset):
        ErrorMapping.verify_number_of_rows_greater_than_or_equal_to(curr_row_count=training_dataset.row_count,
                                                                    required_row_count=1,
                                                                    arg_name=training_dataset.name)
        ErrorMapping.verify_number_of_columns_equal_to(curr_column_count=training_dataset.column_count,
                                                       required_column_count=1, arg_name=training_dataset.name)
        ErrorMapping.verify_element_type(type_=training_dataset.get_column_type(0),
                                         expected_type=ColumnTypeName.STRING,
                                         column_name=training_dataset.columns[0], arg_name=training_dataset.name)

    @params_loader
    def run(self,
            training_data: str,
            output_readable_model_file: Boolean,
            output_inverted_hash_file: Boolean,
            specify_file_type: DataFormat,
            trained_vowpal_wabbit_model: str,
            vw_arguments: str = None,
            pre_trained_vowpal_wabbit_model: VowpalWabbitModelWrapper = None,
            name_of_the_training_data_file: str = None):
        training_dataset = self._prepare_training_dataset(training_data, name_of_the_training_data_file)
        vw_model_wrapper = VowpalWabbitModelWrapper()
        vw_trainer = VowpalWabbitTrainer(vw_model_wrapper)
        vw_trainer.train(arg_str=vw_arguments, training_data=training_dataset, data_format=specify_file_type,
                         output_readable_model_file=output_readable_model_file,
                         output_inverted_hash_file=output_inverted_hash_file,
                         pre_trained_model=pre_trained_vowpal_wabbit_model)
        # trained_model is trained model output path, and the variable name is defined by the module spec
        save_model_to_directory(save_to=trained_vowpal_wabbit_model, model=vw_model_wrapper)
        return vw_model_wrapper,
