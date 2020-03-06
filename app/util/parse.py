import datetime

def parse_time_interval(time_input):
    if time_input[-1] == "h":
        time_interval = datetime.time(hour=int(time_input[:-1]))
    if time_input[-1] == "d":
        days = int(time_input[:-1])
        time_interval = datetime.time(hour=days*24)
    return time_interval