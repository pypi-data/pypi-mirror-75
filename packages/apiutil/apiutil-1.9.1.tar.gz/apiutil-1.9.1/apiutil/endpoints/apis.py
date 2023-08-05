# encoding: utf-8

import re
from future.utils import iteritems
from configurationutil import (CfgItems,
                               InheritableCfgItem,
                               DefaultInheritableConstant)
from classutils.decorators import class_cache_result, clear_class_cached_results
from .config import RegisterAPIConfig
from ._constants import API_CONFIG, APIKeysConstant
from .hosts import Hosts
from .endpoints import Endpoints

MATCH_PORT = re.compile(r"(.+)//(.+):([0-9]+)/(.+)")


def add_default_port_to_uri(uri):
    try:
        MATCH_PORT.match(uri).groups()
    except AttributeError:
        uri = uri.split('/')
        uri[2] = uri[2] + ':80'
        uri = '/'.join(uri)
    return uri


class API(InheritableCfgItem):
    """ Representation of a single API, overrides InheritableCfgItem. """
    STRICT = False
    DEFAULT_PARAMS = {
        APIKeysConstant.host: u'',
        APIKeysConstant.endpoints: [u'default_root'],
        APIKeysConstant.params: None
    }

    _HOSTS = None

    @clear_class_cached_results
    def invalidate(self):
        """ Call to invalidate API memory caches """
        pass

    def __getitem__(self, item):

        """ Extends InheritableCfgItem.__getitem__ to explode default params.

        Will get the API configuration as InheritableCfgItem.__getitem__ but will update
        the following:
            --> host:       Validate host config exists and retrieve the Host object from self.HOSTS.
            --> endpoints:  For each listed endpoint, validate endpoint config exists and retrieve
                            the Endpoint object from self.ENDPOINTS.
        Note: if host or any endpoints are invalid a KeyError will be raised.

        """

        item_value = super(API, self).__getitem__(item)

        if self._HOSTS is None:
            API._HOSTS = Hosts()

        # Attempt to explode Host
        if item == APIKeysConstant.host:
            try:
                return self._HOSTS[item_value]

            except LookupError:
                raise KeyError(u'No Host configuration exists for {host}! '
                               u'Please check your configuration!'.format(host=item_value))

        # Attempt to explode Endpoints
        if item == APIKeysConstant.endpoints:
            return self._get_endpoints_obj(allowed_endpoints=item_value,
                                           host=self.host)

        return item_value

    @class_cache_result
    def _get_endpoints_obj(self,
                           **params):
        return Endpoints(**params)

    def match_url(self,
                  url):

        """ Work out whether the url captured is from this endpoint.

        :param url:     (string)    Full URL to determine the matches for.
        :return:        (list)      List of matched endpoints for the url.
                                    Each item in the list is a tuple of the form:
                                        (API Family, API Name, Endpoint Name)
        """

        best_match = -1
        matched_endpoints = []

        for endpoint_name, endpoint in iter(self.endpoints.items()):
            matched_len = endpoint.match_url(url)

            if matched_len > -1:
                match_ref = (self.family, self.key, endpoint_name)

                if matched_len > best_match:
                    # Better than our best match so restart the list
                    matched_endpoints = [match_ref]
                    best_match = matched_len

                elif matched_len == best_match and match_ref not in matched_endpoints:
                    # Same as best match to append to list
                    matched_endpoints.append(match_ref)

        return matched_endpoints, best_match


class APIS(CfgItems):

    """ API configuration.

    Get environments object:
    >>> apis = APIS()

    Get A list of available APIs:
    >>> list(apis)
    ['example_api', 'example_api_2']

    """

    def __init__(self):
        super(APIS, self).__init__(cfg_fn=RegisterAPIConfig().apis,
                                   cfg_root=API_CONFIG,
                                   key_name=DefaultInheritableConstant.name,
                                   item_class=API)

    @clear_class_cached_results
    def invalidate(self):
        """ Call to invalidate APIS memory caches """
        for api in self:
            self[api].invalidate()

    def get_api_family(self,
                       family=None):

        """ Get and return a list of APIs belonging to an API family.

        :param family:  (string) The API family to get a list of APIs for.
                        default=None (the default family)
        :return:        (list)   List of API names for this family.
        """

        return [api_name for api_name, api in iteritems(self) if api.family == family]

    @class_cache_result
    def get_endpoint_for_request(self,
                                 uri):

        """ Determine and return the API / Endpoint config for a URL.

        :param uri:     (string)    Full URL to determine the config for.
        :return:        (tuple)     Match tuple values: (API Family, API Name, Endpoint Name)

        Examples:
        ---------
        Work out the Env / API configuration for a request:
        >>> APIS().get_endpoint_for_request(u'http://api.example.com/1.1/sometest')
        'example_api'

        """

        uri = add_default_port_to_uri(uri)

        matches = []
        groups = 0
        for api_name, api in self.items():
            for endpoint_name, endpoint in api.endpoints.items():
                # The endpoint serves a regular expression to match against the
                # url.  More than one endpoint can match, so we check the number
                # of matched groups. A higher number of groups means a match
                # against a more complex expression.
                # Assume that the more complex match is the better match,
                match = endpoint.url_regex.match(uri)
                if match:
                    if len(match.groups()) > groups:
                        groups = len(match.groups())
                        matches = []
                    if len(match.groups()) >= groups:
                        matches.append((api.family,
                                        api_name,
                                        endpoint_name))
        if len(matches) == 1:
            return matches[0]

        if len(matches) == 0:
            raise LookupError(u'No Endpoint match for: {uri}'.format(uri=uri))

        raise LookupError(u'Check your config...\n'
                          u'    Multiple matching Endpoints for: {uri}\n'
                          u'    This may mean the specific endpoint for this request is not defined.\n'
                          u'    Matches: {matches}\n'
                          .format(matches='\n             '.join([str(match) for match in matches]),
                                  uri=uri))
