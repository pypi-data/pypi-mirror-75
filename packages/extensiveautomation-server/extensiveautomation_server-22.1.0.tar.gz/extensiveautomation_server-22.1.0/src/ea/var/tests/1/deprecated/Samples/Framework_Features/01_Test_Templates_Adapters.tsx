<?xml version="1.0" encoding="utf-8" ?>
<file>
<properties><parameters /><probes><probe><active>False</active><args /><name>probe01</name></probe></probes><agents><agent><description /><type /><name>AGENT</name><value>agent-socket01</value></agent></agents><descriptions><description><value /><key>author</key></description><description><value /><key>creation date</key></description><description><value /><key>summary</key></description><description><value /><key>prerequisites</key></description><description><value><comments /></value><key>comments</key></description><description><value>myplugins</value><key>libraries</key></description><description><value>myplugins</value><key>adapters</key></description><description><value>Writing</value><key>state</key></description><description><value>REQ_01</value><key>requirement</key></description></descriptions><inputs-parameters><parameter><description /><type>bool</type><name>DEBUG</name><value>True</value><scope>local</scope></parameter><parameter><description /><type>str</type><name>TIMEOUT</name><value>1</value><scope>local</scope></parameter></inputs-parameters><outputs-parameters><parameter><description /><type>float</type><name>TIMEOUT</name><value>1.0</value><scope>local</scope></parameter></outputs-parameters></properties>
<testdefinition><![CDATA[
class TPL_TO_SUT_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		cp = SutAdapter.Adapter(parent=self,name="Test")
		# send message from tas to sut
		self.info("send fake tas message from to sut", bold=True)
		for i in xrange(5):
			# fake tas and raw payload
			tasTpl = TestTemplates.TemplateMessage()
			tasTpl.addRaw( 'test1' ) 
			layer_req = TestTemplates.TemplateLayer(name='request')
			layer_req.addKey(name='cmd', data='NOTIFY')
			layer_req.addKey(name='tid', data='%s' % i)
			layer_req.addKey(name='userid', data='0')
			layer_req.addRaw( 'test2' )
			self.info( layer_req )
			tasTpl.addLayer(layer=layer_req)
			
			layer_bod = TestTemplates.TemplateLayer(name='body')
			layer_bod.addKey(name='raw', data='ABCDEFGHIJKLMNOPQRSTUVWXYZ\nABCDEFGHIJKLMNOPQRSTUVWXYZ')
			tasTpl.addLayer(layer=layer_bod)
			
			summary = "NOTIFY %s 0" % i
			rawPayload = "NOTIFY %i 0\nABCDEFGHIJKLMNOPQRSTUVWXYZ" % i
			tasTpl.addRaw(raw=rawPayload)
			cp.logSentEvent(summary, tasTpl )
		# 
		self.step1.setPassed(actual="success")

class TPL_TO_SUT_02(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		cp = SutAdapter.Adapter(parent=self,name="Test")
		# send message from tas to sut
		self.info("send fake tas message from to sut", bold=True)
		for i in xrange(5):
			# fake tas and raw payload
			tasTpl = TestTemplates.TemplateMessage()
			
			layer_req = TestTemplates.TemplateLayer(name='request')
			layer_req.addKey(name='cmd', data='NOTIFY')
			layer_req.addKey(name='tid', data='%s' % i)
			layer_req.addKey(name='userid', data='0')
			
			layer_sub_req = TestTemplates.TemplateLayer(name='resume')
			layer_sub_req.addKey(name='test1', data='tata')
			layer_sub_req.addKey(name='test2', data='data')
			layer_req.addKey(name='more', data=layer_sub_req)
			
			tasTpl.addLayer(layer=layer_req)
			
			layer_bod = TestTemplates.TemplateLayer(name='body')
			layer_bod.addKey(name='raw', data='ABCDEFGHIJKLMNOPQRSTUVWXYZ\nABCDEFGHIJKLMNOPQRSTUVWXYZ')
			tasTpl.addLayer(layer=layer_bod)
			
			summary = "NOTIFY %s 0" % i
			rawPayload = "NOTIFY %i 0\nABCDEFGHIJKLMNOPQRSTUVWXYZ" % i
			tasTpl.addRaw(raw=rawPayload)
			cp.logSentEvent(summary, tasTpl )
	
		self.step1.setPassed(actual="success")

class TPL_FROM_SUT_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		cp = SutAdapter.Adapter(parent=self,name="Test")
		# receveid message from sut to tas
		self.info("receives fake message from sut from to tas", bold=True)
		for i in xrange(5):
			# simulate send data
			tasTpl = TestTemplates.TemplateMessage()
			
			layer_req = TestTemplates.TemplateLayer(name='request')
			layer_req.addKey(name='cmd', data='NOTIFY')
			layer_req.addKey(name='tid', data='%s' % i)
			layer_req.addKey(name='userid', data='0')
			
			layer_sub_req = TestTemplates.TemplateLayer(name='resume')
			layer_sub_req.addKey(name='test1', data='tata')
			layer_sub_req.addKey(name='test2', data='data')
			layer_req.addKey(name='more', data=layer_sub_req)
			
			tasTpl.addLayer(layer=layer_req)
			
			layer_bod = TestTemplates.TemplateLayer(name='body')
			layer_bod.addKey(name='raw', data='ABCDEFGHIJKLMNOPQRSTUVWXYZ\nABCDEFGHIJKLMNOPQRSTUVWXYZ')
			tasTpl.addLayer(layer=layer_bod)
			
			summary = "NOTIFY %s 0" % i
			rawPayload = "NOTIFY %i 0\nABCDEFGHIJKLMNOPQRSTUVWXYZ" % i
			tasTpl.addRaw(raw=rawPayload)
			cp.logSentEvent(summary, tasTpl )
			
			# simulate received data
			tasTpl2 = TestTemplates.TemplateMessage()
			
			layer_req = TestTemplates.TemplateLayer(name='response')
			layer_req.addKey(name='code', data='403')
			layer_req.addKey(name='tid', data='%s' % i)
			layer_req.addKey(name='phrase', data='FORBIDDEN')	
			tasTpl2.addLayer(layer=layer_req)
			
			layer_bod = TestTemplates.TemplateLayer(name='body')
			layer_bod.addKey(name='raw', data='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
			tasTpl2.addLayer(layer=layer_bod)
			
			summary = "403 %s FORBIDDEN" % i
			rawPayload = "403 %s FORBIDDEN\n0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" % i	
			tasTpl2.addRaw(raw=rawPayload)
			cp.logRecvEvent(summary, tasTpl2 )
		
		self.step1.setPassed(actual="success")

class TPL_MATCH_ANY_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		cp = SutAdapter.Adapter(parent=self,name="Test")
		# first simulate some fake messages
		self.info("1 - receives some fake messages from sut from to tas", bold=True)
		for i in xrange(5):
			# simulate send data
			tasTpl = TestTemplates.TemplateMessage()
			
			layer_req = TestTemplates.TemplateLayer(name='request')
			layer_req.addKey(name='cmd', data='NOTIFY')
			layer_req.addKey(name='tid', data='%s' % i)
			layer_req.addKey(name='userid', data='0')
			
			layer_sub_req = TestTemplates.TemplateLayer(name='resume')
			layer_sub_req.addKey(name='test1', data='tata')
			layer_sub_req.addKey(name='test2', data='data')
			layer_req.addKey(name='more', data=layer_sub_req)
			
			tasTpl.addLayer(layer=layer_req)
			
			layer_bod = TestTemplates.TemplateLayer(name='body')
			layer_bod.addKey(name='raw', data='ABCDEFGHIJKLMNOPQRSTUVWXYZ\nABCDEFGHIJKLMNOPQRSTUVWXYZ')
			tasTpl.addLayer(layer=layer_bod)
			
			summary = "NOTIFY %s 0" % i
			rawPayload = "NOTIFY %i 0\nABCDEFGHIJKLMNOPQRSTUVWXYZ" % i
			tasTpl.addRaw(raw=rawPayload)
			cp.logSentEvent(summary, tasTpl )
			
			# simulate received data
			tasTpl2 = TestTemplates.TemplateMessage()
			
			layer_req = TestTemplates.TemplateLayer(name='response')
			layer_req.addKey(name='code', data='403')
			layer_req.addKey(name='tid', data='%s' % i)
			layer_req.addKey(name='phrase', data='FORBIDDEN')	
			tasTpl2.addLayer(layer=layer_req)
			
			layer_bod = TestTemplates.TemplateLayer(name='body')
			layer_bod.addKey(name='raw', data='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
			tasTpl2.addLayer(layer=layer_bod)
			
			summary = "403 %s FORBIDDEN" % i
			rawPayload = "403 %s FORBIDDEN\n0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" % i	
			tasTpl2.addRaw(raw=rawPayload)
			cp.logRecvEvent(summary, tasTpl2 )

		# try to match one msg during the timeout interval
		self.info("- try to match one msg during the timeout interval", bold=True)
		tplExpected = TestTemplates.TemplateMessage()
		layerExpected = TestTemplates.TemplateLayer(name=TestOperators.Any())
		tplExpected.addLayer(layer=layerExpected)
		evt = cp.received( expected = tplExpected, timeout = input('TIMEOUT') )
		if evt is not None:
			self.info(evt)
			
		# try to match one msg during the timeout interval
		self.info("- try to match one msg during the timeout interval", bold=True)
		tplExpected = TestTemplates.TemplateMessage()
		layerExpected = TestTemplates.TemplateLayer(name='response')
		tplExpected.addLayer(layer=layerExpected)
		evt = cp.received( expected = tplExpected, timeout = input('TIMEOUT') )
		if evt is not None:
			self.info(evt)
			
		# try to match one msg during the timeout interval
		self.info("- try to match one msg during the timeout interval", bold=True)
		tplExpected = TestTemplates.TemplateMessage()
		evt = cp.received( expected = tplExpected, timeout = input('TIMEOUT') )
		if evt is not None:
			self.info(evt)

		# try to match one msg during the timeout interval
		self.info("- try to match one msg during the timeout interval", bold=True)
		tplExpected = TestTemplates.TemplateMessage()
		layerExpected = TestTemplates.TemplateLayer(name=TestOperators.Any())
		tplExpected.addLayer(layer=layerExpected)
		evt = cp.received( expected = tplExpected, timeout = input('TIMEOUT') )
		if evt is not None:
			self.info(evt)
			
		self.step1.setPassed(actual="success")

class TPL_MATCH_02(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		cp = SutAdapter.Adapter(parent=self,name="Test", debug=input('DEBUG'))
		# first simulate some fake messages
		self.info("1 - receives some fake messages from sut from to tas", bold=True)
		for i in xrange(5):
			# simulate send data
			tasTpl = TestTemplates.TemplateMessage()
			
			layer_req = TestTemplates.TemplateLayer(name='request')
			layer_req.addKey(name='cmd', data='NOTIFY')
			layer_req.addKey(name='tid', data='%s' % i)
			layer_req.addKey(name='userid', data='0')

			layer_sub_req2 = TestTemplates.TemplateLayer(name='resume')
			layer_sub_req2.addKey(name='test1', data='tata')
			layer_sub_req2.addKey(name='test2', data='data')

			layer_sub_req = TestTemplates.TemplateLayer(name='resume')
			layer_sub_req.addKey(name='test1', data='tata')
			layer_sub_req.addKey(name='test2', data='data')
			layer_sub_req.addKey(name='more2', data=layer_sub_req2)
			layer_req.addKey(name='more', data=layer_sub_req)
			
			tasTpl.addLayer(layer=layer_req)
			
			layer_bod = TestTemplates.TemplateLayer(name='body')
			layer_bod.addKey(name='raw', data='ABCDEFGHIJKLMNOPQRSTUVWXYZ\nABCDEFGHIJKLMNOPQRSTUVWXYZ')
			tasTpl.addLayer(layer=layer_bod)
			
			summary = "NOTIFY %s 0" % i
			rawPayload = "NOTIFY %i 0\nABCDEFGHIJKLMNOPQRSTUVWXYZ" % i
			tasTpl.addRaw(raw=rawPayload)
			cp.logSentEvent(summary, tasTpl )
			
			# simulate received data
			tasTpl2 = TestTemplates.TemplateMessage()
			
			layer_req = TestTemplates.TemplateLayer(name='response')
			layer_req.addKey(name='code', data='403')
			layer_req.addKey(name='tid', data='%s' % i)
			layer_req.addKey(name='phrase', data='FORBIDDEN')	
			tasTpl2.addLayer(layer=layer_req)

			layer_sub_req2 = TestTemplates.TemplateLayer(name='resume')
			layer_sub_req2.addKey(name='test1', data='tata')
			layer_sub_req2.addKey(name='test2', data='data')
			
			layer_sub_req = TestTemplates.TemplateLayer(name='resume')
			layer_sub_req.addKey(name='test1', data='tata')
			layer_sub_req.addKey(name='test2', data='data')
			layer_sub_req.addKey(name='more2', data=layer_sub_req2)
			layer_req.addKey(name='more', data=layer_sub_req)
			
			layer_bod = TestTemplates.TemplateLayer(name='body')
			layer_bod.addKey(name='raw', data='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
			tasTpl2.addLayer(layer=layer_bod)
			
			summary = "403 %s FORBIDDEN" % i
			rawPayload = "403 %s FORBIDDEN\n0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" % i	
			tasTpl2.addRaw(raw=rawPayload)
			cp.logRecvEvent(summary, tasTpl2 )

			
		# try to match one msg during the timeout interval
		self.info("- try to match one msg during the timeout interval", bold=True)
		
		# create the template expected
		tpl_expected = TestTemplates.TemplateMessage()
		layer_expected = TestTemplates.TemplateLayer(name='response')
		layer_expected.addKey(name='code', data='403')
		tpl_expected.addLayer(layer=layer_expected)
		
		evt = cp.received( expected = tpl_expected, timeout = input('TIMEOUT') )
		if evt is not None:
			self.info(evt)				

		# try to match one msg during the timeout interval
		self.info("- try to match one msg during the timeout interval", bold=True)
		
		# create the template expected
		tpl_expected = TestTemplates.TemplateMessage()
		layer_expected = TestTemplates.TemplateLayer(name='response')
		layer_expected.addKey(name='code', data='4032')
		layer_expected.addKey(name='tid2', data='2')
		layer_expected.addKey(name='test', data='2')
		tpl_expected.addLayer(layer=layer_expected)				
		
		evt = cp.received( expected = tpl_expected, timeout = input('TIMEOUT') )
		if evt is not None:
			self.info(evt)		
			
		self.step1.setPassed(actual="success")

class TPL_MATCH_03(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		cp = SutAdapter.Adapter(parent=self,name="Test", debug=input('DEBUG'))
		# first simulate some fake messages
		self.info("1 - receives some fake messages from sut from to tas", bold=True)
		for i in xrange(5):
			# simulate send data
			tasTpl = TestTemplates.TemplateMessage()
			
			layer_req = TestTemplates.TemplateLayer(name='request')
			layer_req.addKey(name='cmd', data='NOTIFY')
			layer_req.addKey(name='tid', data='%s' % i)
			layer_req.addKey(name='userid', data='0')

			layer_sub_req2 = TestTemplates.TemplateLayer(name='resume')
			layer_sub_req2.addKey(name='test1', data='tata')
			layer_sub_req2.addKey(name='test2', data='data')

			layer_sub_req = TestTemplates.TemplateLayer(name='resume')
			layer_sub_req.addKey(name='test1', data='tata')
			layer_sub_req.addKey(name='test2', data='data')
			layer_sub_req.addKey(name='more2', data=layer_sub_req2)
			layer_req.addKey(name='more', data=layer_sub_req)
			
			tasTpl.addLayer(layer=layer_req)
			
			layer_bod = TestTemplates.TemplateLayer(name='body')
			layer_bod.addKey(name='raw', data='ABCDEFGHIJKLMNOPQRSTUVWXYZ\nABCDEFGHIJKLMNOPQRSTUVWXYZ')
			tasTpl.addLayer(layer=layer_bod)
			
			summary = "NOTIFY %s 0" % i
			rawPayload = "NOTIFY %i 0\nABCDEFGHIJKLMNOPQRSTUVWXYZ" % i
			tasTpl.addRaw(raw=rawPayload)
			cp.logSentEvent(summary, tasTpl )
			
			# simulate received data
			tasTpl2 = TestTemplates.TemplateMessage()
			
			layer_req = TestTemplates.TemplateLayer(name='response')
			layer_req.addKey(name='code', data='403')
			layer_req.addKey(name='tid', data='%s' % i)
			layer_req.addKey(name='phrase', data='FORBIDDEN')	
			tasTpl2.addLayer(layer=layer_req)

			layer_sub_req2 = TestTemplates.TemplateLayer(name='resume')
			layer_sub_req2.addKey(name='test1', data='tata')
			layer_sub_req2.addKey(name='test2', data='data')
			
			layer_sub_req = TestTemplates.TemplateLayer(name='resume')
			layer_sub_req.addKey(name='test1', data='tata')
			layer_sub_req.addKey(name='test2', data='data')
			layer_sub_req.addKey(name='more2', data=layer_sub_req2)
			layer_req.addKey(name='more', data=layer_sub_req)
			
			layer_bod = TestTemplates.TemplateLayer(name='body')
			layer_bod.addKey(name='raw', data='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
			tasTpl2.addLayer(layer=layer_bod)
			
			summary = "403 %s FORBIDDEN" % i
			rawPayload = "403 %s FORBIDDEN\n0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" % i	
			tasTpl2.addRaw(raw=rawPayload)
			cp.logRecvEvent(summary, tasTpl2 )
			
		# try to match one msg during the timeout interval
		self.info("- try to match one msg during the timeout interval", bold=True)

		# create the template expected
		tpl_expected = TestTemplates.TemplateMessage()
		layer_expected = TestTemplates.TemplateLayer(name='response')
		layer_expected.addKey(name='code', data=TestOperators.LowerThan(x=500))
		layer_expected.addKey(name='tid', data=TestOperators.GreaterThan(x=-1))
		tpl_expected.addLayer(layer=layer_expected)	
		
		evt = cp.received( expected = tpl_expected, timeout = input('TIMEOUT') )
		if evt is not None:
			self.info(evt)				

		# try to match one msg during the timeout interval
		self.info("- try to match one msg during the timeout interval", bold=True)

		# create the template expected
		tpl_expected = TestTemplates.TemplateMessage()
		layer_expected = TestTemplates.TemplateLayer(name='response')
		layer_expected.addKey(name='code', data='4032')
		layer_expected.addKey(name='tid2', data='2')
		layer_expected.addKey(name='test', data='2')
		tpl_expected.addLayer(layer=layer_expected)	
		
		evt = cp.received( expected = tpl_expected, timeout = input('TIMEOUT') )
		if evt is not None:
			self.info(evt)		
			
		self.step1.setPassed(actual="success")

class TPL_MATCH_04(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		cp = SutAdapter.Adapter(parent=self,name="Test", debug=input('DEBUG'))
		# first simulate some fake messages
		self.info("1 - receives some fake messages from sut from to tas", bold=True)
		for i in xrange(5):
			# simulate send data
			tasTpl = TestTemplates.TemplateMessage()
			
			layer_req = TestTemplates.TemplateLayer(name='request')
			layer_req.addKey(name='cmd', data='NOTIFY')
			layer_req.addKey(name='tid', data='%s' % i)
			layer_req.addKey(name='userid', data='0')

			layer_sub_req2 = TestTemplates.TemplateLayer(name='resume')
			layer_sub_req2.addKey(name='test1', data='tata')
			layer_sub_req2.addKey(name='test2', data='data')

			layer_sub_req = TestTemplates.TemplateLayer(name='resume')
			layer_sub_req.addKey(name='test1', data='tata')
			layer_sub_req.addKey(name='test2', data='data')
			layer_sub_req.addKey(name='more2', data=layer_sub_req2)
			layer_req.addKey(name='more', data=layer_sub_req)
			
			tasTpl.addLayer(layer=layer_req)
			
			layer_bod = TestTemplates.TemplateLayer(name='body')
			layer_bod.addKey(name='raw', data='ABCDEFGHIJKLMNOPQRSTUVWXYZ\nABCDEFGHIJKLMNOPQRSTUVWXYZ')
			tasTpl.addLayer(layer=layer_bod)
			
			summary = "NOTIFY %s 0" % i
			rawPayload = "NOTIFY %i 0\nABCDEFGHIJKLMNOPQRSTUVWXYZ" % i
			tasTpl.addRaw(raw=rawPayload)
			cp.logSentEvent(summary, tasTpl )
			
			# simulate received data
			tasTpl2 = TestTemplates.TemplateMessage()
			
			layer_req = TestTemplates.TemplateLayer(name='response')
			layer_req.addKey(name='code', data='403')
			layer_req.addKey(name='tid', data='%s' % i)
			layer_req.addKey(name='phrase', data='FORBIDDEN')	
			tasTpl2.addLayer(layer=layer_req)

			layer_sub_req2 = TestTemplates.TemplateLayer(name='resume')
			layer_sub_req2.addKey(name='test1', data='tata')
			layer_sub_req2.addKey(name='test2', data='data')
			
			layer_sub_req = TestTemplates.TemplateLayer(name='resume')
			layer_sub_req.addKey(name='test1', data='tata')
			layer_sub_req.addKey(name='test2', data='data')
			layer_sub_req.addKey(name='more2', data=layer_sub_req2)
			layer_req.addKey(name='more', data=layer_sub_req)
			
			layer_bod = TestTemplates.TemplateLayer(name='body')
			layer_bod.addKey(name='raw', data='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
			tasTpl2.addLayer(layer=layer_bod)
			
			summary = "403 %s FORBIDDEN" % i
			rawPayload = "403 %s FORBIDDEN\n0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" % i	
			tasTpl2.addRaw(raw=rawPayload)
			cp.logRecvEvent(summary, tasTpl2 )

			
		# try to match one msg during the timeout interval
		self.info("- try to match one msg during the timeout interval", bold=True)

		# create the template expected
		tpl_expected = TestTemplates.TemplateMessage()
		layer_expected = TestTemplates.TemplateLayer(name='response')
		layer_expected.addKey(name=TestOperators.NotContains(needle='tid2'), data=TestOperators.Any() )
		layer_expected.addKey(name=TestOperators.Contains(needle='phrase'), data='FORBIDDEN')
		tpl_expected.addLayer(layer=layer_expected)	
		
		evt = cp.received( expected = tpl_expected, timeout = input('TIMEOUT') )
		if evt is not None:
			self.info(evt)				

		# try to match one msg during the timeout interval
		self.info("- try to match one msg during the timeout interval", bold=True)

		# create the template expected
		tpl_expected = TestTemplates.TemplateMessage()
		layer_expected = TestTemplates.TemplateLayer(name='response')
		tpl_expected.addLayer(layer=layer_expected)	
		
		evt = cp.received( expected = tpl_expected, timeout = input('TIMEOUT') )
		if evt is not None:
			self.info(evt)		
			
		self.step1.setPassed(actual="success")

class TPL_MATCH_05(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		cp = SutAdapter.Adapter(parent=self,name="Test", debug=input('DEBUG'))
		# first simulate some fake messages
		self.info("1 - receives some fake messages from sut from to tas", bold=True)
		for i in xrange(5):
			# fake tas and raw payload
			summary = 'test'
			
			# simulate send data
			tasTpl = TestTemplates.TemplateMessage()
			
			layer_ip = TestTemplates.TemplateLayer(name='IP')
			layer_ip.addKey(name='source-ip', data='127.0.0.1')
			layer_ip.addKey(name='destination-ip', data='127.0.0.1')
			tasTpl.addLayer(layer=layer_ip)

			layer_tcp = TestTemplates.TemplateLayer(name='TCP')
			layer_tcp.addKey(name='source-port', data='60246')
			layer_tcp.addKey(name='destination-port', data='80')
			layer_tcp.addKey(name='tcp-event', data='connected')
			tasTpl.addLayer(layer=layer_tcp)

			layer_http = TestTemplates.TemplateLayer(name='HTTP')
			
			sub_layer_http = TestTemplates.TemplateLayer(name='GET /.../ HTTP 1.1')
			sub_layer_http.addKey(name='method', data='GET')
			sub_layer_http.addKey(name='version', data='HTTP 1.1')
			
			layer_http.addKey(name='request', data=sub_layer_http)
			tasTpl.addLayer(layer=layer_http)

			layer_app = TestTemplates.TemplateLayer(name='APP')
			layer_app.addKey(name='raw', data='xxxxxxxxx')
			tasTpl.addLayer(layer=layer_app)


			rawPayload = "NOTIFY %i 0\nABCDEFGHIJKLMNOPQRSTUVWXYZ" % i	
			tasTpl.addRaw(raw=rawPayload)
			cp.logRecvEvent(summary, tasTpl )

		tpl_expected = TestTemplates.TemplateMessage()
		
		layer_ip_expected = TestTemplates.TemplateLayer(name=TestOperators.Any())
		layer_ip_expected.addKey(name=TestOperators.NotContains('source2'), data=TestOperators.Any())
		layer_ip_expected.addKey(name=TestOperators.Endswith('source-ip'), data='127.0.0.1')
		tpl_expected.addLayer(layer=layer_ip_expected)	

		layer_tcp_expected = TestTemplates.TemplateLayer(name=TestOperators.Contains('TCP'))
		layer_tcp_expected.addKey(name='tcp-event', data=TestOperators.Startswith('conn'))
		layer_tcp_expected.addKey(name=TestOperators.Contains('source'), data='60246')
		layer_tcp_expected.addKey(name='destination-port', data=TestOperators.GreaterThan('70'))
		tpl_expected.addLayer(layer=layer_tcp_expected)	

		layer_http_expected = TestTemplates.TemplateLayer(name='HTTP')
		sub_layer_http_expected = TestTemplates.TemplateLayer(name=TestOperators.Endswith('HTTP 1.1'))
		sub_layer_http_expected.addKey(name='version', data=TestOperators.Contains('1.1'))
		layer_http_expected.addKey(name=TestOperators.Contains('request'), data=sub_layer_http_expected)
		tpl_expected.addLayer(layer=layer_http_expected)	

		layer_app_expected = TestTemplates.TemplateLayer(name=TestOperators.Endswith('PP'))
		layer_app_expected.addKey(name=TestOperators.Contains('raw'), data='xxxxxxxxx' )
		tpl_expected.addLayer(layer=layer_app_expected)	
		
		evt = cp.received( expected = tpl_expected, timeout = input('TIMEOUT') )
		if evt is not None:
			self.info(evt)				

		self.step1.setPassed(actual="success")
				
class TPL_TIMER_EXCEEDED_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)				
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass		
	def definition(self):
		self.step1.start()
		
		cp = SutAdapter.Adapter(parent=self,name="Test")
		# first simulate some fake messages
		self.info("1 - receives some fake messages from sut from to tas", bold=True)
		for i in xrange(5):
			# simulate send data
			tasTpl = TestTemplates.TemplateMessage()
			
			layer_req = TestTemplates.TemplateLayer(name='request')
			layer_req.addKey(name='cmd', data='NOTIFY')
			layer_req.addKey(name='tid', data='%s' % i)
			layer_req.addKey(name='userid', data='0')					
			tasTpl.addLayer(layer=layer_req)
			
			layer_bod = TestTemplates.TemplateLayer(name='body')
			layer_bod.addKey(name='raw', data='ABCDEFGHIJKLMNOPQRSTUVWXYZ\nABCDEFGHIJKLMNOPQRSTUVWXYZ')
			tasTpl.addLayer(layer=layer_bod)
			
			summary = "NOTIFY %s 0" % i
			rawPayload = "NOTIFY %i 0\nABCDEFGHIJKLMNOPQRSTUVWXYZ" % i
			tasTpl.addRaw(raw=rawPayload)
			cp.logSentEvent(summary, tasTpl )
			
			# simulate received data
			tasTpl2 = TestTemplates.TemplateMessage()
			
			layer_req = TestTemplates.TemplateLayer(name='response')
			layer_req.addKey(name='code', data='403')
			layer_req.addKey(name='tid', data='%s' % i)
			layer_req.addKey(name='phrase', data='FORBIDDEN')	
			tasTpl2.addLayer(layer=layer_req)
			
			layer_bod = TestTemplates.TemplateLayer(name='body')
			layer_bod.addKey(name='raw', data='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
			tasTpl2.addLayer(layer=layer_bod)
			
			summary = "403 %s FORBIDDEN" % i
			rawPayload = "403 %s FORBIDDEN\n0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ" % i	
			tasTpl2.addRaw(raw=rawPayload)
			cp.logRecvEvent(summary, tasTpl2 )
			
		# try to match one msg during the timeout interval
		self.info("2 - try to match one msg during the timeout interval", bold=True)
		
		# create the template expected
		tpl_expected = TestTemplates.TemplateMessage()
		layer_expected = TestTemplates.TemplateLayer(name='other')
		tpl_expected.addLayer(layer=layer_expected)	


		evt = cp.received( expected = tpl_expected, timeout = input('TIMEOUT') )
		if evt is not None:
			self.info(evt)	

		self.step1.setPassed(actual="success")
			
]]></testdefinition>
<testexecution><![CDATA[
TPL_TO_SUT_01().execute()
TPL_TO_SUT_02().execute()
TPL_FROM_SUT_01().execute()

TPL_MATCH_ANY_01().execute()
TPL_MATCH_02().execute()
TPL_MATCH_03().execute()
TPL_MATCH_04().execute()
TPL_MATCH_05().execute()
TPL_TIMER_EXCEEDED_01().execute()
]]></testexecution>
<testdevelopment>1386106074.73</testdevelopment>
</file>