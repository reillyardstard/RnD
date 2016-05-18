import logging

ilog_console = logging.WARNING  # desired max console logging level
ilog_file = logging.DEBUG       # desired max file logging level
ilog_filename = 'test.log'

ilog = logging.getLogger()
ilog.setLevel(logging.DEBUG)    # cap max level for all logging

# console logging
ch = logging.StreamHandler()
ch.setLevel(ilog_console)
formatter = logging.Formatter('%(message)s')
ch.setFormatter(formatter)
ilog.addHandler(ch)

# file logging
fh = logging.FileHandler(ilog_filename, mode='w')
fh.setLevel(ilog_file)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ilog.addHandler(fh)

if __name__ == "__main__":
    ilog.debug('debug message')
    ilog.info('info message')
    ilog.warn('warn message')
    ilog.error('error message')
    ilog.critical('critical message')
