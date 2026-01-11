"""Index manager for tracking analysis history"""

import json
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from ..models.analysis import AnalysisIndex
from ..config import settings
from ..utils.logger import logger
from ..utils.date_utils import validate_date


class IndexManager:
    """Manages analysis index for tracking history."""
    
    def __init__(self, analysis_dir: Optional[Path] = None):
        """Initialize index manager.
        
        Args:
            analysis_dir: Directory containing index.json
        """
        self.analysis_dir = analysis_dir or settings.analysis_dir
        self.index_file = self.analysis_dir / "index.json"
        
        # Ensure directory exists
        self.analysis_dir.mkdir(parents=True, exist_ok=True)
    
    def load_index(self) -> AnalysisIndex:
        """Load analysis index.
        
        Returns:
            AnalysisIndex instance
        """
        if not self.index_file.exists():
            logger.info("Index file not found, creating new index")
            return AnalysisIndex(dates=[], latest="")
        
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            return AnalysisIndex(**data)
            
        except Exception as e:
            logger.error(f"Failed to load index: {e}")
            # Return empty index on error
            return AnalysisIndex(dates=[], latest="")
    
    def save_index(self, index: AnalysisIndex) -> None:
        """Save analysis index.
        
        Args:
            index: AnalysisIndex to save
        """
        try:
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(
                    index.model_dump(mode='json'),
                    f,
                    ensure_ascii=False,
                    indent=2,
                    default=str
                )
            
            logger.info(f"Index saved to {self.index_file}")
            
        except Exception as e:
            logger.error(f"Failed to save index: {e}")
            raise
    
    def add_date(self, date: str) -> None:
        """Add date to index.
        
        Args:
            date: Date string in YYYYMMDD format
        """
        if not validate_date(date):
            raise ValueError(f"Invalid date format: {date}")
        
        index = self.load_index()
        
        if date not in index.dates:
            index.dates.append(date)
            index.dates = sorted(index.dates)
        
        index.latest = date
        index.updated_at = datetime.now()
        
        self.save_index(index)
    
    def get_dates(self, limit: Optional[int] = None) -> List[str]:
        """Get list of analyzed dates.
        
        Args:
            limit: Optional limit on number of dates to return
            
        Returns:
            List of date strings (sorted descending)
        """
        index = self.load_index()
        dates = sorted(index.dates, reverse=True)
        
        if limit:
            return dates[:limit]
        
        return dates
    
    def get_latest(self) -> Optional[str]:
        """Get latest analysis date.
        
        Returns:
            Latest date string or None
        """
        index = self.load_index()
        return index.latest if index.latest else None
