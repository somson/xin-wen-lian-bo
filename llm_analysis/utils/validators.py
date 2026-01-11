"""Validation utility functions for LLM News Analysis"""

from typing import Any, Dict


def validate_news_content(content: str) -> bool:
    """Validate news content format.
    
    Args:
        content: News content to validate
        
    Returns:
        True if content is valid, False otherwise
    """
    if not isinstance(content, str):
        return False
    
    if len(content.strip()) == 0:
        return False
    
    # Check minimum length (at least some content)
    if len(content.strip()) < 10:
        return False
    
    return True


def validate_analysis_result(result: Dict[str, Any]) -> bool:
    """Validate analysis result structure.
    
    Args:
        result: Analysis result dictionary
        
    Returns:
        True if result is valid, False otherwise
    """
    if not isinstance(result, dict):
        return False
    
    # Check required fields
    required_fields = ['date', 'sentiment', 'trends']
    
    for field in required_fields:
        if field not in result:
            return False
    
    # Validate date format
    date = result.get('date')
    if not isinstance(date, str) or len(date) != 8:
        return False
    
    # Validate sentiment structure
    sentiment = result.get('sentiment')
    if not isinstance(sentiment, dict):
        return False
    
    if 'score' not in sentiment or 'category' not in sentiment:
        return False
    
    # Validate trends structure
    trends = result.get('trends')
    if not isinstance(trends, dict):
        return False
    
    return True
