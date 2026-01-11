"""Text processing utility functions for LLM News Analysis"""

import re
from typing import List


def clean_text(text: str) -> str:
    """Clean and normalize text content.
    
    Args:
        text: Raw text content
        
    Returns:
        Cleaned text
    """
    if not isinstance(text, str):
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text


def extract_summary(text: str, max_length: int = 200) -> str:
    """Extract summary from text.
    
    Args:
        text: Full text content
        max_length: Maximum length of summary
        
    Returns:
        Text summary
    """
    if not text:
        return ""
    
    cleaned = clean_text(text)
    
    if len(cleaned) <= max_length:
        return cleaned
    
    # Try to cut at sentence boundary
    truncated = cleaned[:max_length]
    last_period = truncated.rfind('。')
    last_exclamation = truncated.rfind('！')
    last_question = truncated.rfind('？')
    
    cut_point = max(last_period, last_exclamation, last_question)
    
    if cut_point > max_length * 0.7:  # Only use if we keep at least 70% of text
        return truncated[:cut_point + 1]
    
    return truncated + "..."


def split_into_chunks(text: str, chunk_size: int = 4000) -> List[str]:
    """Split text into chunks for LLM processing.
    
    Args:
        text: Text to split
        chunk_size: Maximum size of each chunk
        
    Returns:
        List of text chunks
    """
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    # Split by paragraphs first
    paragraphs = text.split('\n\n')
    
    for paragraph in paragraphs:
        if len(current_chunk) + len(paragraph) + 2 <= chunk_size:
            current_chunk += paragraph + '\n\n'
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = paragraph + '\n\n'
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
