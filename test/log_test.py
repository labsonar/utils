from lps_utils.log import *

def main():
    debug('main()')
    info('main()')
    warning('main()')
    exception('main()')
    error('main()')

if __name__ == "__main__":
    print('Calling default main function')
    main()
    set_warning_log_level()
    print('Calling default main function with warning log level')
    main()