from release_one.events import standard_events, add_events, drop_events

# standard event list
standard_events

# adding new events
events = add_events(standard_events,
                    names=['july day', 'aug day'],
                    dates=['2020-07-03', '2020-08-01'],
                    factors=[2.5, 1.5])

events

# removing events
if __name__ == '__main__':
    events = drop_events(events,
                         names='july day',
                         dates='2020-07-03',
                         factors=2.5)

events