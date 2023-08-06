# flake8: noqa


class ExtensionError(Exception):
    """An error related to the construction of extensions.
    """
    pass


class Extensions:
    """Enumerates the IDs of common extensions."""
    ASSETS = 'asset'
    CHECKSUM = 'checksum'
    DATACUBE = 'datacube'
    DATETIME_RANGE = 'datetime-range'
    EO = 'eo'
    LABEL = 'label'
    POINTCLOUD = 'pointcloud'
    PROJECTION = 'projection'
    SAR = 'sar'
    SCIENTIFIC = 'scientific'
    SINGLE_FILE_STAC = 'single-file-stac'
    VIEW = 'view'
