from webapp.models import Timebox
from webapp.timebox.shortcuts import SHORTCUTS
from datetime import datetime, timedelta, time

def test_timebox_shortcuts():
	"""
	GIVEN a Timebox model
	WHEN timebox is created using shortcut 1
	THEN title is 'To Do Today', start time is now and end time is midnight tonight
	"""
	t = Timebox(title=SHORTCUTS[1]['title'], start_time=SHORTCUTS[1]['start_time'], 
		end_time=SHORTCUTS[1]['end_time'])
	assert t.title == 'To Do Today'
	assert t.start_time < datetime.now() + timedelta(seconds=1)
	assert t.end_time == datetime.combine(datetime.today(), time.max)
