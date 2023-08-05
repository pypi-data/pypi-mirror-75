# coding=utf-8


DAYS = 'days'
HOURS = 'hours'
MINUTES = 'minutes'
SECONDS = 'seconds'
MICROSECONDS = 'microseconds'


# This scheduler must wake up more frequently than the
# regular of 5 minutes because it needs to take external
# changes to the schedule into account.
DEFAULT_MAX_INTERVAL = 5  # seconds

DEFAULT_BEAT_DBURI = 'sqlite:///schedule.db'

ADD_ENTRY_ERROR = """\
Cannot add entry %r to database schedule: %r. Contents: %r
"""
