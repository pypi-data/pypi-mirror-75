import logging
import sys
import types


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
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - Shield34 - %(message)s')
        formatter.datefmt = "%H:%M:%S"
        ch.setFormatter(formatter)
        ch.setLevel(logging.INFO)
        Shield34Logger.logger.addHandler(ch)

        Shield34Logger.blank_handler = logging.StreamHandler()
        Shield34Logger.blank_handler.setLevel(logging.INFO)
        Shield34Logger.blank_handler.setFormatter(logging.Formatter(fmt=''))

        def log_newline(self, how_many_lines=1):
            # Switch handler, output a blank line
            origHandlers = Shield34Logger.logger.handlers.copy()
            for handler in Shield34Logger.logger.handlers:
                Shield34Logger.logger.removeHandler(handler)
            self.addHandler(Shield34Logger.blank_handler)
            for i in range(how_many_lines):
                self.info('')
            # Switch back
            self.removeHandler(Shield34Logger.blank_handler)
            for handler in origHandlers:
                Shield34Logger.logger.addHandler(handler)

        Shield34Logger.logger.newline = types.MethodType(log_newline, Shield34Logger.logger)



