#!/usr/bin/env python
# -*- coding=utf-8 -*-

# -------------------------------------------------------------------
# Copyright (c) 2010-2020 Denis Machard
# This file is part of the extensive automation project
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA
# -------------------------------------------------------------------

import sys
import copy

from ea.testexecutorlib import TestValidatorsLib as TestValidators
from ea.testexecutorlib import TestTemplatesLib as TestTemplates
from ea.testexecutorlib import TestOperatorsLib as TestOperators
from ea.testexecutorlib import TestAdapterLib as TestAdapter

from ea.sutadapters.CLI import codec_term
from ea.sutadapters.CLI import templates_term
from ea.sutadapters.CLI import templates
from ea.sutadapters.CLI import client

__NAME__= """TERM"""

KEY_CTRLC = '\x03'
KEY_ENTER = '\n'

class SshTerminal(TestAdapter.Adapter):
	
	def __init__(self, parent,  destIp, destPort=22, 
											bindIp = '0.0.0.0', bindPort=0,  
											login='admin', password='admin', 
											privateKey=None,  privateKeyPath=None, 
											verbose=True, name=None,  
											debug=False, logEventSent=True, 
											logEventReceived=True, parentName=None, shared=False, 
											agent=None, agentSupport=False, 
											terminalWidth=400, terminalHeight=400, cycleSnap=1):
		"""
		Terminal to interact easily with SSH server.

		@param parent: parent testcase
		@type parent: testcase

		@param name: adapter name used with from origin/to destination (default=None)
		@type name: string/none
		
		@param login: ssh login (default=admin)
		@type login: string
		
		@param privateKey: string private key to use to authenticate, push your public key on the remote server
		@type privateKey: string/none
		
		@param privateKeyPath: path to the private key to use to authenticate, push your public key on the remote server
		@type privateKeyPath: string/none
		
		@param verbose: False to disable verbose mode (default=True)
		@type verbose: boolean
		
		@param password: ssh password (default=admin)
		@type password: string
		
		@param bindIp: bind on ip (source ip)
		@type bindIp: string

		@param bindPort: bind on port (source port)
		@type bindPort: integer

		@param destIp: destination ip
		@type destIp: string

		@param destPort: destination port
		@type destPort: integer
		
		@param debug: True to activate debug mode (default=False)
		@type debug: boolean

		@param shared: shared adapter (default=False)
		@type shared:	boolean

		@param agent: agent to use
		@type agent: string/none
		
		@param agentSupport: agent support (default=False)
		@type agentSupport:	boolean
		
		@param terminalWidth: terminal width (default=400)
		@type terminalWidth: integer
		
		@param terminalHeight: terminal height (default=400)
		@type terminalHeight: integer

		@param cycleSnap: interval to take a snap of the screen (default=1s)
		@type cycleSnap: integer
		"""
		# init adapter
		TestAdapter.Adapter.__init__(self, name = __NAME__, parent = parent, 
                                    debug=debug, realname=name, shared=shared,
                                    showEvts=verbose, showSentEvts=verbose, showRecvEvts=verbose )
		
		self.parent = parent
		self.logEventSent = logEventSent
		self.logEventReceived = logEventReceived
		
		self.codec  = None
		self.ADP_SSH = None
		self.ADP_SSH = client.Client(parent=parent, login=login, password=password, 
                                    privateKey=privateKey, privateKeyPath=privateKeyPath,
                                    bindIp=bindIp, bindPort=bindPort,  destIp=destIp, destPort=destPort, 
                                    destHost='',  debug=debug, logEventSent=False, 
                                    logEventReceived=False, parentName=__NAME__, 
                                    shared=shared, sftpSupport=False, agent=agent,  
                                    agentSupport=agentSupport, verbose = verbose,
                                    terminalWidth=terminalWidth, terminalHeight=terminalHeight
																				)
		self.buf = ''

		self.codec = codec_term.Codec(parent=self, 
                                        terminalWidth=terminalWidth, 
                                        terminalHeight=terminalHeight, 
                                        cycleSnap=cycleSnap)
		self.cfg = {}
		
		self.cfg['dst-ip'] = destIp
		self.cfg['dst-port'] = destPort
		self.cfg['bind-ip'] = bindIp
		self.cfg['bind-port'] = bindPort

		self.__checkConfig()

		self.lower_event = None
		
		# wrap function
		self.ADP_SSH.handleIncomingData = self.handleIncomingData
		self.ADP_SSH.handleConnectionFailed = self.handleConnectionFailed
		self.codec.handleScreen = self.handleScreen
		
	def __checkConfig(self):	
		"""
		Private function
		"""
		self.debug("config: %s" % self.cfg)

	def onReset(self):
		"""
		Called automaticly on reset adapter
		"""
		if self.codec is not None: 
			self.codec.reset()
		if self.ssh() is not None:
			self.ssh().onReset()

	def ssh(self):
		"""
		Return ssh level
		"""
		return self.ADP_SSH

	def encapsule(self,  layer_term):
		"""
		Encapsule
		"""
		lower_event = TestTemplates.TemplateMessage()
		
		if self.ADP_SSH.cfg['agent-support']:
			layer_agent= TestTemplates.TemplateLayer('AGENT')
			layer_agent.addKey(name='name', data=self.ADP_SSH.cfg['agent']['name'] )
			layer_agent.addKey(name='type', data=self.ADP_SSH.cfg['agent']['type'] )
			lower_event.addLayer(layer=layer_agent)
			
		# add layer to tpl
		lower_event.addLayer(layer=layer_term)
		return lower_event

	def handleScreen(self, screen):
		"""
		"""
		summary, tpl_term = screen
		new_tpl = self.encapsule( layer_term=tpl_term)
		new_tpl.addRaw( tpl_term.get("data") )
		if self.logEventReceived:
			self.logRecvEvent( shortEvt = summary, tplEvt = new_tpl ) 

	def handleConnectionFailed(self, err):
		"""
		"""
		new_tpl = self.encapsule(layer_term=templates_term.term_open_failed(data=err) )
		new_tpl.addRaw( err )
		self.logRecvEvent( shortEvt = "open error", tplEvt = new_tpl ) 
		
	def handleIncomingData(self, data):
		"""
		Called on incoming data
		
		@param data: tcp data received
		@type data: string
		
		@param lower: template tcp data received
		@type lower: templatemessage
		"""
		try:
			# bytes to str
			if sys.version_info > (3,): 
				if not isinstance(data, bytes): data = data.encode()
			
			# save ssh date in private area, can be useful for debug
			self.privateAppendFile(destname="ssh_dump.log", data=data)

			# finally decode the data
			self.codec.decode(data=data)
		except Exception as e:
			self.error('Error while waiting on incoming ssh data: %s' % str(e))

	def getExpectedTemplate(self, event):
		"""
		"""
		tpl = self.ssh().getExpectedTemplate(event=None)
		tpl.addLayer(event)
		
		return tpl

	
	def doSession(self, timeout=10.0, message=None):
		"""
		Open a session
		
		@param timeout: time max to wait to receive event in second (default=10s)
		@type timeout: float			
		
		@param message: message expected
		@type message: string/operators/none	

		@return: True on success, False otherwise
		@rtype: boolean	
		"""
		ret = False
		self.connect()
		if self.isOpened(timeout=timeout, message=message) is not None:
			ret = True
		return ret
		
	
	def doClose(self, timeout=10.0):
		"""
		Close the session
		
		@param timeout: time max to wait to receive event in second (default=10s)
		@type timeout: float			

		@return: True on closed, False otherwise
		@rtype: boolean	
		"""
		ret = False
		self.disconnect()
		if self.codec is not None: self.codec.unwatch()
		self.lower_event = None
		ret = True
		return ret
		
	
	def doText(self, text):
		"""
		Type text on terminal

		@param text: the text to type
		@type text: str			
		
		@return: True on success, False otherwise
		@rtype: boolean	
		"""
		ret = False
		if self.ssh().connected:
			self.ssh().sendData(dataRaw=text +"\n")
			new_tpl = self.encapsule( layer_term=templates_term.term_data(data=text+"\n") )
			new_tpl.addRaw(text)
			if self.logEventSent:
				self.logSentEvent( shortEvt = "send text", tplEvt = new_tpl )
			ret = True
		return ret
		
	
	def doClear(self):
		"""
		Clear the terminal

		@return: True on success, False otherwise
		@rtype: boolean	
		"""
		ret = False
		if self.ssh().connected:
			self.ssh().sendData(dataRaw="clear\n")
			
			new_tpl = self.encapsule(layer_term=templates_term.term_data(data="clear\n") )
	
			if self.logEventSent:
				self.logSentEvent( shortEvt = "clear screen", tplEvt = new_tpl )
			ret = True
		return ret

	
	def doShorcut(self, key):
		"""
		Type key on terminal
		
		@param key: SutAdapters.SSH.KEY_CTRLC|SutAdapters.SSH.KEY_ENTER
		@type key: str		
		
		@return: True on success, False otherwise
		@rtype: boolean	
		"""
		ret = False
		if self.ssh().connected:
			self.ssh().sendData(dataRaw=key + "\n")
			
			new_tpl = self.encapsule( layer_term=templates_term.term_data(data=key) )
			new_tpl.addRaw(key)
			
			if self.logEventSent:
				self.logSentEvent( shortEvt = "send key", tplEvt = new_tpl )
			ret = True
		return ret
		
	
	def connect(self):
		"""
		Connect to the SSH server
		Login is performed in automatic
		"""
		new_tpl = self.encapsule(  layer_term=templates_term.term_open(ip=self.cfg['dst-ip'],
																					port=self.cfg['dst-port'], login=self.ssh().cfg['login']) )
		if self.logEventSent:
			self.logSentEvent( shortEvt = "open", tplEvt = new_tpl )
		
		tpl = self.ssh().connect()
		
	
	def disconnect(self):
		"""
		Disconnect from the SCP server
		"""
		new_tpl = self.encapsule( layer_term=templates_term.term_close() )
		if self.logEventSent:
			self.logSentEvent( shortEvt = "close", tplEvt = new_tpl )

		tpl = self.ssh().disconnect()

	
	def isOpened(self, timeout=10.0, message=None):
		"""
		Waits to receive "opened" event until the end of the timeout

		@param timeout: time max to wait to receive event in second (default=10s)
		@type timeout: float			
		
		@param message: message expected
		@type message: string/operators/none	

		@return: an event matching with the template or None otherwise
		@rtype: templatemessage	
		"""
		TestAdapter.check_timeout(caller=TestAdapter.caller(), timeout=timeout)
		
		# construct the expected template
		expected = self.getExpectedTemplate(event=templates_term.term_opened(data=message))
		
		# try to match the template 
		evt = self.received( expected=expected, timeout=timeout )
		return evt
		
	
	def isClosed(self, timeout=10.0):
		"""
		Waits to receive "closed" event until the end of the timeout

		@param timeout: time max to wait to receive event in second (default=10s)
		@type timeout: float			

		@return: an event matching with the template or None otherwise
		@rtype: templatemessage	
		"""
		TestAdapter.check_timeout(caller=TestAdapter.caller(), timeout=timeout)
		
		# construct the expected template
		expected = self.getExpectedTemplate(event=templates_term.term_closed())
		
		# try to match the template 
		evt = self.received( expected=expected, timeout=timeout )
		return evt
		
	
	def hasReceivedScreen(self, timeout=10.0, text=None):
		"""
		Waits to receive "screen" event until the end of the timeout

		@param timeout: time max to wait to receive event in second (default=10s)
		@type timeout: float			
		
		@param text: text expected
		@type text: string/operators/none	

		@return: an event matching with the template or None otherwise
		@rtype: templatemessage	
		"""
		TestAdapter.check_timeout(caller=TestAdapter.caller(), timeout=timeout)
		
		# construct the expected template
		expected = self.getExpectedTemplate(event=templates_term.term_data(data=text))
		
		# try to match the template 
		evt = self.received( expected=expected, timeout=timeout )
		return evt