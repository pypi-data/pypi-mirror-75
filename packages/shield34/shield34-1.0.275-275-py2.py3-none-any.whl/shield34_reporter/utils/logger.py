import logging

class Shield34Logger():

    logger = logging.getLogger('shield34')
    @staticmethod
    def set_logger(logger):
        Shield34Logger.logger = logger

    @staticmethod
    def override_console_method():
        def console(msg):
            if msg:
                print(msg)

        Shield34Logger.logger.console = console
