# Recurrent
Recurrent is a python library for natural language parsing of dates and recurring
events. It turns strings like "every tuesday and thurs until next month"
into [RFC-compliant RRULES][1], to be fed into a calendar api or [python-dateutil's][2]
rrulestr.

```sh
pip install recurrent
```

## Examples
### Date times
* next tuesday
* tomorrow
* in an hour

### Recurring events
* on weekdays
* every fourth of the month from jan 1 2010 to dec 25th 2020
* each thurs until next month
* once a year on the fourth thursday in november
* tuesdays and thursdays at 3:15

### Messy strings
* Please schedule the meeting for every other tuesday at noon
* Set an alarm for next tuesday at 11pm

## Usage
```python
>>> import datetime
>>> from recurrent import RecurringEvent
>>> r = RecurringEvent(now_date=datetime.datetime(2010, 1, 1))
>>> r.parse('every day starting next tuesday until feb')
'DTSTART:20100105\nRRULE:FREQ=DAILY;INTERVAL=1;UNTIL=20100201'
>>> r.is_recurring
True
>>> r.get_params()
{'dtstart': '20100105', 'freq': 'daily', 'interval': 1, 'until': '20100201'}

>>> r.parse('feb 2nd')
datetime.datetime(2010, 2, 2, 0, 0)

>>> r.parse('not a date at all')
>>>
```

You can then use python-dateutil to work with the recurrence rules.
```python
>>> from dateutil import rrule
>>> rr = rrule.rrulestr(r.get_RFC_rrule())
>>> rr.after(datetime.datetime(2010, 1, 2))
datetime.datetime(2010, 1, 5, 0, 0)
>>> rr.after(datetime.datetime(2010, 1, 25))
datetime.datetime(2010, 1, 26, 0, 0)
```

## Dependencies
Recurrent uses [parsedatetime][3] to parse dates.

## Things it can't do

Recurrent is regrettably quite U.S. (and completely english) centric. Contributions from other perspectives are welcome :)

## Credits
Recurrent is inspired by the similar Ruby library Tickle by Joshua
Lippiner. It also uses the parsedatetime library for fuzzy human date
parsing.

## Author
Ken Van Haren kvh@science.io [@squaredloss](http://twitter.com/squaredloss)

[1]: http://www.kanzaki.com/docs/ical/rrule.html
[2]: http://labix.org/python-dateutil
[3]: https://github.com/bear/parsedatetime
[4]: https://github.com/kvh/parsedatetime
