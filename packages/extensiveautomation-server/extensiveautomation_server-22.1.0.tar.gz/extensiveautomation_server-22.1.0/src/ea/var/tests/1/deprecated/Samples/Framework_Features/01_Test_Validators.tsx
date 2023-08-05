<?xml version="1.0" encoding="utf-8" ?>
<file>
<properties><parameters /><probes><probe><active>False</active><args /><name>probe01</name><type>default</type></probe></probes><agents><agent><description /><type /><name>AGENT</name><value>agent-socket01</value></agent></agents><descriptions><description><value>tester</value><key>author</key></description><description><value>09/04/2012</value><key>creation date</key></description><description><value>Just a basic sample.</value><key>summary</key></description><description><value>None.</value><key>prerequisites</key></description><description><value><comments /></value><key>comments</key></description><description><value>myplugins</value><key>libraries</key></description><description><value>myplugins</value><key>adapters</key></description><description><value>Writing</value><key>state</key></description><description><value>REQ_01</value><key>requirement</key></description></descriptions><inputs-parameters><parameter><description /><type>bool</type><name>DEBUG</name><value>False</value><scope>local</scope></parameter><parameter><description /><type>float</type><name>TIMEOUT</name><value>1.0</value><scope>local</scope></parameter></inputs-parameters><outputs-parameters><parameter><description /><type>float</type><name>TIMEOUT</name><value>1.0</value><scope>local</scope></parameter></outputs-parameters></properties>
<testdefinition><![CDATA[		
class TESTCASE_STRING_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		validator = TestValidators.String()
		for i in xrange(10):
			randStr = validator.getRandom(length=12, withLetterLowerCase=True, withLetterUpperCase=True, withPunctuation=True,
						withDigits=True, withWhitespace=True, withHexdigits=False)
			self.info(txt=randStr, bold=False)	
		
		nb = validator.containsDigits(strVal=randStr)
		self.info( str(nb) )
		
		self.step1.setPassed(actual="success")
		
class TESTCASE_STRING_02(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		validator = TestValidators.String()
		for i in xrange(10):
			randStr = validator.getRandom(length=12, withLetterLowerCase=False, withLetterUpperCase=False, withPunctuation=False,
						withDigits=False, withWhitespace=False, withHexdigits=False)
			self.info(txt=randStr, bold=False)	
		
		nb = validator.containsDigits(strVal=randStr)
		self.info( str(nb) )
		
		self.step1.setPassed(actual="success")
		
class TESTCASE_FLOAT_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		validator = TestValidators.Float()
		for i in xrange(10):
			randFloat = validator.getRandom(fmin=5.2, fmax=25.8)
			self.info(txt=randFloat, bold=False)	
		
		floatValid = validator.isValid(n="fds")
		self.info( str(floatValid) )
		
		self.step1.setPassed(actual="success")

class TESTCASE_INTEGER_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		validator = TestValidators.Integer()
		for i in xrange(10):
			randInt = validator.getRandom(imin=10, imax=25)
			self.info(txt=randInt, bold=False)	
		
		intValid = validator.isValid(n="fds")
		self.info( str(intValid) )
		
		self.step1.setPassed(actual="success")

class TESTCASE_MAC_ADDRESS_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		validator = TestValidators.MacAddress(separator=":")

		mac = '01:11:22:33:44:FF'
		self.info( mac )
		ret = validator.isValid(mac=mac)
		if ret: self.info( 'this mac is valid' )
		else: 
			self.error( 'this mac is invalid' )
			self.setFailed()
		
		self.step1.setPassed(actual="success")

class TESTCASE_MAC_ADDRESS_INVALID_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		validator = TestValidators.MacAddress(separator=":")

		mac = '01:11:22:33:44:FFF'
		self.info( mac )
		ret = validator.isValid(mac=mac)
		if ret:
			self.error( 'this mac is valid' )
			self.setFailed()
		else: 
			self.info( 'this mac is invalid' )
		
		mac = '11:22:33:44'
		self.info( mac )
		ret = validator.isValid(mac=mac)
		if ret: 
			self.error( 'this mac is valid' )
			self.setFailed()
		else: 
			self.info( 'this mac is invalid' )
		
		self.step1.setPassed(actual="success")


class TESTCASE_MAC_ADDRESS_BROADCAST_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		validator = TestValidators.MacAddress(separator="-")
		
		self.info( validator.getBroadcast() ) 
		self.step1.setPassed(actual="success")

class TESTCASE_MAC_ADDRESS_RANDOM_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		validator = TestValidators.MacAddress(separator="-")
		
		for i in xrange(100):
			self.info( validator.getRandom() ) 
		self.step1.setPassed(actual="success")

class TESTCASE_IPV4_ADDRESS_BROADCAST_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		validator = TestValidators.IPv4Address(separator=".")
		
		self.info( validator.getBroadcast() ) 
		self.step1.setPassed(actual="success")

class TESTCASE_IPV4_ADDRESS_LOCALHOST_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		validator = TestValidators.IPv4Address(separator=".")
		
		self.info( validator.getLocalhost() ) 
		self.step1.setPassed(actual="success")
		
class TESTCASE_IPV4_ADDRESS_NULL_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		validator = TestValidators.IPv4Address(separator=".")

		self.info( validator.getNull() ) 
		self.step1.setPassed(actual="success")
		
class TESTCASE_IPV4_ADDRESS_RANDOM_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		validator = TestValidators.IPv4Address(separator=".")
		
		for i in xrange(100):
			self.info( validator.getRandom() ) 
		self.step1.setPassed(actual="success")

class TESTCASE_IPV4_ADDRESS_VALID_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		validator = TestValidators.IPv4Address(separator=".")

		ip = '192.168.1.1'
		self.info(ip )
		ret = validator.isValid(ip=ip)
		if ret: 
			self.info( 'this ip is valid' )
		else:
			self.setFailed()
			self.error( 'this ip is invalid' )

		self.step1.setPassed(actual="success")

class TESTCASE_IPV4_ADDRESS_INVALID_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		validator = TestValidators.IPv4Address(separator=".")
		
		ip = '192.168.1.1999'
		self.info(ip )
		ret = validator.isValid(ip=ip)
		if ret: 
			self.error( 'this ip is valid' )
			self.setFailed()
		else: 
			self.info( 'this ip is invalid' )
		
		ip = '192.168.1'
		self.info( ip )
		ret = validator.isValid(ip=ip)
		if ret: 
			self.error( 'this ip is valid' )
			self.setFailed()
		else: 
			self.info( 'this ip is invalid' )
		
		self.step1.setPassed(actual="success")
		
class TESTCASE_EMAIL_VALID_01(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")				
	def prepare(self):

		# adapters 
		self.VAL_EMAIL = TestValidators.Email()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		email = 'toto@tt.com'
		self.info( 'email: %s' % email)
		if self.VAL_EMAIL.isValid(email=email):
			self.step1.setPassed(actual="success")
		else:
			self.step1.setFailed(actual="invalid")
			
class TESTCASE_EMAIL_INVALID_01(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):
		# adapters 
		self.VAL_EMAIL = TestValidators.Email()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		email = '.toto@tt.com'
		self.info( 'email: %s' % email)
		if self.VAL_EMAIL.isValid(email=email):
			self.step1.setFailed(actual="invalid")
		else:
			self.step1.setPassed(actual="success")
class TESTCASE_EMAIL_INVALID_02(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):

		# adapters 
		self.VAL_EMAIL = TestValidators.Email()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		email = 't@oto@tt.com'
		self.info( 'email: %s' % email)
		if self.VAL_EMAIL.isValid(email=email):
			self.step1.setFailed(actual="invalid")
		else:
			self.step1.setPassed(actual="success")			
			
class TESTCASE_FTPURL_VALID_01(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):

		# adapters 
		self.VAL_FTPURL = TestValidators.FtpUrl()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		ftpurl = 'ftp://192.168.1.1'
		self.info( 'ftp url: %s' % ftpurl)
		if self.VAL_FTPURL.isValid(url=ftpurl):
			self.step1.setPassed(actual="success")
		else:
			self.step1.setFailed(actual="invalid")

			
class TESTCASE_FTPURL_INVALID_01(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):

		# adapters 
		self.VAL_FTPURL = TestValidators.FtpUrl()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		ftpurl = 'ftp://192.168.1.1aaa'
		self.info( 'ftp url: %s' % ftpurl)
		if self.VAL_FTPURL.isValid(url=ftpurl):
			self.step1.setFailed(actual="invalid")
		else:
			self.step1.setPassed(actual="success")

class TESTCASE_HTTPURL_VALID_01(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):

		# adapters 
		self.VAL_HTTPURL = TestValidators.HttpUrl()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		httpurl = 'http://192.168.1.1'
		self.info( 'http url: %s' % httpurl)
		if self.VAL_HTTPURL.isValid(url=httpurl):
			self.step1.setPassed(actual="success")
		else:
			self.step1.setFailed(actual="invalid")

class TESTCASE_HTTPURL_VALID_02(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):

		# adapters 
		self.VAL_HTTPURL = TestValidators.HttpUrl()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		httpurl = 'https://www.google.fr/imghp?hl=en&tab=wi&ei=5FXKUsmBNIab0AWy8oHoCQ&ved=0CAQQqi4oAg'
		self.info( 'http url: %s' % httpurl)
		if self.VAL_HTTPURL.isValid(url=httpurl, https=True):
			self.step1.setPassed(actual="success")
		else:
			self.step1.setFailed(actual="invalid")

class TESTCASE_HTTPURL_INVALID_01(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):

		# adapters 
		self.VAL_HTTPURL = TestValidators.HttpUrl()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		httpurl = 'http://aaa192.168.1.1'
		self.info( 'http url: %s' % httpurl)
		if self.VAL_HTTPURL.isValid(url=httpurl):
			self.step1.setFailed(actual="invalid")
		else:
			self.step1.setPassed(actual="success")

class TESTCASE_HTTPURL_INVALID_02(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):

		# adapters 
		self.VAL_HTTPURL = TestValidators.HttpUrl()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		httpurl = 'https:/sqdsqdsq/www.google.fr/imghp?hl=en&tab=wi&ei=5FXKUsmBNIab0AWy8oHoCQ&ved=0CAQQqi4oAg'
		self.info( 'http url: %s' % httpurl)
		if self.VAL_HTTPURL.isValid(url=httpurl):
			self.step1.setFailed(actual="invalid")
		else:
			self.step1.setPassed(actual="success")

class TESTCASE_URI_VALID_01(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):

		# adapters 
		self.VAL_URI = TestValidators.Uri()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		uri = 'http://192.168.1.1'
		self.info( 'uri: %s' % uri)
		if self.VAL_URI.isValid(uri=uri):
			self.step1.setPassed(actual="success")
		else:
			self.step1.setFailed(actual="invalid")

class TESTCASE_URI_VALID_02(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):

		# adapters 
		self.VAL_URI = TestValidators.Uri()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		uri = 'https://www.google.fr/imghp?hl=en&tab=wi&ei=5FXKUsmBNIab0AWy8oHoCQ&ved=0CAQQqi4oAg'
		self.info( 'uri: %s' % uri)
		if self.VAL_URI.isValid(uri=uri):
			self.step1.setPassed(actual="success")
		else:
			self.step1.setFailed(actual="invalid")

class TESTCASE_URI_INVALID_01(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):

		# adapters 
		self.VAL_URI = TestValidators.Uri()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		uri = '.htdsqdsqtp://aaa192.168.1.1'
		self.info( 'uri: %s' % uri)
		if self.VAL_URI.isValid(uri=uri):
			self.step1.setFailed(actual="valid but should not")
		else:
			self.step1.setPassed(actual="success")

class TESTCASE_URI_INVALID_02(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):

		# adapters 
		self.VAL_URI = TestValidators.Uri()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		uri = '-https:/sqdsqdsq/www.google.fr/imghp?hl=en&tab=wi&ei=5FXKUsmBNIab0AWy8oHoCQ&ved=0CAQQqi4oAg'
		self.info( 'uri: %s' % uri)
		if self.VAL_URI.isValid(uri=uri):
			self.step1.setFailed(actual="valid but should not")
		else:
			self.step1.setPassed(actual="success")
			
class TESTCASE_IPV6_VALID_01(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):

		# adapters 
		self.VAL_IPV6 = TestValidators.IPv6Address()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		ip = '::1'
		self.info( 'ip: %s' % ip)
		if self.VAL_IPV6.isValid(ip=ip):
			self.step1.setPassed(actual="success")
		else:
			self.step1.setFailed(actual="invalid")
class TESTCASE_IPV6_VALID_02(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):

		# adapters 
		self.VAL_IPV6 = TestValidators.IPv6Address()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		ip = 'FFFF:AAAA::221:3:11:3'
		self.info( 'ip: %s' % ip)
		if self.VAL_IPV6.isValid(ip=ip):
			self.step1.setPassed(actual="success")
		else:
			self.step1.setFailed(actual="invalid")
class TESTCASE_IPV6_INVALID_01(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):

		# adapters 
		self.VAL_IPV6 = TestValidators.IPv6Address()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		ip = 'FFFF:AAAA:;:221:3:11:3'
		self.info( 'ip: %s' % ip)
		if self.VAL_IPV6.isValid(ip=ip):
				self.step1.setFailed(actual="invalid")
		else:
			self.step1.setPassed(actual="success")

class TESTCASE_HOSTNAME_VALID_01(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):

		# adapters 
		self.VAL_HOST = TestValidators.Hostname()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		hostname = 'www.google.fr'
		self.info( 'hostname: %s' % hostname)
		if self.VAL_HOST.isValid(hostname=hostname):
			self.step1.setPassed(actual="success")
		else:
			self.step1.setFailed(actual="invalid")

class TESTCASE_HOSTNAME_INVALID_01(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample")
	def prepare(self):

		# adapters 
		self.VAL_HOST = TestValidators.Hostname()

	def cleanup(self, aborted):
		pass
	def definition(self):
		# starting initial step
		self.step1.start()
		hostname = ';www.google.fr'
		self.info( 'hostname: %s' % hostname)
		if self.VAL_HOST.isValid(hostname=hostname):
			self.step1.setFailed(actual="invalid")
		else:
			self.step1.setPassed(actual="success")
			]]></testdefinition>
<testexecution><![CDATA[
TESTCASE_STRING_01(suffix=None).execute()
TESTCASE_STRING_02(suffix=None).execute()
TESTCASE_FLOAT_01(suffix=None).execute()
TESTCASE_INTEGER_01(suffix=None).execute()

TESTCASE_MAC_ADDRESS_01(suffix=None).execute()
TESTCASE_MAC_ADDRESS_INVALID_01(suffix=None).execute()
TESTCASE_MAC_ADDRESS_BROADCAST_01(suffix=None).execute()
TESTCASE_MAC_ADDRESS_RANDOM_01(suffix=None).execute()

TESTCASE_IPV4_ADDRESS_BROADCAST_01(suffix=None).execute()
TESTCASE_IPV4_ADDRESS_LOCALHOST_01(suffix=None).execute()
TESTCASE_IPV4_ADDRESS_NULL_01(suffix=None).execute()
TESTCASE_IPV4_ADDRESS_RANDOM_01(suffix=None).execute()
TESTCASE_IPV4_ADDRESS_VALID_01(suffix=None).execute()
TESTCASE_IPV4_ADDRESS_INVALID_01(suffix=None).execute()

TESTCASE_EMAIL_VALID_01(suffix=None).execute()
TESTCASE_EMAIL_INVALID_01(suffix=None).execute()
TESTCASE_EMAIL_INVALID_02(suffix=None).execute()

TESTCASE_FTPURL_VALID_01(suffix=None).execute()
TESTCASE_FTPURL_INVALID_01(suffix=None).execute()

TESTCASE_HTTPURL_VALID_01(suffix=None).execute()
TESTCASE_HTTPURL_VALID_02(suffix=None).execute()
TESTCASE_HTTPURL_INVALID_01(suffix=None).execute()
TESTCASE_HTTPURL_INVALID_02(suffix=None).execute()

TESTCASE_URI_VALID_01(suffix=None).execute()
TESTCASE_URI_VALID_02(suffix=None).execute()
TESTCASE_URI_INVALID_01(suffix=None).execute()
TESTCASE_URI_INVALID_02(suffix=None).execute()

TESTCASE_IPV6_VALID_01(suffix=None).execute()
TESTCASE_IPV6_VALID_02(suffix=None).execute()
TESTCASE_IPV6_INVALID_01(suffix=None).execute()

TESTCASE_HOSTNAME_VALID_01(suffix=None).execute()
TESTCASE_HOSTNAME_INVALID_01(suffix=None).execute()]]></testexecution>
<testdevelopment>1386106104.74</testdevelopment>
</file>