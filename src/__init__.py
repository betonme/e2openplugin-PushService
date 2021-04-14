from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from os import environ as os_environ
import gettext

from Components.config import config, ConfigSubsection, ConfigNothing, ConfigEnableDisable, ConfigText, ConfigClock, ConfigSelectionNumber


# Config options
config.pushservice = ConfigSubsection()

config.pushservice.about = ConfigNothing()

config.pushservice.enable = ConfigEnableDisable(default=True)

config.pushservice.boxname = ConfigText(default="Enigma2", fixed_size=False)
config.pushservice.xmlpath = ConfigText(default="/etc/enigma2/pushservice.xml", fixed_size=False)

config.pushservice.time = ConfigClock(default=0)
config.pushservice.period = ConfigSelectionNumber(0, 1000, 1, default=24)
config.pushservice.runonboot = ConfigEnableDisable(default=True)
config.pushservice.bootdelay = ConfigSelectionNumber(5, 1000, 5, default=10)

config.pushservice.push_errors = ConfigEnableDisable(default=False)

config.pushservice.popups_success_timeout = ConfigSelectionNumber(-1, 20, 1, default=3)
config.pushservice.popups_warning_timeout = ConfigSelectionNumber(-1, 20, 1, default=-1)
config.pushservice.popups_error_timeout = ConfigSelectionNumber(-1, 20, 1, default=-1)

config.pushservice.log_shell = ConfigEnableDisable(default=False) 
config.pushservice.log_write = ConfigEnableDisable(default=False) 
config.pushservice.log_file = ConfigText(default="/tmp/pushservice.log", fixed_size=False) 


def localeInit():
	lang = language.getLanguage()[:2]  # getLanguage returns e.g. "fi_FI" for "language_country"
	os_environ["LANGUAGE"] = lang      # Enigma doesn't set this (or LC_ALL, LC_MESSAGES, LANG). gettext needs it!
	gettext.bindtextdomain("PushService", resolveFilename(SCOPE_PLUGINS, "Extensions/PushService/locale"))

def _(txt):
	if txt:
		t = gettext.dgettext("PushService", txt)
		if t == txt:
			t = gettext.gettext(txt)
		return t 
	else:
		return ""

localeInit()
language.addCallback(localeInit)
