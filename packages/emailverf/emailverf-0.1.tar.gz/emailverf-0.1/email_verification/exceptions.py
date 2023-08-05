class InvalidSyntaxException(Exception):
	def __init__(self):
		pass

	def __str__(self):
		return 'Invalid syntax: the syntax is not in accordance with RFC guidelines. Check guidelines here: https://tools.ietf.org/html/rfc2822'


class InvalidDomainError(Exception):
	def __init__(self):
		pass

	def __str__(self):
		return 'Invalid domain: the domain could not be verified.'
		