from datetime import datetime, time, timedelta

SHORTCUTS = {
	1: {
	'title': 'To Do Today',
	'start_time': datetime.now(),
	'end_time': datetime.combine(datetime.today(), time.max),
	},
	2: {
	'title': 'To Do This Week',
	'start_time': datetime.now(),
	'end_time': datetime.combine(datetime.today(), time.max),
	}
}