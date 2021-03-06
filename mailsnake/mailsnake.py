""" MailSnake """

import urllib
import urllib2

try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        try:
            from django.utils import simplejson as json
        except ImportError:
            raise ImportError('A json library is required to use ' + \
                             'this python library. Lol, yay for ' + \
                             'being verbose. ;)')

from .exceptions import *


class MailSnake(object):
    def __init__(self,
                 apikey='',
                 extra_params=None,
                 api='api',
                 api_section=''):
        """
            Cache API key and address.
        """
        self.apikey = apikey

        ACCEPTED_APIS = ('api', 'sts', 'export', 'mandrill')
        if not api in ACCEPTED_APIS:
            raise MailSnakeException('The API "%s" is not supported.') % api

        self.api = api

        self.default_params = {'apikey': apikey}
        extra_params = extra_params or {}
        if api == 'mandrill':
            self.default_params = {'key': apikey}
            if api_section != '':
                self.api_section = api_section
            else:
                # Mandrill divides the api into different sections
                for x in ['users', 'messages', 'tags', 'rejects',
                          'senders', 'urls', 'templates', 'webhooks']:
                    setattr(self, x, MailSnake(apikey, extra_params,
                                              api, x))
        self.default_params.update(extra_params)

        if '-' in self.apikey:
            self.dc = self.apikey.split('-')[1]
        api_info = {
            'api': (self.dc, '.api.', 'mailchimp', '1.3/?method='),
            'sts': (self.dc, '.sts.', 'mailchimp', '1.0/'),
            'export': (self.dc, '.api.', 'mailchimp', 'export/1.0/'),
            'mandrill': ('', '', 'mandrillapp', 'api/1.0/'),
        }
        self.api_url = 'https://%s%s%s.com/%s' % api_info[api]

    def __repr__(self):
        if self.api == 'api':
            api = 'API v3'
        elif self.api == 'sts':
            api = self.api.upper() + ' API'
        else:
            api = self.api.capitalize() + ' API'

        return u'<MailSnake %s: %s>' % (api, self.apikey)

    def call(self, method, params=None):
        url = self.api_url
        if self.api == 'mandrill':
            url += (self.api_section + '/' + method + '.json')
        elif self.api == 'sts':
            url += (method + '.json/')
        else:
            url += method

        params = params or {}
        params.update(self.default_params)

        if self.api == 'api' or self.api == 'mandrill':
            data = json.dumps(params)
            if self.api == 'api':
                data = urllib2.quote(data)
            headers = {'content-type': 'application/json'}
        else:
            data = params
            headers = {
                'content-type': 'application/x-www-form-urlencoded'
            }

        try:
            if self.api == 'export':
                req = urllib2.urlopen(url, data)
            else:
                req = urllib2.urlopen(url, data)
        except urllib2.HTTPError, e:
            raise HTTPRequestException(e.read())
        except urllib2.URLError, e:
            raise HTTPRequestException(e.reason)

        try:
            response_data = req.read()
            if self.api == 'export':
                rsp = [json.loads(i) for i in \
                      response_data.split('\n')[0:-1]]
            else:
                rsp = json.loads(response_data)
        except ValueError, e:
            raise ParseException(e.message)

        if not isinstance(rsp, (int, bool, basestring)) and \
                'error' in rsp and 'code' in rsp:
            try:
                Err = exception_for_code(rsp['code'])
            except KeyError:
                raise SystemException(rsp['error'])
            raise Err(rsp['error'])

        return rsp

    def __getattr__(self, method_name):
        def get(self, *args, **kwargs):
            params = dict((i, j) for (i, j) in enumerate(args))
            params.update(kwargs)
            # Some mandrill functions use - in the name
            return self.call(method_name.replace('_', '-'), params)

        return get.__get__(self)
