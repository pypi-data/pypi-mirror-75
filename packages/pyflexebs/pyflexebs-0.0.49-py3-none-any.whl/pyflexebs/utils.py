from subprocess import Popen, PIPE


def run_with_logger(args, logger):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    logger.info("running [{}]".format(",".join(args)))
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode
    if exitcode != 0:
        logger.error("error in execution with code [{}]".format(exitcode))
        logger.debug("stdout was [{}]".format(out.decode()))
        logger.debug("stderr was [{}]".format(err.decode()))
    else:
        logger.info("execution was successful")
