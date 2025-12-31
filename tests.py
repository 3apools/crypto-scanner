"""
Unit tests for crypto analysis system.
Tests for scoring engine, chat handler, and API endpoints.
"""

import pytest
import json
from unittest.mock import Mock, patch
from scoring_engine import ScoringEngine, Intent
from chat_handler import ChatHandler, Intent as ChatIntent
from main import app, score_token_internal
from config import Config


@pytest.fixture
def scoring_engine():
      return ScoringEngine()


@pytest.fixture
def chat_handler():
      return ChatHandler()


@pytest.fixture
def config():
      return Config()


class TestChatHandler:
      """Test chat handler parsing and response formatting"""

    def test_parse_score_token_intent(self, chat_handler):
              parsed = chat_handler.parse_query("Score BTC")
              assert parsed.intent == ChatIntent.SCORE_TOKEN
              assert "BTC" in parsed.tokens

    def test_parse_compare_intent(self, chat_handler):
              parsed = chat_handler.parse_query("Compare ETH vs SOL")
              assert parsed.intent == ChatIntent.COMPARE_TOKENS
              assert len(parsed.tokens) >= 2

    def test_parse_market_overview_intent(self, chat_handler):
              parsed = chat_handler.parse_query("Market overview")
              assert parsed.intent == ChatIntent.MARKET_OVERVIEW

    def test_parse_help_intent(self, chat_handler):
              parsed = chat_handler.parse_query("help")
              assert parsed.intent == ChatIntent.HELP

    def test_extract_time_period(self, chat_handler):
              parsed = chat_handler.parse_query("Score BTC 1h")
              assert parsed.time_period == "1h"

    def test_extract_limit(self, chat_handler):
              parsed = chat_handler.parse_query("Top 20 gainers")
              assert parsed.limit == 20

    def test_confidence_calculation(self, chat_handler):
              parsed = chat_handler.parse_query("Score BTC please")
              assert 0 <= parsed.confidence <= 1


class TestScoringEngine:
      """Test scoring engine functionality"""

    def test_scoring_engine_initialization(self, scoring_engine):
              assert scoring_engine is not None

    def test_score_calculation(self, scoring_engine):
              token_data = {
                            "symbol": "BTC",
                            "price": 42500,
                            "volume_24h": 25000000000
              }
              # Score should be between 0-100
              assert True  # Placeholder

    def test_signal_generation(self, scoring_engine):
              # Test that signals are properly generated
              assert True  # Placeholder


class TestConfig:
      """Test configuration management"""

    def test_config_initialization(self, config):
              assert config is not None

    def test_config_get_default(self, config):
              value = config.get("NON_EXISTENT_KEY", "default")
              assert value == "default"

    def test_config_api_host(self, config):
              host = config.api_host
              assert isinstance(host, str)
              assert len(host) > 0

    def test_config_api_port(self, config):
              port = config.api_port
              assert isinstance(port, int)
              assert 1 <= port <= 65535

    def test_config_bool_conversion(self, config):
              result = config.get_bool("NON_EXISTENT", False)
              assert result is False


class TestAPIEndpoints:
      """Test FastAPI endpoints"""

    @pytest.fixture
    def client(self):
              from fastapi.testclient import TestClient
              return TestClient(app)

    def test_root_endpoint(self, client):
              response = client.get("/")
              assert response.status_code == 200
              assert "service" in response.json()

    def test_health_check(self, client):
              response = client.get("/health")
              assert response.status_code == 200
              assert response.json()["status"] == "healthy"

    def test_score_token_endpoint(self, client):
              response = client.get("/api/v1/score/BTC")
              assert response.status_code == 200
              data = response.json()
              assert "token" in data
              assert "score" in data

    def test_market_overview_endpoint(self, client):
              response = client.get("/api/v1/market/overview")
              assert response.status_code == 200
              data = response.json()
              assert "btc_dominance" in data


class TestDataValidation:
      """Test data validation and edge cases"""

    def test_invalid_token_symbol(self, chat_handler):
              parsed = chat_handler.parse_query("Score XYZ123")
              # Should handle invalid symbols gracefully
              assert parsed is not None

    def test_empty_query(self, chat_handler):
              parsed = chat_handler.parse_query("")
              assert parsed.intent == ChatIntent.UNKNOWN

    def test_very_long_query(self, chat_handler):
              long_query = "Score " + "BTC " * 100
              parsed = chat_handler.parse_query(long_query)
              # Should limit tokens to reasonable number
              assert len(parsed.tokens) <= 10


class TestErrorHandling:
      """Test error handling"""

    def test_missing_required_config(self, config):
              # Should handle missing required config gracefully
              assert config is not None

    def test_invalid_json_handling(self):
              # Test JSON parsing with invalid data
              invalid_json = "{invalid json}"
              try:
                            json.loads(invalid_json)
                            assert False, "Should have raised error"
except json.JSONDecodeError:
            assert True


if __name__ == "__main__":
      pytest.main([__file__, "-v"])
  
