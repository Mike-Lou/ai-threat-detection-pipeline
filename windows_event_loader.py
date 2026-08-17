import xml.etree.ElementTree as ET
import pandas as pd

def load_windows_event_log(path):
    tree = ET.parse(path)
    root = tree.getroot()

    rows = []
    for event in root.findall(".//Event"):
        row = {}
        for child in event:
            row[child.tag] = child.text
        rows.append(row)

    return pd.DataFrame(rows)
