"""OpenAI LLM client service"""

import asyncio
from typing import Optional, Dict, Any
from openai import AsyncOpenAI
from openai import APIError, Timeout, RateLimitError

from ..config import settings
from ..utils.logger import logger


class LLMClient:
    """Client for interacting with OpenAI API."""
    
    def __init__(
        self,
        api_base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[int] = None
    ):
        """Initialize LLM client.
        
        Args:
            api_base_url: OpenAI API base URL
            api_key: OpenAI API key
            model: Model name to use
            timeout: Request timeout in seconds
        """
        self.api_key = api_key or settings.openai_api_key
        self.model = model or settings.openai_model
        self.timeout = timeout or settings.openai_timeout
        
        # Handle optional base_url
        self.api_base_url = api_base_url or settings.openai_api_base_url
        
        # Create client with optional base_url
        client_kwargs = {
            "api_key": self.api_key,
            "timeout": self.timeout
        }
        if self.api_base_url:
            client_kwargs["base_url"] = self.api_base_url
        
        self.client = AsyncOpenAI(**client_kwargs)
    
    async def analyze(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        json_mode: bool = True,
        max_retries: int = 3
    ) -> str:
        """Analyze content using LLM.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            json_mode: Whether to use JSON mode
            max_retries: Maximum number of retry attempts
            
        Returns:
            LLM response text
            
        Raises:
            APIError: If API call fails after retries
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        for attempt in range(max_retries):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    response_format={"type": "json_object"} if json_mode else None,
                    temperature=0.7,
                )
                
                content = response.choices[0].message.content
                logger.info(f"LLM analysis completed successfully")
                return content
                
            except RateLimitError as e:
                wait_time = 2 ** attempt  # Exponential backoff
                logger.warning(f"Rate limit error, retrying in {wait_time}s: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(wait_time)
                else:
                    raise
                    
            except Timeout as e:
                logger.warning(f"Timeout error, retrying: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
                else:
                    raise
                    
            except APIError as e:
                logger.error(f"OpenAI API error: {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
                else:
                    raise
                    
            except Exception as e:
                logger.error(f"Unexpected error in LLM call: {e}")
                raise
