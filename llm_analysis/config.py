"""Configuration management for LLM News Analysis"""

import os
from pathlib import Path
from typing import Optional, Any

from dotenv import load_dotenv
from pydantic import Field
try:
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback for older pydantic versions
    from pydantic import BaseSettings


# Get project root directory (absolute path)
PROJECT_ROOT = Path(__file__).parent.parent.resolve()

# Load environment variables from .env file
env_path = PROJECT_ROOT / ".env"
load_dotenv(env_path, override=False)

# Also try loading from llm_analysis/env if it exists
llm_env_path = Path(__file__).parent / ".env"
if llm_env_path.exists():
    load_dotenv(llm_env_path, override=False)


class Settings(BaseSettings):
    """Application settings."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
    openai_api_base_url: Optional[str] = Field(
        default=None,
        alias="OPENAI_API_BASE_URL",
        description="OpenAI API base URL (defaults to official OpenAI API if not set)"
    )
    openai_model: str = Field(default="gpt-3.5-turbo", alias="OPENAI_MODEL")
    openai_timeout: int = Field(default=300, alias="OPENAI_TIMEOUT")
    
    # Directory Configuration (as strings, will be converted to absolute Path in __init__)
    analysis_dir: str = Field(default="", alias="ANALYSIS_DIR")
    news_dir: str = Field(default="", alias="NEWS_DIR")
    results_dir: str = Field(default="", alias="RESULTS_DIR")
    
    # Feishu Webhook Configuration
    feishu_webhook_url: Optional[str] = Field(default=None, alias="FEISHU_WEBHOOK_URL")
    feishu_enabled: bool = Field(default=False, alias="FEISHU_ENABLED")
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
    
    def __init__(self, **kwargs):
        """Initialize settings with absolute path resolution."""
        super().__init__(**kwargs)
        
        # Convert string paths to absolute Path objects
        # If path is relative, resolve against PROJECT_ROOT
        # If path is absolute, use as-is
        
        def resolve_path(path_str: str, default_relative: str) -> Path:
            """Resolve path string to absolute Path.
            
            Args:
                path_str: Path string from config (can be empty, relative, or absolute)
                default_relative: Default relative path if path_str is empty
                
            Returns:
                Absolute Path object
            """
            if not path_str:
                # Use default relative path
                path = PROJECT_ROOT / default_relative
            elif Path(path_str).is_absolute():
                # Already absolute path
                path = Path(path_str)
            else:
                # Relative path, resolve against PROJECT_ROOT
                path = PROJECT_ROOT / path_str
            
            return path.resolve()
        
        # Resolve all paths to absolute paths
        self.analysis_dir = resolve_path(self.analysis_dir, "news/analysis")
        self.news_dir = resolve_path(self.news_dir, "news")
        self.results_dir = resolve_path(self.results_dir, "results")
        
        # Create directories if they don't exist
        self.analysis_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
try:
    settings = Settings()
except Exception as e:
    import sys
    error_msg = str(e)
    if "OPENAI_API_KEY" in error_msg and "Field required" in error_msg:
        print(
            "错误: 缺少必需的配置项 OPENAI_API_KEY\n"
            "请创建 .env 文件并设置以下配置:\n"
            "  OPENAI_API_KEY=your-openai-api-key-here\n"
            "  OPENAI_API_BASE_URL=(可选)\n"
            "  OPENAI_MODEL=gpt-3.5-turbo\n"
            "\n"
            f"配置文件位置: {env_path}\n"
            f"或: {llm_env_path if llm_env_path.exists() else 'llm_analysis/env'}\n",
            file=sys.stderr
        )
    raise
