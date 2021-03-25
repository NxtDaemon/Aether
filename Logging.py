import logging, coloredlogs

# Create formatters 
DETAILED = logging.Formatter("%(asctime)-30s %(module)-15s %(levelname)-8s %(funcName)-20s %(message)s")

# Custom Logger
logger = logging.getLogger(__name__)
coloredlogs.install(logger=logger,level=logging.DEBUG)
FileHandler = logging.FileHandler("DaemonBot_Errors.log")
FileHandler.setFormatter(DETAILED)
logger.addHandler(FileHandler)

