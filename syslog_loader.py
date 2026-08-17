import re
import pandas as pd

SYSLOG_PATTERN = re.compile(
    r'^(?P<timestamp>\w{3}\s+\d+\s+\d+:\d+:\d+)\s+(?P<host>\S+)\s+(?P<process>\S+):\s+(?P<message>.*)$'
)

def parse_syslog_line(line):
    match = SYSLOG_PATTERN.match(line)
    if not match:
        return None
    return match.groupdict()

def load_syslog(path):
    rows = []
    with open(path, "r") as f:
        for line in f:
            parsed = parse_syslog_line(line.strip())
            if parsed:
                rows.append(parsed)
    return pd.DataFrame(rows)
