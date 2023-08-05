<?xml version="1.0" encoding="utf-8" ?>
<file>
<properties><parameters /><probes><probe><active>False</active><args /><name>probe01</name><type>default</type></probe></probes><agents><agent><description /><type /><name>AGENT</name><value>agent-socket01</value></agent></agents><descriptions><description><value>admin</value><key>author</key></description><description><value>12/08/2012</value><key>creation date</key></description><description><value>Just a basic sample.</value><key>summary</key></description><description><value>None.</value><key>prerequisites</key></description><description><value><comments /></value><key>comments</key></description><description><value>myplugins</value><key>libraries</key></description><description><value>myplugins</value><key>adapters</key></description><description><value>Writing</value><key>state</key></description><description><value>REQ_01</value><key>requirement</key></description></descriptions><inputs-parameters><parameter><description /><type>bool</type><name>DEBUG</name><value>False</value><scope>local</scope></parameter><parameter><description /><type>float</type><name>TIMEOUT</name><value>1.0</value><scope>local</scope></parameter></inputs-parameters><outputs-parameters><parameter><description /><type>float</type><name>TIMEOUT</name><value>1.0</value><scope>local</scope></parameter></outputs-parameters></properties>
<testdefinition><![CDATA[
class STATES_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)					
	def test(self):
		self.info(txt='hello world', bold=False, italic=False)
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass
	def definition(self):
		self.step1.start()
		
		a = TestAdapter.Adapter(parent=self, name='AA', debug=False)
		b = TestAdapter.State(parent=a, name='AABB', initial='idle')
		b.set(state='init')
		self.info( b.get() )
		b.set(state='end')
		self.info( b.get() )

		self.step1.setPassed(actual="success")
		
class TIMERS_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)					
	def test(self):
		self.info(txt='hello world', bold=False, italic=False)

	def test2(self):
		self.info(txt='hello world 2', bold=False, italic=False)

	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass
	def definition(self):
		self.step1.start()
		
		a = TestAdapter.Adapter(parent=self, name='AA', debug=input('DEBUG'))

		t = TestAdapter.Timer(parent=a, duration=10, name='b', callback=self.test, logEvent=True)
		t.start()
		
		t2= TestAdapter.Timer(parent=a, duration=10, name='c', callback=self.test2, logEvent=True)
		t2.start()
		
		self.wait( 20 )
		
		self.step1.setPassed(actual="success")

class TIMERS_RESTART_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)					
	def test(self):
		self.info(txt='hello world', bold=False, italic=False)
	def prepare(self):
		pass
	def cleanup(self, aborted):
		pass
	def definition(self):
		self.step1.start()
		
		a = SutAdapter.Adapter(parent=self, name='AA', debug=False)

		t = SutAdapter.Timer(parent=a, duration=10, name='b', callback=self.test)
		t.start()
		self.wait( 15)
		t.restart()
		self.wait( 20 )
		
		self.step1.setPassed(actual="success")
		
class STORAGE_01(TestCase):
	def description(self):
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)					
	def prepare(self):
		
		self.ADP_A = SutAdapter.Adapter(parent=self, name='test1', realname=None, debug=False, showEvts=True, showSentEvts=True, showRecvEvts=True, shared=False, agentSupport=False, agent=None, timeoutSleep=0.05)
		self.ADP_B= SutAdapter.Adapter(parent=self, name='test2', realname=None, debug=False, showEvts=True, showSentEvts=True, showRecvEvts=True, shared=False, agentSupport=False, agent=None, timeoutSleep=0.05)
		
	def cleanup(self, aborted):
		pass
	def definition(self):
		self.step1.start()
		
		self.warning( self.ADP_A.getAdapterId() )
		self.warning( self.ADP_B.getAdapterId() )
		
		self.ADP_A.privateSaveFile(destname='rezre.txt', data="hello world é")
		
		self.ADP_B.privateSaveFile(destname='rezre2é.txt', data="hello world2 é")
		
		Private(self).saveFile(destname="tc", data="test")
		
		Private(self).appendFile(destname="tc2.txt", data="test1")
		Private(self).appendFile(destname="tc2.txt", data="test2")
		
		self.step1.setPassed(actual="success")
		
class STORAGE_02(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)

	def prepare(self):
		# adapters and libraries
		pass

	def cleanup(self, aborted):
		pass

	def definition(self):
		# starting initial step
		if self.step1.isEnabled():
			self.step1.start()
			
			Private(self).saveFile(destname="test", data="@string")
			
			self.step1.setPassed(actual="success")

class STORAGE_03(TestCase):
	def description(self):
		# testcase description
		self.setPurpose(purpose="Testcase sample")

		# steps description
		self.step1 = self.addStep(expected="result expected", description="step description", summary="step sample", enabled=True)

	def prepare(self):
		# adapters and libraries
		pass

	def cleanup(self, aborted):
		pass

	def definition(self):
		# starting initial step
		if self.step1.isEnabled():
			self.step1.start()

			Private(self).saveFile(destname="test", data="@string é")
			
			self.step1.setPassed(actual="success")

]]></testdefinition>
<testexecution><![CDATA[
STATES_01(suffix=None).execute()
TIMERS_01(suffix=None).execute()
TIMERS_RESTART_01(suffix=None).execute()
STORAGE_01(suffix=None).execute()
STORAGE_02(suffix=None).execute()
STORAGE_03(suffix=None).execute()]]></testexecution>
<testdevelopment>1386106129.04</testdevelopment>
</file>