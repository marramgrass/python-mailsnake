MailSnake
=========

A Python wrapper for MailChimp's The API, STS API, Export API, and the
new Mandrill API. It requires the [python requests library](http://docs.python-requests.org/en/latest/index.html "Requests Documentation").

Usage
-----

	>>> from mailsnake import MailSnake
	>>> mcapi = MailSnake('YOUR MAILCHIMP API KEY')
	>>> mcapi.ping()
	u"Everything's Chimpy!"

The default API is MCAPI, but STS, Export, and Mandrill can be used by
supplying an api argument set to 'sts', 'export', or 'mandrill'
respectively. Here's an example:

	>>> mcsts = MailSnake('YOUR MAILCHIMP API KEY', api='sts')
	>>> mcsts.GetSendQuota()
    {'Max24HourSend': '10000.0', 'SentLast24Hours': '0.0', 'MaxSendRate': '5.0'}

Since the Mandrill API is divided into sections, one must take that into
account when using it. Here's an example:

	>>> mapi = MailSnake('YOUR MANDRILL API KEY', api='mandrill')
	>>> mapi.users.ping()
    u'PONG!'
    
or:

	>>> mapi\_users = MailSnake('YOUR MANDRILL API KEY', api='mandrill', api\_section='users')
	>>> mapi\_users.ping()
    u'PONG!'

Some Mandrill functions have a dash(-) in the name. Since Python
function names can't have dashes in them, user underscores(\_) instead:

	>>> mapi = MailSnake('YOUR MANDRILL API KEY', api='mandrill')
	>>> mapi.messages.send(message={'html':'email html', 'subject':'email subject', 'from\_email':'from@example.com', 'from\_name':'From Name', 'to':\[{'email':'to@example.com', 'name':'To Name'}\]})
    u'PONG!'

Note
----

API parameters must be passed by name. For example:

	>>> mcapi.listMemberInfo(id='YOUR LIST ID', email\_address='name@email.com')

API Documentation
-----------------

Note that in order to use the STS API or Mandrill you first need to
enable the Amazon Simple Email Service or the Mandrill
[integration](https://us4.admin.mailchimp.com/account/integrations/ "MailChimp Integrations")
in MailChimp.

[MailChimp API v1.3 documentation](http://apidocs.mailchimp.com/api/1.3/ "MCAPI v1.3 Documentation")

[MailChimp STS API v1.0 documentation](http://apidocs.mailchimp.com/sts/1.0/ "STS API v1.0 Documentation")

[MailChimp Export API v1.0 documentation](http://apidocs.mailchimp.com/export/1.0/ "Export API v1.0 Documentation")

