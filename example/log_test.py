"""
Simple log test, make prints and test debug level control
"""
from lps_utils.log import debug, info, warning, exception, error, set_warning_log_level

def main():
    """Main function make prints in all debug levels """
    debug('msg')
    info('msg')
    warning('msg')
    exception('msg')
    error('msg')

if __name__ == "__main__":
    print('Calling default main function')
    main()

    print('Calling default main function with warning log level')
    set_warning_log_level()
    main()
