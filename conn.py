import requests
from urlparse import urlparse
from requests import ConnectionError


def error_out(message, t):
    ''' Prints a readable exit status.

    >>> error_out('testing', 0)
    testing
    Closing in 0 seconds...
    'testing'
    '''
    print message
    print "Closing in {} seconds...".format(t)
    time.sleep(t)
    return message


def load_profile(profile_link=None, t=10):
    ''' Validates and returns a  profile link after loading it from the
    profile.cfg file.

    kwarg is for debugging.

    >>> load_profile('http://d3up.com/b/496741/batuo-dual-ls-5-9')
    'http://d3up.com/b/496741/batuo-dual-ls-5-9'


    >>> try:
    ...     load_profile('http://google.com', t=0)
    ... except Exception as e:
    ...     print repr(e)
    The profile link provided in profile.cfg is invalid!
    Closing in 0 seconds...
    ValueError('The profile link provided in profile.cfg is invalid!',)

    '''
    if not profile_link:
        f = open('profile.cfg')
        with f:
            print 'loading profile link from profile.cfg configuration file...'
            profile_link = f.next()

    parse = urlparse(profile_link)
    if parse.netloc == 'd3up.com':
        return profile_link
    else:
        m = error_out('The profile link provided in profile.cfg'
                      ' is invalid!', t)
        raise ValueError(m)


def download_data():
    ''' Downloads the data from the profile link specified in profile.cfg.
    Connects using requests.'''
    profile = load_profile()
    print 'downloading data now...'
    try:
        r = requests.get(profile)
        if r.status_code == 200:
            print 'download complete!'
            # sometimes you feel like a method, sometimes you dont.
            try:
                return r.content()
            except:
                return r.content

        else:
            m = error_out("Could not connect to d3up!", 10)
            raise IOError(m)
    except ConnectionError:
        m = error_out("Could not connect to the internet!", 10)
        raise ConnectionError
