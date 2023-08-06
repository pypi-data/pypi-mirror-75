"""
The default group of operations that pypathutil has
"""

from pytconf import register_endpoint, register_function_group

import pypathutil.version
from pypathutil import common
from pypathutil.configs import ConfigFolder, ConfigPath, ConfigHead, ConfigSeparator, ConfigOps

GROUP_NAME_DEFAULT = "default"
GROUP_DESCRIPTION_DEFAULT = "all pypathutil commands"


def register_group_default():
    """
    register the name and description of this group
    """
    register_function_group(
        function_group_name=GROUP_NAME_DEFAULT,
        function_group_description=GROUP_DESCRIPTION_DEFAULT,
    )


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
)
def version() -> None:
    """
    Print version
    """
    print(pypathutil.version.VERSION_STR)


@register_endpoint(
    configs=[
        ConfigFolder,
        ConfigPath,
        ConfigHead,
        ConfigSeparator,
        ConfigOps,
    ]
)
def add() -> None:
    """
    add two paths together
    """
    new_path = common.add(
        path=ConfigPath.path,
        folder=ConfigFolder.folder,
        head=ConfigHead.head,
        separator=ConfigSeparator.separator,
        remove_duplicates=ConfigOps.remove_duplicates,
        remove_non_folders=ConfigOps.remove_non_folders,
        remove_non_abs=ConfigOps.remove_non_abs,
    )
    print(new_path)


@register_endpoint(
    configs=[
        ConfigSeparator,
        ConfigOps,
        ConfigPath,
    ]
)
def clean() -> None:
    """
    clean a path, removing elements which repeat or are not valid paths
    """
    path = common.clean(
        path=ConfigPath.path,
        separator=ConfigSeparator.separator,
        remove_duplicates=ConfigOps.remove_duplicates,
        remove_non_folders=ConfigOps.remove_non_folders,
        remove_non_abs=ConfigOps.remove_non_abs,
    )
    print(path)


@register_endpoint(
    configs=[
        ConfigOps,
        ConfigSeparator,
        ConfigPath,
        ConfigFolder,
    ]
)
def remove() -> None:
    """ remove element from a path """
    new_path = common.remove(
        path=ConfigPath.path,
        folder=ConfigFolder.folder,
        separator=ConfigSeparator.separator,
        remove_duplicates=ConfigOps.remove_duplicates,
        remove_non_folders=ConfigOps.remove_non_folders,
        remove_non_abs=ConfigOps.remove_non_abs,
    )
    print(new_path)
