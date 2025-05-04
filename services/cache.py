import json
from datetime import datetime, timedelta
import os
from typing import Dict, Any, Optional
import logging
from pathlib import Path

class Cache:
    def __init__(self, cache_dir: str = "cache", max_age: int = 3600):
        """
        Initialize cache system
        :param cache_dir: Directory to store cache files
        :param max_age: Maximum age of cache entries in seconds
        """
        self.cache_dir = Path(cache_dir)
        self.max_age = max_age
        self.logger = logging.getLogger(__name__)
        
        # Create cache directory if it doesn't exist
        self.cache_dir.mkdir(exist_ok=True)

    def _get_cache_key(self, universe: str, topic: str, grade: str) -> str:
        """Generate unique cache key using hash for better performance"""
        return f"{hash(f'{universe}_{topic}_{grade}')}.json"

    def _is_cache_valid(self, cache_file: Path) -> bool:
        """Check if cache file is valid (not expired)"""
        try:
            if not cache_file.exists():
                return False

            modification_time = cache_file.stat().st_mtime
            current_time = datetime.now().timestamp()
            
            if (current_time - modification_time) > self.max_age:
                self.logger.debug(f"Cache expired for {cache_file}")
                return False
                
            return True
        except Exception as e:
            self.logger.error(f"Error checking cache validity: {e}")
            return False

    def get(self, universe: str, topic: str, grade: str) -> Optional[Dict[str, Any]]:
        """Get cached response if available"""
        cache_key = self._get_cache_key(universe, topic, grade)
        cache_file = self.cache_dir / cache_key

        try:
            if self._is_cache_valid(cache_file):
                self.logger.debug(f"Cache hit for {cache_key}")
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                self.logger.debug(f"Cache miss for {cache_key}")
                return None
        except Exception as e:
            self.logger.error(f"Error reading cache: {e}")
            return None

    def set(self, universe: str, topic: str, grade: str, data: Dict[str, Any]) -> bool:
        """Store response in cache"""
        cache_key = self._get_cache_key(universe, topic, grade)
        cache_file = self.cache_dir / cache_key

        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.debug(f"Cached {cache_key}")
            return True
        except Exception as e:
            self.logger.error(f"Error writing cache: {e}")
            return False

    def clear(self) -> None:
        """Clear all cache entries"""
        try:
            for file in self.cache_dir.glob("*.json"):
                file.unlink()
            self.logger.debug("Cache cleared")
        except Exception as e:
            self.logger.error(f"Error clearing cache: {e}")
