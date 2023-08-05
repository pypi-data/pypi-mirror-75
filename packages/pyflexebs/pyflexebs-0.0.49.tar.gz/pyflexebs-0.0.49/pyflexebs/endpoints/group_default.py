"""
The default group of operations that pyflexebs has
"""
import logging
import os
import sys
import time

import bitmath
import boto3
import ec2_metadata
import psutil as psutil
from hurry.filesize import size
from pylogconf.core import create_pylogconf_file
from pytconf import register_endpoint, register_function_group

import pyflexebs
import pyflexebs.version
from pyflexebs.configs import ConfigAlgo, ConfigProxy

import pypathutil.common

from pyflexebs.utils import run_with_logger

GROUP_NAME_DEFAULT = "default"
GROUP_DESCRIPTION_DEFAULT = "all pyflexebs commands"

TAG_DONT_RESIZE = "dont_resize"


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
    print(pyflexebs.version.VERSION_STR)


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[ConfigAlgo, ConfigProxy],
)
def daemon() -> None:
    """
    Run daemon and monitor disk utilization
    """
    logger = get_logger()
    configure_proxy()
    check_tools()
    check_root()
    metadata = ec2_metadata.ec2_metadata
    instance_id = metadata.instance_id
    ec2_resource = boto3.resource('ec2', region_name=metadata.region)
    instance = ec2_resource.Instance(instance_id)
    tags = instance.tags
    ec2_client = boto3.client('ec2', region_name=metadata.region)

    volumes = instance.volumes.all()
    device_to_volume = dict()
    for volume in volumes:
        for a in volume.attachments:
            device = normalize_device(a["Device"])
            device_to_volume[device] = volume

    while True:
        logger.info("checking disk utilization")
        for p in psutil.disk_partitions():
            if p.mountpoint in ConfigAlgo.disregard:
                continue
            if p.fstype not in ConfigAlgo.file_systems:
                continue
            if TAG_DONT_RESIZE in tags:
                continue
            logger.info("checking {} {} {}".format(
                p.device,
                p.mountpoint,
                p.fstype,
            ))
            if ConfigAlgo.watermark_max is not None:
                if psutil.disk_usage(p.mountpoint).percent >= ConfigAlgo.watermark_max:
                    logger.info("max watermark detected at disk {} mountpoint {}".format(
                        p.device,
                        p.mountpoint,
                    ))
                    logger.info("percent is {}, total is {}, used is {}".format(
                        psutil.disk_usage(p.mountpoint).percent,
                        psutil.disk_usage(p.mountpoint).total,
                        psutil.disk_usage(p.mountpoint).used,
                    ))
                    enlarge_volume(p, device_to_volume, ec2_client)
        time.sleep(ConfigAlgo.interval)


def normalize_device(dev: str) -> str:
    """
    turns /dev/sdb to /dev/xvdb (if needed)
    """
    last_part = dev.split("/")[2]
    if last_part.startswith("sd"):
        drive = last_part[2:]
        return "/dev/xvd{}".format(drive)
    return dev


def enlarge_volume(p, device_to_volume, ec2):
    logger = get_logger()
    if p.device not in device_to_volume:
        logger.error("Cannot find device [{}]. Not resizing".format(p.device))
        return
    volume = device_to_volume[p.device]
    volume_id = volume.id
    # volume_size = volume.size
    volume_size = psutil.disk_usage(p.mountpoint).total
    logger.info("total is [{}]".format(size(volume_size)))
    volume_size_float = float(volume_size)
    volume_size_float /= 100
    volume_size_float *= (100+ConfigAlgo.increase_percent)
    new_size = int(volume_size_float)
    if volume.size < new_size:
        logger.info("trying to increase size to [{}]".format(size(new_size)))
        # noinspection PyBroadException
        try:
            result = ec2.modify_volume(
                DryRun=ConfigAlgo.dryrun,
                VolumeId=volume_id,
                Size=bitmath.Byte(new_size).to_GB(),
            )
            logger.debug("Success in increasing size [{}]".format(result))
            logger.info("Success in increasing size")
        except Exception as e:
            logger.info("Failure in increasing size [{}]".format(e))
    # resize the file system
    logger.info("doing [{}] extension", format(p.fstype))
    if p.fstype == "ext4":
        if not ConfigAlgo.dryrun:
            run_with_logger([
                "resize2fs",
                p.device,
            ], logger=logger)
    if p.fstype == "xfs":
        if not ConfigAlgo.dryrun:
            run_with_logger([
                "xfs_growfs",
                "-d",
                p.mountpoint,
            ], logger=logger)


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[ConfigAlgo, ConfigProxy],
)
def show_volumes() -> None:
    """
    Show volume information
    """
    logger = get_logger()
    configure_proxy()
    metadata = ec2_metadata.ec2_metadata
    # check that we have attached an IAM role to the machine
    # we need this for credentials
    if metadata.iam_info is None:
        logger.error("No IAM role attached to instance. Please fix instance configuration.")
        return
    logger.info("Found iam_info, good...")
    instance_id = metadata.instance_id
    session = boto3.session.Session(region_name=metadata.region)
    ec2 = session.resource('ec2')
    instance = ec2.Instance(instance_id)
    logger.info("instance is [{}]".format(instance_id))
    volumes = instance.volumes.all()
    for v in volumes:
        dump(v)


def dump(obj):
    """
    debugging function to dump objects
    """
    for attr in dir(obj):
        if attr.startswith("__"):
            continue
        print("obj.%s = %r" % (attr, getattr(obj, attr)))


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
)
def create_pylogconf() -> None:
    """
    create a pylogconf configuration file
    """
    create_pylogconf_file()


@register_endpoint(
    group=GROUP_NAME_DEFAULT,
    configs=[ConfigProxy],
)
def show_policies() -> None:
    """
    Show policies that are configured for your role
    """
    logger = get_logger()
    configure_proxy()
    metadata = ec2_metadata.ec2_metadata
    # check that we have attached an IAM role to the machine
    # we need this for credentials
    if metadata.iam_info is None:
        logger.error("No IAM role attached to instance. Please fix instance configuration.")
        return
    logger.info("Found iam_info, good...")
    logger.info("found [{}]".format(metadata.iam_info))
    instance_profile_arn = metadata.iam_info["InstanceProfileArn"]
    logger.info("instance_profile_arn [{}]".format(instance_profile_arn))
    name = instance_profile_arn.split("/")[1]
    logger.info("name [{}]".format(name))
    session = boto3.session.Session(region_name=metadata.region)
    iam = session.client('iam')
    policy_list = iam.list_attached_role_policies(RoleName=name)
    for policy in policy_list["AttachedPolicies"]:
        policy_name = policy["PolicyName"]
        policy_arn = policy["PolicyArn"]
        logger.info("policy_name: [{}]".format(policy_name))
        logger.info("policy_arn: [{}]".format(policy_arn))


def configure_proxy():
    if ConfigProxy.http_proxy is not None:
        os.environ['http_proxy'] = ConfigProxy.http_proxy
        os.environ['HTTP_PROXY'] = ConfigProxy.http_proxy
    if ConfigProxy.https_proxy is not None:
        os.environ['https_proxy'] = ConfigProxy.https_proxy
        os.environ['HTTPS_PROXY'] = ConfigProxy.https_proxy
    if ConfigProxy.no_proxy is not None:
        os.environ['no_proxy'] = ConfigProxy.no_proxy
        os.environ['NO_PROXY'] = ConfigProxy.no_proxy


def check_tools():
    """
    Check that the command line tools we need are available
    """
    logger = get_logger()
    problems = False
    for app in ["xfs_growfs", "resize2fs"]:
        if pypathutil.common.find_in_standard_path(app) is None:
            problems = True
            logger.error("please install executable [{}]".format(app))
    if problems:
        sys.exit(1)


def get_logger():
    return logging.getLogger(pyflexebs.LOGGER_NAME)


def check_root():
    if not os.geteuid() == 0:
        sys.exit('Script must be run as root')
