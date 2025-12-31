"""
Configuration management for crypto analysis system.
Loads environment variables and provides configuration access.
"""

import os
from typing import Any, Optional
from dotenv import load_dotenv

load_dotenv()


class Config:
      """
          Configuration management class.
              Loads settings from environment variables with sensible defaults.
                  """

    def __init__(self):
              """Initialize configuration from environment"""
              self.env = os.environ.copy()

    def get(self, key: str, default: Any = None) -> Any:
              """
                      Get configuration value from environment.

                                      Args:
                                                  key: Configuration key
                                                              default: Default value if key not found

                                                                                  Returns:
                                                                                              Configuration value or default
                                                                                                      """
              return self.env.get(key, default)

    def get_bool(self, key: str, default: bool = False) -> bool:
              """Get boolean configuration value"""
              value = self.get(key, str(default)).lower()
              return value in ("true", "1", "yes", "on")

    def get_int(self, key: str, default: int = 0) -> int:
              """Get integer configuration value"""
              try:
                            return int(self.get(key, default))
except ValueError:
            return default

    def require(self, key: str) -> str:
              """
                      Get required configuration value.
                              Raises error if not found.
                                      """
              value = self.get(key)
              if value is None:
                            raise ValueError(f"Required config {key} not found in environment")
                        return value

    # API Configuration
    @property
    def api_host(self) -> str:
              return self.get("API_HOST", "0.0.0.0")

    @property
    def api_port(self) -> int:
              return self.get_int("API_PORT", 8000)

    @property
    def debug(self) -> bool:
              return self.get_bool("DEBUG", False)

    # External API Keys
    @property
    def coingecko_api_key(self) -> Optional[str]:
              return self.get("COINGECKO_API_KEY")

    @property
    def taapi_api_key(self) -> str:
              return self.require("TAAPI_API_KEY")

    @property
    def lunarcrush_api_key(self) -> str:
              return self.require("LUNARCRUSH_API_KEY")

    @property
    def dune_api_key(self) -> str:
              return self.require("DUNE_API_KEY")

    @property
    def github_token(self) -> str:
              return self.require("GITHUB_TOKEN")

    # Scoring Configuration
    @property
    def scoring_rules_path(self) -> str:
              return self.get("SCORING_RULES_PATH", "scoring_rules.json")

    @property
    def min_score(self) -> int:
              return self.get_int("MIN_SCORE", 0)

    @property
    def max_score(self) -> int:
              return self.get_int("MAX_SCORE", 100)

    # Cache Configuration
    @property
    def cache_enabled(self) -> bool:
              return self.get_bool("CACHE_ENABLED", True)

    @property
    def cache_ttl_seconds(self) -> int:
              return self.get_int("CACHE_TTL_SECONDS", 300)

    @property
    def redis_url(self) -> Optional[str]:
              return self.get("REDIS_URL")

    # Alert Configuration
    @property
    def alert_enabled(self) -> bool:
              return self.get_bool("ALERT_ENABLED", True)

    @property
    def alert_check_interval(self) -> int:
              return self.get_int("ALERT_CHECK_INTERVAL", 300)

    # Database Configuration
    @property
    def database_url(self) -> Optional[str]:
              return self.get("DATABASE_URL")

    # Logging Configuration
    @property
    def log_level(self) -> str:
              return self.get("LOG_LEVEL", "INFO")

    @property
    def log_file(self) -> Optional[str]:
              return self.get("LOG_FILE")

    def to_dict(self) -> dict:
              """Export non-sensitive configuration as dictionary"""
              return {
                  "api_host": self.api_host,
                  "api_port": self.api_port,
                  "debug": self.debug,
                  "cache_enabled": self.cache_enabled,
                  "cache_ttl_seconds": self.cache_ttl_seconds,
                  "alert_enabled": self.alert_enabled,
                  "log_level": self.log_level,
              }
      
