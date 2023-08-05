#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import gettext
import sys
from ikabot.helpers.pedirInfo import read
from ikabot.helpers.process import run
from ikabot.helpers.gui import *
from ikabot.config import *

t = gettext.translation('update',
                        localedir,
                        languages=languages,
                        fallback=True)
_ = t.gettext

def update(session, event, stdin_fd):
	"""
	Parameters
	----------
	session : ikabot.web.session.Session
	event : multiprocessing.Event
	stdin_fd: int
	"""
	sys.stdin = os.fdopen(stdin_fd)
	try:
		print(_('To update ikabot run:'))
		print('python3 -m pip install --user --upgrade ikabot')
		enter()
		event.set()
	except KeyboardInterrupt:
		event.set()
		return
