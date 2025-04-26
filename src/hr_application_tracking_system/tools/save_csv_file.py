from crewai.tools import BaseTool
from typing import Union, Dict, List
import csv
import os

class SaveToCSVTool(BaseTool):
    name: str = "save_to_csv"
    description: str = "Save a dictionary or list of dictionaries to a CSV file"

    def _run(self, data: Union[Dict, List[Dict]], file_path: str = "output/results.csv") -> str:
        try:
            if isinstance(data, dict):
                data = [data]

            if not data:
                return "No data to save."

            fieldnames = data[0].keys()
            with open(file_path, mode='a', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                # Write header only if file is empty
                csv_file.seek(0, 2)  # Move to end of file
                if csv_file.tell() == 0:
                    writer.writeheader()
                writer.writerows(data)

            return f"Data successfully saved to {file_path}"
        except Exception as e:
            return f"Failed to save to CSV: {e}"