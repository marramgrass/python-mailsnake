import copy
import json
import requests
import urllib2

class MailSnake(object):
    def __init__(self,
                 apikey = '',
                 extra_params = {},
                 api = 'api',
                 api_section = ''):
        """
            Cache API key and address.
        """
        self.apikey = apikey
        self.api = api

        self.default_params = {'apikey':apikey}
        if api == 'mandrill':
            self.default_params = {'key':apikey}
            if api_section != '':
                self.api_section = api_section
            else:
                # Mandrill divides the api into different sections
                for x in ['users', 'messages', 'tags', 'rejects',
                          'senders', 'urls', 'templates', 'webhooks']:
                    setattr(self, x, MailSnake(apikey, extra_params,
                                              api, x))
        self.default_params.update(extra_params)

        dc = 'us1'
        if '-' in self.apikey:
            dc = self.apikey.split('-')[1]
        api_info = {
            'api':(dc,'.api.','mailchimp','1.3/?method='),
            'sts':(dc,'.sts.','mailchimp','1.0/'),
            'export':(dc,'.api.','mailchimp','export/1.0/'),
            'mandrill':('','','mandrillapp','api/1.0/'),
        }
        self.api_url = 'https://%s%s%s.com/%s' % api_info[api]

    def call(self, method, params = {}):
        url = self.api_url
        if self.api == 'mandrill':
            url += (self.api_section + '/' + method + '.json')
        elif self.api == 'sts':
            url += (method + '.json/')
        else:
            url += method
        
        all_params = self.default_params.copy()
        all_params.update(params)
        
        if self.api == 'api' or self.api == 'mandrill':
            data = json.dumps(all_params)
            if self.api == 'api':
                data = urllib2.quote(data)
            headers = {'content-type':'application/json'}
        else:
            data = all_params
            headers = {'content-type':
                      'application/x-www-form-urlencoded'}
        
        if self.api == 'export':
            request = requests.post(url, params=data, headers=headers)
            return [json.loads(i) for i in \
                    request.text.split('\n')[0:-1]]
        else:
            request = requests.post(url, data=data, headers=headers)
            return json.loads(request.text)

    def __getattr__(self, method_name):
        def get(self, *args, **kwargs):
            params = dict((i,j) for (i,j) in enumerate(args))
            params.update(kwargs)
            # Some mandrill functions use - in the name
            return self.call(method_name.replace('_', '-'), params)

        return get.__get__(self)
