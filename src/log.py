import logging
from colorama import Fore, Style

# return created custom logger
def get_logger(name:str, to_file:bool = False, filename:str ='', mode:str='a') -> object:
    """Sets up custom logger with rainbow coloring
    'file' flag -> boolean (write logs to a file?)
    'filename' needed only if 'file'=True"""
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

        def fromat(self, record):
            if record.levelno in self.COLORS:
                record.levelname = f'{self.COLORS[record.levelno]}{record.levelname}{Style.RESET_ALL}'
                record.msg = f'{self.COLORS[record.levelno]}{record.msg}{Style.RESET_ALL}'
            return super().format(record)

    console_handler.setFormatter(ReinbowFormatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt=r'%m/%d %H:%M:%S'))

    logger.addHandler(console_handler)

    if to_file:
        file_handler = logging.FileHandler(filename=filename, mode=mode)
        formaterr = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt=r'%m/%d %H:%M:%S')
        file_handler.setFormatter(formaterr)

        logger.addHandler(file_handler)

    return logger
