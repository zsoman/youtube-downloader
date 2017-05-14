from urllib.request import urlopen


def check_internet(logger):
    for host_name in ['http://www.google.com/', 'http://www.facebook.com/']:
        for timeout in [1, 5, 10, 15]:
            try:
                logger.debug("checking internet connection...")
                urlopen(host_name, timeout=timeout)
                logger.debug("Internet is on!")
                return True
            except Exception as ex:
                pass
            logger.error("Failed to connect in {} seconds to {}!".format(timeout, host_name))
    return False
