from datetime import date


def get_today():
	"""
	:rtype: date
	"""
	return date.today()


def get_today_str():
	"""
	:rtype:  str
	"""
	return str(get_today())


get_date = get_today
