from Logger import get_logger

def do_work():
    logger = get_logger("example")
    logger.info("[Worker] Info: This is a log message from worker_module.") 