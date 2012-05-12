MailSnake
=========

A Python wrapper for MailChimp's The API, STS API, and Export API.

Usage
-----

	>>> from mailsnake import MailSnake
	>>> mcapi = MailSnake('YOUR MAILCHIMP API KEY')
	>>> mcapi.ping()
	'"Everything\'s Chimpy!"'

The default API is MCAPI, but STS or Export can be used by supplying an api argument set to 'sts' or 'export' respectively. Here's an example:

	>>> mcsts = MailSnake('YOUR MAILCHIMP API KEY', api='sts')
	>>> mcsts.GetSendQuota()
    {'Max24HourSend': '10000.0', 'SentLast24Hours': '0.0', 'MaxSendRate': '5.0'}

Note
----

API parameters must be passed by name. For example:

	>>> mcapi.listMemberInfo(id='YOUR LIST ID', email_address='name@email.com')

API Documentation
-----------------

Note that in order to use the STS API you first need to enable the Amazon Simple Email Service [integration](https://us4.admin.mailchimp.com/account/integrations/ "MailChimp Integrations") in MailChimp.

[MailChimp API v1.3 documentation](http://apidocs.mailchimp.com/api/1.3/ "MCAPI v1.3")

[MailChimp STS API v1.0 documentation](http://apidocs.mailchimp.com/sts/1.0/ "STS API v1.0")

[MailChimp Export API v1.0 documentation](http://apidocs.mailchimp.com/export/1.0/ "Export API v1.0")

