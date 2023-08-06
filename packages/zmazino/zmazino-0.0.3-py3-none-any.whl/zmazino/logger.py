import configparser, os, logging


FORMAT = '%(asctime)s :: %(levelname)-7s --- %(message)s (%(filename)s:%(lineno)d)'

class Logger:

    def __init__(self, conf_tag='logger', conf_file='config.ini'):
        super().__init__()

        parser = configparser.ConfigParser()

        if os.path.isfile(conf_file):
            parser.read(conf_file)
        else:
            raise FileNotFoundError()
        
        try:
            config = parser[conf_tag]
            name = config['name']
            file = config['file']
            format = logging.Formatter(FORMAT)
        except:
            name = 'root'
            file = './app.log'
            format = logging.Formatter(FORMAT)


        # create the logging instance for logging
        self._logger = logging.getLogger(name)
        self._logger.setLevel(logging.INFO)
        # create the file handler
        file_logger = logging.FileHandler(file)
        file_logger.setFormatter(format)
        # create the console handler
        console_logger = logging.StreamHandler()
        console_logger.setLevel(logging.INFO)
        console_logger.setFormatter(format)
        # finally, add the handlers to the base logger
        self._logger.addHandler(file_logger)
        self._logger.addHandler(console_logger)

    def info(self, msg:str, exc_info=False):
        self._logger.info(msg, exc_info=exc_info)
    
    def warn(self, msg:str, exc_info=False):
        self._logger.warn(msg, exc_info=exc_info)
    
    def error(self, msg:str, exc_info=False):
        self._logger.error(msg, exc_info=exc_info)
