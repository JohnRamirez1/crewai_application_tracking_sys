from crewai.tools import BaseTool
from typing import Union, Dict, List
import csv
import os
    

def save_tocsv(filepath, data):
    # write to CSV
    with open(filepath, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if file.tell() == 0:
            writer.writeheader() 
            writer.writerow(data)