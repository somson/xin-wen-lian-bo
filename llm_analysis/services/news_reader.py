"""News content reader service"""

from pathlib import Path
from typing import Optional

from ..config import settings
from ..utils.logger import logger
from ..utils.validators import validate_news_content
from ..utils.date_utils import validate_date, get_today_date


class NewsReader:
    """Service for reading news content from Markdown files."""
    
    def __init__(self, news_dir: Optional[Path] = None):
        """Initialize news reader.
        
        Args:
            news_dir: Directory containing news Markdown files
        """
        self.news_dir = news_dir or settings.news_dir
    
    def read_news(self, date: Optional[str] = None) -> str:
        """Read news content for specified date.
        
        Args:
            date: Date string in YYYYMMDD format. If None, uses today's date.
            
        Returns:
            News content as string
            
        Raises:
            FileNotFoundError: If news file doesn't exist
            ValueError: If content is invalid
        """
        if date is None:
            date = get_today_date()
        
        if not validate_date(date):
            raise ValueError(f"Invalid date format: {date}")
        
        file_path = self.news_dir / f"{date}.md"
        
        if not file_path.exists():
            raise FileNotFoundError(f"News file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not validate_news_content(content):
                raise ValueError(f"Invalid news content in {file_path}")
            
            logger.info(f"News content read from {file_path}")
            return content
            
        except Exception as e:
            logger.error(f"Failed to read news file: {e}")
            raise
