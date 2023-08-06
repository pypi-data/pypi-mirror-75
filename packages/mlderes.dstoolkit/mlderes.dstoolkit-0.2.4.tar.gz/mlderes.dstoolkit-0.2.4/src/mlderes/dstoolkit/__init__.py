__version__ = "0.2.4"
from .io import (
    get_latest_filename,
    get_latest_data_filename,
    make_ts_filename,
    write_data,
    read_latest,
    DataFolder,
)

from .cleaning import (
    replace_string_in_col_name,
    remove_columns,
    convert_to_bool,
    convert_from_bool,
    remove_duplicates,
)

