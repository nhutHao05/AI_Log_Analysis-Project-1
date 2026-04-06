"""
Log parser - Parse log entries into structured data
"""
import re
from typing import Optional
from models import LogEntry


class LogParser:
    """Parse log entries into structured data"""
    
    def __init__(self):
        self.timestamp_pattern = re.compile(r'(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})')
        self.severity_pattern = re.compile(r'\b(ERROR|INFO|WARNING|DEBUG|CRITICAL|WARN|FATAL)\b', re.IGNORECASE)
        self.component_pattern = re.compile(r'^\[([^\]]+)\]|^([^:]+):')
        self.uuid_pattern = re.compile(r'\b[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}\b')
    
    def parse_log_entry(self, match) -> Optional[LogEntry]:
        """Parse a log line into structured data"""
        if isinstance(match, str):
            line = match
            file_name = ""
            line_num = 0
        else:
            line = match.get('content', '')
            file_name = match.get('file', '')
            line_num = match.get('line_number', 0)
        
        if not line:
            return None
        
        entry = LogEntry(
            file=file_name,
            line_number=line_num,
            content=line
        )
        
        # Extract timestamp
        timestamp_match = self.timestamp_pattern.search(line)
        if timestamp_match:
            entry.timestamp = timestamp_match.group(1)
        
        # Extract severity
        severity_match = self.severity_pattern.search(line)
        if severity_match:
            entry.severity = severity_match.group(1).upper()
        else:
            entry.severity = "UNKNOWN"
        
        # Extract component and message
        if timestamp_match:
            remainder = line[timestamp_match.end():].strip()
        else:
            remainder = line
        
        if severity_match:
            component_msg = remainder.replace(severity_match.group(0), "", 1).strip()
            
            # Extract component (in brackets or before colon)
            component_match = self.component_pattern.search(component_msg)
            if component_match:
                component = component_match.group(1) or component_match.group(2)
                entry.component = component.strip()
                
                # Message is the rest
                if component_match.group(1):  # [component] format
                    entry.message = component_msg[component_match.end():].strip()
                else:  # component: format
                    entry.message = component_msg[component_match.end():].strip()
            else:
                entry.message = component_msg
        else:
            entry.message = remainder
        
        return entry
    
    def normalize_pattern(self, text: str) -> str:
        """Normalize a log message to find patterns"""
        # Replace UUIDs
        text = self.uuid_pattern.sub('<ID>', text)
        # Replace numbers
        text = re.sub(r'\d+', '<NUM>', text)
        # Replace IP addresses
        text = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<IP>', text)
        return text
