import urllib2

from urllib import quote

try:
    import simplejson as json
except ImportError:
    import json

class MailSnake(object):
    def __init__(self, apikey = '', extra_params = {}, api = 'api'):
        """
            Cache API key and address.
        """
        self.apikey = apikey
        self.api = api

        self.default_params = {'apikey':apikey}
        self.default_params.update(extra_params)

        dc = 'us1'
        if '-' in self.apikey:
            dc = self.apikey.split('-')[1]
        api_info = {
            'api':('api','1.3/?method='),
            'sts':('sts','1.0/'),
            'export':('api','export/1.0/')
        }
        self.api_url = 'https://%s.%s.mailchimp.com/%s' % \
                       ((dc,) + api_info[api])

    def call(self, method, params = {}):
        url = self.api_url + method
        all_params = self.default_params.copy()
        all_params.update(params)

        if self.api == 'api':
            post_data = urllib2.quote(json.dumps(all_params))
            headers = {'Content-Type':'application/json'}
        else:
            headers = {'Content-Type':'application/x-www-form-urlencoded'}
            post_data = http_build_query(all_params)
            if self.api == 'sts':
                url += '.json/'
            else:
                # Use GET for the Export API
                url += '?' + post_data
                post_data = ''
        request = urllib2.Request(url, post_data, headers)
        response = urllib2.urlopen(request)

        if self.api == 'export':
            return [json.loads(i) for i in response.readlines()]
        else:
            return json.loads(response.read())

    def __getattr__(self, method_name):

        def get(self, *args, **kwargs):
            params = dict((i,j) for (i,j) in enumerate(args))
            params.update(kwargs)
            return self.call(method_name, params)

        return get.__get__(self)

##################################################
# http://www.codigomanso.com/en/2010/04/http_build_query-para-python/
# By Pau Sanchez
# Mimics the behaviour of http_build_query PHP function
# This method can be useful for sending data to flash applications
##################################################
def http_build_query(params, topkey = ''): 
    if len(params) == 0:
        return ""

    result = ""
 
    # is a dictionary?
    if type (params) is dict:
        for key in params.keys():
            newkey = quote (key)
            if topkey != '':
              newkey = topkey + quote('[' + key + ']')
 
            if type(params[key]) is dict:
                result += http_build_query (params[key], newkey)

            elif type(params[key]) is list:
                i = 0
                for val in params[key]:
                    result += newkey + quote('[' + str(i) + ']') + \
                              "=" + quote(str(val)) + "&"
                    i = i + 1

            # boolean should have special treatment as well
            elif type(params[key]) is bool:
                result += newkey + "=" + quote(str(int(params[key]))) + "&"

            # assume string (integers and floats work well)
            else:
                result += newkey + "=" + quote(str(params[key])) + "&"

    # remove the last '&'
    if (result) and (topkey == '') and (result[-1] == '&'):
        result = result[:-1]

    return result
