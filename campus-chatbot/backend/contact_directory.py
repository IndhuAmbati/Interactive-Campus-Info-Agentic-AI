import pandas as pd
from pathlib import Path

class ContactDirectory:
    def __init__(self):
        self.contacts = []
        
    def load_from_excel(self, filepath):
        """Load faculty contacts from Excel"""
        df = pd.read_excel(filepath)
        self.contacts = df.to_dict('records')
        
    def search_by_department(self, dept):
        """Find contacts by department"""
        return [c for c in self.contacts if c['department'] == dept]
    
    def get_faculty_info(self, name):
        """Get faculty details"""
        # Implementation
        pass