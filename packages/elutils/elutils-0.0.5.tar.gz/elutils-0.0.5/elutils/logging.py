import logging
import datetime
import os

# LOGGING
def create_logger(logging_level=None, logger_name=None, logging_format = None,log_to_console=True,config=None):
    '''Does the setup for the log and the config file'''
    # Setup logging
    if logger_name is None:
        logger_name = __name__

    if logging_level is None:
        if config is None:
            logging_level = logging.INFO
        else:
            logging_level = config.get('development','log_level',fallback=logging.INFO)

    if logging_format is None:
        logging_format = logging.Formatter(fmt='%(asctime)s.%(msecs)03d|%(funcName)s|%(levelname)s|%(message)s',
                                           datefmt='%d-%b-%y %H:%M:%S')

    if config is not None:
        log_file_folder = config.get('logging','log_file_folder',fallback='logs')
    else:
        log_file_folder='logs'

    # if not a passed a config file, do not save on new day per default
    if config is not None:
        if config.getboolean('logging','save_new_day_in_own_folder',fallback=True):
            log_file_folder = os.path.join(log_file_folder,f'{datetime.datetime.today().strftime("%Y-%m-%d")}')
    else:
        # just save in the project folder
        pass

    # make sure the dir that the log file is to be placed in does exist
    if not os.path.exists(log_file_folder):
        os.makedirs(log_file_folder)

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging_level)
    handler = logging.FileHandler(os.path.join(log_file_folder,f'{logger_name}.log'))
    logger.addHandler(handler)
    handler.setFormatter(logging_format)
    if log_to_console:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        logger.addHandler(stream_handler)

    logger.debug(f'Logger "{logger_name}" created')

    if not log_to_console:
        logger.propagate = False


    return logger

def setup_global_logging(main_log_file_name=None,logging_level=None,config=None):
    if logging_level is None:
        logging_level = logging.INFO

    if main_log_file_name is None:
        main_log_file_name = 'main_log_file.log'

    if config is not None:
        log_file_folder = config.get('logging', 'log_file_folder', fallback='logs')
    else:
        log_file_folder = 'logs'

    if config.getboolean('logging','save_new_day_in_own_folder',fallback=False):
        log_file_folder = os.path.join(log_file_folder,f'{datetime.datetime.today().strftime("%Y-%m-%d")}')
    else:
        # just save in the folder
        pass

    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)


    try:
        logging.basicConfig(format='%(asctime)s.%(msecs)03d|%(filename)s|%(funcName)s|%(levelname)s|%(message)s',
                            datefmt='%d-%b-%y %H:%M:%S',
                            level=logging_level, filename=os.path.join(log_file_folder,main_log_file_name))
    except FileNotFoundError:
        # if it cannot find the log it will create the log file and folder
        log_file_folder = os.path.join(os.getcwd(), 'logs')
        if not os.path.isdir(log_file_folder):
            os.makedirs(log_file_folder)
        logging.basicConfig(format='%(asctime)s.%(msecs)03d|%(filename)s|%(funcName)s|%(levelname)s|%(message)s',
                            datefmt='%d-%b-%y %H:%M:%S',
                            level=logging_level, filename=os.path.join(log_file_folder,main_log_file_name))

    logging.propagate=False
    logging.info('Created global logger')