"""Date utility functions for LLM News Analysis"""

import re
from datetime import datetime
from typing import Optional


def validate_date(date_str: str) -> bool:
    """Validate date string format (YYYYMMDD).
    
    Args:
        date_str: Date string to validate
        
    Returns:
        True if date format is valid, False otherwise
    """
    if not isinstance(date_str, str):
        return False
    
    pattern = r'^\d{8}$'
    if not re.match(pattern, date_str):
        return False
    
    try:
        year = int(date_str[:4])
        month = int(date_str[4:6])
        day = int(date_str[6:8])
        datetime(year, month, day)
        return True
    except (ValueError, IndexError):
        return False


def format_date(date: Optional[datetime] = None) -> str:
    """Format datetime to YYYYMMDD string.
    
    Args:
        date: Datetime object to format. If None, uses current date.
        
    Returns:
        Formatted date string (YYYYMMDD)
    """
    if date is None:
        date = datetime.now()
    
    return date.strftime('%Y%m%d')


def get_today_date() -> str:
    """Get today's date in YYYYMMDD format.
    
    Returns:
        Today's date string (YYYYMMDD)
    """
    return format_date()


def parse_date(date_str: str) -> datetime:
    """Parse YYYYMMDD string to datetime object.
    
    Args:
        date_str: Date string in YYYYMMDD format
        
    Returns:
        Datetime object
        
    Raises:
        ValueError: If date string is invalid
    """
    if not validate_date(date_str):
        raise ValueError(f"Invalid date format: {date_str}. Expected YYYYMMDD.")
    
    year = int(date_str[:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])
    
    return datetime(year, month, day)
