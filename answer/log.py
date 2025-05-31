import logging
from colorama import Fore, Style

# return created custom logger
def get_logger(name:str, filename:str ='', mode:str='a') -> object:
    """Sets up custom logger with rainbow coloring
    'filename' needed only if you need to log into file
    mode -> a = append | w = write"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()

    class ReinbowFormatter(logging.Formatter):
        # color or each logging level
        COLORS = {
            logging.CRITICAL : f'{Fore.RED}{Style.DIM}', 
            logging.ERROR : Fore.RED,
            logging.WARNING : Fore.YELLOW,
            logging.INFO : Fore.BLUE,
            logging.DEBUG : Fore.LIGHTBLACK_EX
        }

        def format(self, record):
            if record.levelno in self.COLORS:
                #save original levelname
                levelname_orig = record.levelname
                msg_orig = record.msg
                # add colors
                color = self.COLORS[record.levelno]
                record.levelname = f'{color}{record.levelname}{Style.RESET_ALL}'
                record.msg = f'{color}{record.msg}{Style.RESET_ALL}'
            formatted = super().format(record)
            # back to original state
            record.levelname = levelname_orig
            record.msg = msg_orig
            # return result
            return formatted

    console_handler.setFormatter(ReinbowFormatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt=r'%m/%d %H:%M:%S'))

    if not logger.handlers:
        logger.addHandler(console_handler)

    if len(filename) > 0:
        file_handler = logging.FileHandler(filename=filename, mode=mode)
        formaterr = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt=r'%m/%d %H:%M:%S')
        file_handler.setFormatter(formaterr)

        logger.addHandler(file_handler)

    return logger
