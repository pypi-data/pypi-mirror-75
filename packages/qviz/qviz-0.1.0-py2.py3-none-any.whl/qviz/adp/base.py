from abc import ABC, abstractmethod


class AutomatedPreparation(ABC):

    def __init__(self):
        pass

    def set_args(self, missing_values=None, remove_outliers=False, threshold_cardinality=None, scaling_method=None,
                 do_PCA=False, target_variable=None):
        self.missing_values = missing_values
        self.remove_outliers = remove_outliers
        self.threshold_cardinality = threshold_cardinality
        self.scaling_method = int(scaling_method) if scaling_method is not None else None
        self.do_PCA = do_PCA
        if target_variable == "None":
            target_variable = None
        self.target_variable = target_variable

    @abstractmethod
    def get_df(self, backend, *args):
        pass

    @abstractmethod
    def _replace_missing_data(self, df):
        return df

    @abstractmethod
    def _is_numeric(self, data_type):
        pass

    @abstractmethod
    def _interpolate_missing_data(self, df, types):
        return df

    @abstractmethod
    def _detect_remove_outliers(self, df, types):
        return df

    @abstractmethod
    def _one_hot_encode(self, df, column):
        return df

    @abstractmethod
    def _label_encode(self, df, column):
        return df

    @abstractmethod
    def _encode_categorical(self, df, types):
        return df

    @staticmethod
    @abstractmethod
    def get_scaling_options():
        pass

    @abstractmethod
    def _scale_df(self, df):
        return df

    @abstractmethod
    def _perform_pca(self, df):
        return df

    @abstractmethod
    def automated_data_preparation(self, df, description, progress):
        return df

    @abstractmethod
    def save_df(self, df, backend, args):
        pass
