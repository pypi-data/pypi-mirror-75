import re
import socket
import tldextract
from exceptions import InvalidSyntaxException, InvalidDomainError
import urllib.request
import smtplib
import dns.resolver


JUNK_EMAIL_LOCAL_1 = 'j342jh342hj342hj342hj342h342b2h4bjh24b3234j32'
JUNK_EMAIL_LOCAL_2 = 'gfx3gf4x46g7x5yfusx7fx7f6x98f8b7xz9f7z69dz76d'
JUNK_EMAILS = [JUNK_EMAIL_LOCAL_1, JUNK_EMAIL_LOCAL_2]


class Email_verification:
	def __init__(self):
		pass

	@classmethod
	def check_syntax(cls, email_address):
		"""
		Does regex based syntax check of email address based on RFC guidelines
		"""
		regex = r"^([!#-\'*+\/-9=?A-Z^-~\\\\-]{1,64}(\.[!#-\'*+\/-9=?A-Z^-~\\\\-]{1,64})*|\"([\]!#-[^-~\ \t\@\\\\]|(\\[\t\ -~]))+\")@([0-9A-Z]([0-9A-Z-]{0,61}[0-9A-Za-z])?(\.[0-9A-Z]([0-9A-Z-]{0,61}[0-9A-Za-z])?))+$"

		if re.match(regex, email_address, re.IGNORECASE):
			return True
		else:
			return False

	@staticmethod
	def get_domain(email_address):
		"""
		If syntax is correct, returns the domain name of the email address
		"""
		if Email_verification.check_syntax(email_address) == True:
			domain = (email_address.split('@')[-1]).lower()
		else:
			raise InvalidSyntaxException

		sub_domain_possibility = None
		if domain.count('.') > 1:
			sub_domain_possibility = True

		domain, domain_valid, business_name, domain_type, sub_domain_possibility = Email_verification.validate_domain(domain=domain, sub_domain_possibility=sub_domain_possibility)
		return domain, domain_valid, business_name, domain_type, sub_domain_possibility

	@classmethod
	def validate_domain(cls, domain, domain_valid=None, business_name=None, domain_type=None, sub_domain_possibility=None):
		"""
		Expects the domains_master dictionary
		Processes and evaluates domain validity and business name for the domain names with None values
		"""
		# establishing if the domain exists
		if domain_valid is None:
			try:
				socket.gethostbyname(domain)
				domain_valid = True

			except socket.gaierror:
				domain_valid = False
				business_name = False
				domain_type = False
				# sub_domain = 'Invalid'
				raise InvalidDomainError
				
		# getting the (probable) business name of the valid domain names
		if business_name is None:
			business_name = Email_verification.get_title(domain, domain_valid)

		if domain_type is None:
			domain_type = Email_verification.check_domain_type(domain, domain_valid)

		if domain_valid == False and business_name == False and domain_type == False and sub_domain_possibility == True:
			if domain.count('.') == 2:
				url = 'https://www.' + domain
				tldextract_url = tldextract.extract(url)
				sub_domain_new = tldextract_url[1] + '.' + tldextract_url[2]
				
				result_sub_domain = cls.validate_domain(sub_domain_new, None, None, None, None)
				if result_sub_domain[1] == True:
					return domain, result_sub_domain[1], result_sub_domain[2], result_sub_domain[3], sub_domain_new
				else:
					raise InvalidDomainError
		else:
			return domain, domain_valid, business_name, domain_type, sub_domain_possibility

	@classmethod
	def get_title(cls, domain, valid, tries=1):
		"""
		Gets the title from the HTML page that the domain name directs to
		This method tries these combinations- 
		https://www.domain.com
		http://www.domain.com
		www.domain.com
		"""
		# creating opener to act like a actual web browser ping
		opener = urllib.request.build_opener()
		opener.addheaders=[('User-Agent',
							'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)' \
							'Chrome/36.0.1941.0 Safari/537.36')]
		urllib.request.install_opener(opener)

		try:
			url = 'https://www.' + domain
			
			with urllib.request.urlopen(url, timeout=60) as conn:
				req = conn.read()
		except:
			try:
				url = 'http://www.' + domain
				
				with urllib.request.urlopen(url, timeout=60) as conn:
					req = conn.read()
			except:
				try:
					url = 'www.' + domain
				
					with urllib.request.urlopen(url, timeout=60) as conn:
						req = conn.read()
				except Exception as exc:
					req = ('ERR', exc)

		if type(req) is not tuple:
			try:
				req = req.decode('utf-8').lower()
				title1 = int(req.find('<title')) + 6
				title1 = int(req.find('>', title1)) + 1
				title2 = int(req.find('</title>'))
				title = req[title1:title2]
			except UnicodeDecodeError:
				return 'Wrong encoding'
		else:
			if tries < 5:
				title = Email_verification.get_title(domain, valid, tries+1)
			else:	
				title = str(req[1])

		# handling some weird characters that utf-8 did not handle
		# title = title.replace('\n', '').replace('\r', '').replace('\t', '').replace('&#8211;', '-').strip().title()
		handle_texts = {'\n', '\r', '\t', '&#8211;'}
		for text in handle_texts:
			title = title.replace(text, '')
		title = title.strip().title()

		if title == '' or title.lower() == 'home' or ('doctype' in title.lower() and 'html' in title.lower()):
			return 'No title found'
		else:
			return title

	@classmethod
	def check_domain_type(cls, domain, domain_valid):
		"""
		Tries to verify 2 junk email addresses on a domain to decide if that domain
		might be catch all or bouncing off all emails sent to it
		"""

		results = []
		if domain_valid == 'Valid':
			for junk_email in JUNK_EMAILS:
				try:
					# domainName = email_address.split("@")[1]
					records = dns.resolver.query(domain, 'MX')
					mxRecord = records[0].exchange
					mxRecord = str(mxRecord)

					host = socket.gethostname()
					server = smtplib.SMTP()
					server.set_debuglevel(0)

					server.connect(mxRecord)
					server.helo(host)
					server.mail('me@domaincc.com')
					email_address = junk_email + '@' + domain
					# print(email_address)
					code, message = server.rcpt(str(email_address))
					results.append((code, message))
					server.quit()

				except Exception as e:
					code = "ERR"
					message = e
					results.append((code, message))

			if str(results[0][0]) == '250' and str(results[1][0]) == '250':
				return 'Catch all'
			
			else:
				return 'Cannot determine'

		else:
			return 'Invalid'

	@classmethod
	def verifiy_email(cls, email_address):
		domain, domain_valid, business_name, domain_type, sub_domain_possibility = \
			Email_verification.get_domain(email_address)
		
		if domain_type.lower() == 'catch all':
			code = '250-C'
			message = 'Catch all'

		elif domain_valid == True:
			try:
				records = dns.resolver.query(domain, 'MX')
				mxRecord = records[0].exchange
				mxRecord = str(mxRecord)

				host = socket.gethostname()
				server = smtplib.SMTP()
				server.set_debuglevel(0)

				server.connect(mxRecord)
				server.helo(host)
				server.mail('me@domain.com')
				code, message = server.rcpt(str(email_address))
				server.quit()

			except Exception as e:
				code = "ERR"
				message = e

		else:
			code = '550'
			message = 'Invalid email address'

		if str(code) == '250':
			if domain_type.lower() != 'catch all':
				domain_type = 'Valid'

		return code, message, domain, domain_valid, business_name, domain_type, sub_domain_possibility
