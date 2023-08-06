from .utilities import requires_pandas


class Model:
    """Base class for Models."""
    pass


class Report(list):
    """Base class for Reports."""
    @requires_pandas
    def to_frame(self):
        """Method for producing a DataFrame of the provided data.

        This method **requires a `pandas` installation** to work - if `pandas`
        is not present, an `ImportError` will be raised.

        Returns:
            pd.DataFrame: [description]
        """
        return pd.DataFrame(self)
