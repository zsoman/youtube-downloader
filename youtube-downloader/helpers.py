from urllib.request import urlopen


def internet_on():
    for host_name in ['http://www.google.com/', 'http://www.facebook.com/']:
        for timeout in [1, 5, 10, 15]:
            try:
                print("checking internet connection..")
                urlopen(host_name, timeout=timeout)
                print("Internet is on!")
                return True
            except Exception as err:
                pass
            print("Failed to connect in {} seconds to {}!".format(timeout, host_name))
    return False
