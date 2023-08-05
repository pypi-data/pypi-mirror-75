"""
main entry point to the program
"""
import pylogconf.core
from pytconf import register_main, config_arg_parse_and_launch

from pyflexebs.endpoints.group_default import register_group_default
from pyflexebs.utils import get_logger


def register_all_groups():
    """
    registers all groups of operations with pytconf
    """
    register_group_default()


@register_main()
def main():
    """
    pyflexebs will enlarge/reduce your ebs volumes in real time
    """
    pylogconf.core.setup_systemd(name="pyflexebs")
    logger = get_logger()
    logger.info("starting")
    register_all_groups()
    config_arg_parse_and_launch()


if __name__ == '__main__':
    main()
