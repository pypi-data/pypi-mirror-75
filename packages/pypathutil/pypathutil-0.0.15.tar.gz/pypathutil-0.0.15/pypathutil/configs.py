"""
All configurations for pypathutil
"""
import os

from pytconf import Config, ParamCreator


class ConfigSeparator(Config):
    """
    Parameters for configuring the separator
    """
    separator = ParamCreator.create_str(
        help_string="What is the path separator?",
        default=os.pathsep,
    )


class ConfigOps(Config):
    """
    Which operations to perform on the path
    """
    remove_non_abs = ParamCreator.create_bool(
        help_string="remove non absolute folder elements from the path?",
        default=True,
    )
    remove_non_folders = ParamCreator.create_bool(
        help_string="remove non folder elements from the path?",
        default=True,
    )
    remove_duplicates = ParamCreator.create_bool(
        help_string="remove duplicate elements from the path?",
        default=True,
    )


class ConfigPath(Config):
    """
    The existing path
    """
    path = ParamCreator.create_str(
        help_string="What is the path to work on?",
    )


class ConfigFolder(Config):
    """
    A folder name
    """
    folder = ParamCreator.create_str(
        help_string="A folder to work with"
    )


class ConfigHead(Config):
    """
    Configure whether we need head or tail
    """
    head = ParamCreator.create_bool(
        help_string="add to the head of the path?",
        default=True,
    )
