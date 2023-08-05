"""
All configurations for pyflexebs
"""


from pytconf import Config, ParamCreator


class ConfigAlgo(Config):
    """
    Parameters for interval monitors
    """
    interval = ParamCreator.create_int(
        default=20,
        help_string="interval to monitor",
    )
    watermark_max = ParamCreator.create_int_or_none(
        default=70,
        help_string="max watermark for disk utilization",
    )
    # watermark_min = ParamCreator.create_int_or_none(
    #    default=None,
    #    help_string="min watermark for disk utilization",
    # )
    disregard = ParamCreator.create_list_str(
        default="/",
        help_string="what mount points to disregard",
    )
    file_systems = ParamCreator.create_list_str(
        default="ext4,xfs",
        help_string="what file systems to check",
    )
    increase_percent = ParamCreator.create_int(
        default=50,
        help_string="By how much to increase (in percentiles)",
    )
    increase_max_gb = ParamCreator.create_int(
        default=100,
        help_string="never increase by more than (in GB)",
    )
    dryrun = ParamCreator.create_bool(
        default=False,
        help_string="Should we dry run the actual operations?",
    )


class ConfigProxy(Config):
    """
    Configure proxy settings for the daemon
    """
    no_proxy = ParamCreator.create_str_or_none(
        default="localhost,.amdocs.com,169.254.169.254",
        help_string="what addresses to exempt from proxy",
    )
    http_proxy = ParamCreator.create_str_or_none(
        default="http://10.65.1.6:8080",
        help_string="http proxy",
    )
    https_proxy = ParamCreator.create_str_or_none(
        default="http://10.65.1.6:8080",
        help_string="https proxy",
    )
