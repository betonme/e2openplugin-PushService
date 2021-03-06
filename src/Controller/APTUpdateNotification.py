#######################################################################
#
#    Push Service for Enigma-2
#    Coded by betonme (c) 2012 <glaserfrank(at)gmail.com>
#    Support: http://www.i-have-a-dreambox.com/wbb2/thread.php?threadid=167779
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#######################################################################

# Config
from Components.config import ConfigYesNo, ConfigText, ConfigNumber, NoSave

# Plugin internal
from Plugins.Extensions.PushService.__init__ import _
from Plugins.Extensions.PushService.ControllerBase import ControllerBase
from Plugins.Extensions.PushService.Logger import log

# Plugin specific
import os
from time import time
from Tools.BoundFunction import boundFunction
from enigma import eConsoleAppContainer


# Constants
SUBJECT = _("APT Update Notification")
BODY    = _("There are updates available:\n%s")


class APTUpdateNotification(ControllerBase):
	
	ForceSingleInstance = True
	
	def __init__(self):
		# Is called on instance creation
		ControllerBase.__init__(self)
		
		# Default configuration
		self.setOption( 'selfcheck', NoSave(ConfigYesNo( default = False )), _("Start update check if not done yet") )
		
		self.data = ""
		self.container = eConsoleAppContainer()
		try:
			self.container_dataAvail_conn = self.container.dataAvail.connect(self.dataAvail)
		except:
			self.container_dataAvail_conn = None
			self.container.dataAvail.append(self.dataAvail)
		try:
			self.container_appClosed_conn = self.container.appClosed.connect(self.aptupgradableFinished)
		except:
			self.container_appClosed_conn = None
			self.container.appClosed.append(self.aptupgradableFinished)

	def run(self, callback, errback):
		self.data = ""
		self.opkgupgradable()
		callback()

	def dataAvail(self, string):
		self.data += string

	def opkgupgradable(self):
		if self.getValue('selfcheck'):
			self.container.execute("apt update && apt-get --just-print upgrade")
		else:
			self.container.execute("apt-get --just-print upgrade")

	def aptupgradableFinished(self, retval=None):
		
		try:
			log.debug( "PushService retval: ",str(retval) )
		except:
			pass
		try:
			log.debug( "PushService self.data: ",str(self.data) )
		except:
			pass
		
		updates = ""
		excepts = ""
		
		if self.data:
			try:
				for line in self.data.split("\n"):
					log.debug( "PushService opkg upgradable data: ",line )
					if line.startswith("Inst"):
						updates += line[5:] + "\r\n"
						continue
			except Exception, e:
				excepts += "\r\n\r\nException:\r\n" + str(e)
		
		if excepts:
			log.exception( excepts )
		
		if updates:
			#callback( SUBJECT, BODY % (updates) )
			
			#TODO Problem test run won't get the message
			# Push mail
			from Plugins.Extensions.PushService.plugin import gPushService
			if gPushService:
				gPushService.push(self, SUBJECT, BODY % (updates))

