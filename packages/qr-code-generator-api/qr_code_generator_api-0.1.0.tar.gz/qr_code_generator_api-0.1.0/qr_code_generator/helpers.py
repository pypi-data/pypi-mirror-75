#!/usr/bin/env python3
import yaml


class Config(dict):
    """
    Configuration class, behaves just like a dict.
    """
    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)

        # Basic configuration values
        self['API_URI'] = 'https://api.qr-code-generator.com/v1/create?'
        self['FORCE_OVERWRITE'] = False
        self['REQUIRED_PARAMETERS'] = [
            'access_token',
            'qr_code_text'
        ]
        self['OUT_FOLDER'] = 'out'
        self['OUTPUT_FOLDER'] = 'output'
        self['VERBOSE'] = False


class Options(dict):
    """
    Settings class, behaves just like a dict.
    """
    def __init__(self, *args, **kwargs):
        super(Options, self).__init__(*args, **kwargs)

        # Default settings for QR code generation
        self['access_token'] = None
        self['qr_code_text'] = None
        self['image_format'] = 'SVG'
        self['image_width'] = 500
        self['download'] = 0
        self['foreground_color'] = '#000000'
        self['background_color'] = '#FFFFFF'
        self['marker_left_inner_color'] = '#000000'
        self['marker_left_outer_color'] = '#000000'
        self['marker_right_inner_color'] = '#000000'
        self['marker_right_outer_color'] = '#000000'
        self['marker_bottom_inner_color'] = '#000000'
        self['marker_bottom_outer_color'] = '#000000'
        self['marker_left_template'] = 'version1'
        self['marker_right_template'] = 'version1'
        self['marker_bottom_template'] = 'version1'
        self['qr_code_logo'] = 'no-logo'
        self['frame_color'] = '#000000'
        self['frame_text'] = None
        self['frame_text_color'] = '#ffffff'
        self['frame_icon_name'] = 'app'
        self['frame_name'] = 'no-frame'


# Utility helper functions
def is_yaml(file):
    """
    Checks whether or not the specified file is a yaml-file.

    Parameters
    ----------
    file : str
        The relative path to the file that should be checked.

    Returns
    -------
    bool
        Whether or not the specified file is a yaml-file.
    """
    extension = file.split('.')[-1]
    if not extension == 'yaml':
        return False
    return True


def load_yaml(file):
    """
    Loads a yaml file into a Python dictionary.

    Parameters
    ----------
    file : str
        The relative path to the yaml-file that should be used to load settings.

    Raises
    ------
    ValueError
        The specified file is not a yaml-file and thus could not be loaded.

    Returns
    -------
    items : dict
        The dictionary loaded from a Yaml file.
    """
    if not is_yaml(file):
        raise ValueError()

    with open(file, "r") as f:
        items = yaml.load(f, Loader=yaml.FullLoader)

    return items
