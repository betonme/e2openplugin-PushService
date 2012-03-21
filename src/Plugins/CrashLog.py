# Config
from Components.config import ConfigYesNo, NoSave

# Plugin internal
from Plugins.Extensions.PushService.__init__ import _
from Plugins.Extensions.PushService.PluginBase import PluginBase

# Plugin specific
import os


CRASHLOG_DIR = '/media/hdd'

SUBJECT = _("Found CrashLog(s)")
BODY    = _("Crashlog(s) are attached")


class CrashLog(PluginBase):
	
	ForceSingleInstance = True
	
	def __init__(self):
		# Is called on instance creation
		PluginBase.__init__(self)
		self.crashlogs = []

		# Default configuration
		self.setOption( 'delete_logs', NoSave(ConfigYesNo( default = False )), _("Delete crashlog(s)") )

	def run(self):
		# Return Header, Body, Attachment
		# If empty or none is returned, nothing will be sent
		# Search crashlog files
		self.crashlogs = []
		text = "Found crashlogs, see attachment(s)\n"
		for file in os.listdir( CRASHLOG_DIR ):
			if file.startswith("enigma2_crash_") and file.endswith(".log"):
				crashlog = os.path.join( CRASHLOG_DIR, file )
				self.crashlogs.append(crashlog)
		if self.crashlogs:
			return SUBJECT, BODY, self.crashlogs
		else:
			return None

	# Callback functions
	def success(self):
		# Called after successful sending the message
		if self.getValue('delete_logs'):
			# Delete crashlogs
			for crashlog in self.crashlogs[:]:
				if os.path.exists( crashlog ):
					os.remove( crashlog )
				self.crashlogs.remove( crashlog )
		else:
			# Rename crashlogs to avoid resending it
			for crashlog in self.crashlogs[:]:
				if os.path.exists( crashlog ):
					# Adapted from autosubmit - instead of .sent we will use .pushed
					currfilename = str(os.path.basename(crashlog))
					newfilename = "/media/hdd/" + currfilename + ".pushed"
					os.rename(crashlog,newfilename)
				self.crashlogs.remove( crashlog )

	def error(self):
		# Called after message sent has failed
		self.crashlogs = []
