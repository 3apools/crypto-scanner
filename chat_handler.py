"""
Natural language chat interface for crypto analysis system.
Handles user intent detection, argument extraction, and response formatting.
"""

from enum import Enum
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime
import json
import re
from pydantic import BaseModel, Field


class Intent(str, Enum):
      """User intent detection enums"""
      SCORE_TOKEN = "score_token"
      ANALYZE_PORTFOLIO = "analyze_portfolio"
      COMPARE_TOKENS = "compare_tokens"
      GET_ALERTS = "get_alerts"
      SET_ALERT = "set_alert"
      MARKET_OVERVIEW = "market_overview"
      TOP_PERFORMERS = "top_performers"
      EXPLAIN_SCORE = "explain_score"
      HELP = "help"
      UNKNOWN = "unknown"


@dataclass
class ParsedQuery:
      """Structured user query"""
      intent: Intent
      tokens: List[str]
      portfolio_ids: List[str]
      time_period: Optional[str]
      limit: int = 10
      confidence: float = 0.0
      raw_query: str = ""


class ChatHandler:
      """Handles natural language interface for crypto analysis system."""

    def __init__(self, scoring_engine=None, data_layer=None):
              self.scoring_engine = scoring_engine
              self.data_layer = data_layer
              self.conversation_history: List[Dict[str, str]] = []

    def parse_query(self, user_input: str) -> ParsedQuery:
              """Parse user input into structured intent and parameters."""
              user_input_lower = user_input.lower().strip()
              tokens = self._extract_tokens(user_input)
              portfolio_ids = self._extract_portfolio_ids(user_input)
              time_period = self._extract_time_period(user_input)
              limit = self._extract_limit(user_input)

        intent = self._detect_intent(user_input_lower, tokens, portfolio_ids)
        confidence = self._calculate_confidence(user_input_lower, intent)

        return ParsedQuery(
                      intent=intent,
                      tokens=tokens,
                      portfolio_ids=portfolio_ids,
                      time_period=time_period,
                      limit=limit,
                      confidence=confidence,
                      raw_query=user_input
        )

    def _detect_intent(self, user_input_lower: str, tokens: List[str], portfolio_ids: List[str]) -> Intent:
              """Detect user intent from query text"""
              if any(kw in user_input_lower for kw in ["score", "rate", "grade", "how good"]):
                            return Intent.SCORE_TOKEN if tokens else Intent.UNKNOWN

              if any(kw in user_input_lower for kw in ["portfolio", "holdings", "my tokens"]):
                            return Intent.ANALYZE_PORTFOLIO if portfolio_ids else Intent.UNKNOWN

              if any(kw in user_input_lower for kw in ["compare", "vs", "versus", "better"]):
                            return Intent.COMPARE_TOKENS if len(tokens) >= 2 else Intent.UNKNOWN

              if any(kw in user_input_lower for kw in ["alert", "notify me", "remind me"]):
                            return Intent.SET_ALERT if "set" in user_input_lower else Intent.GET_ALERTS

              if any(kw in user_input_lower for kw in ["market", "overview", "status"]):
                            return Intent.MARKET_OVERVIEW

              if any(kw in user_input_lower for kw in ["top", "best", "worst", "gainers"]):
                            return Intent.TOP_PERFORMERS

              if any(kw in user_input_lower for kw in ["explain", "scoring", "methodology"]):
                            return Intent.EXPLAIN_SCORE

              if any(kw in user_input_lower for kw in ["help", "commands", "usage"]):
                            return Intent.HELP

              return Intent.UNKNOWN

    def _calculate_confidence(self, user_input_lower: str, intent: Intent) -> float:
              """Calculate confidence score for detected intent"""
              if intent == Intent.UNKNOWN:
                            return 0.3

              confidence = 0.7
              if len(user_input_lower.split()) > 5:
                            confidence += 0.1

              if any(w in user_input_lower for w in ["maybe", "possibly", "not sure"]):
                            confidence -= 0.2

              return max(0.0, min(1.0, confidence))

    def _extract_tokens(self, user_input: str) -> List[str]:
              """Extract cryptocurrency ticker symbols"""
              pattern = r'\b([A-Z]{3,5})\b'
              matches = re.findall(pattern, user_input)
              common_words = {"THE", "AND", "ARE", "FOR", "WITH", "THAT"}
              tokens = [m for m in matches if m not in common_words]
              return list(set(tokens))[:10]

    def _extract_portfolio_ids(self, user_input: str) -> List[str]:
              """Extract portfolio identifiers"""
              pattern = r'port(?:folio)?[_-]?(\w+)'
              return re.findall(pattern, user_input, re.IGNORECASE)

    def _extract_time_period(self, user_input: str) -> Optional[str]:
              """Extract time period"""
              time_patterns = {
                  r'\b1h\b|\bone\s+hour': '1h',
                  r'\b4h\b|\bfour\s+hour': '4h',
                  r'\b1d\b|\bone\s+day': '1d',
                  r'\b1w\b|\bone\s+week': '1w',
                  r'\b1m\b|\b1mo\b|\bone\s+month': '1mo',
              }

        for pattern, period in time_patterns.items():
                      if re.search(pattern, user_input, re.IGNORECASE):
                                        return period
                                return None

    def _extract_limit(self, user_input: str) -> int:
              """Extract limit/count parameter"""
        pattern = r'(?:top|get|show|list)\s+(\d+)'
        match = re.search(pattern, user_input, re.IGNORECASE)

        if match:
                      limit = int(match.group(1))
            return max(1, min(limit, 100))
        return 10

    def format_response(self, intent: Intent, data: Dict[str, Any], error: Optional[str] = None) -> str:
              """Format system response into readable chat message."""
        if error:
                      return self._format_error(error)

        if intent == Intent.SCORE_TOKEN:
                      return self._format_token_score(data)
elif intent == Intent.COMPARE_TOKENS:
            return self._format_comparison(data)
elif intent == Intent.MARKET_OVERVIEW:
            return self._format_market_overview(data)
elif intent == Intent.TOP_PERFORMERS:
            return self._format_top_performers(data)
elif intent == Intent.EXPLAIN_SCORE:
            return self._format_explanation(data)
elif intent == Intent.HELP:
            return self._format_help()
else:
            return "I didn't quite understand that. Type 'help' for available commands."

    def _format_token_score(self, data: Dict[str, Any]) -> str:
              """Format token scoring results"""
        if not data or 'token' not in data:
                      return "Could not retrieve token data."

        token = data['token']
        score = data.get('score', {})

        output = f"\n📊 **{token.upper()} Analysis**\n"
        output += f"Overall Score: {score.get('overall', 'N/A')}/100\n"
        output += f"- Fundamentals: {score.get('fundamentals', 'N/A')}/100\n"
        output += f"- Technicals: {score.get('technicals', 'N/A')}/100\n"
        output += f"- Sentiment: {score.get('sentiment', 'N/A')}/100\n"
        output += f"- Smart Money: {score.get('smart_money', 'N/A')}/100\n"

        signal = data.get('signal', {})
        if signal:
                      output += f"Signal: {signal.get('type', 'NEUTRAL')}\n"
            output += f"Confidence: {signal.get('confidence', 0):.1%}\n"

        return output

    def _format_comparison(self, data: Dict[str, Any]) -> str:
              """Format token comparison"""
        output = "\n📈 **Token Comparison**\n"
        if 'tokens' in data:
                      for token, scores in data['tokens'].items():
                                        output += f"\n{token}:\n"
                                        output += f"  Overall Score: {scores.get('overall', 'N/A')}\n"
                                        output += f"  Signal: {scores.get('signal', 'NEUTRAL')}\n"
                                return output

    def _format_market_overview(self, data: Dict[str, Any]) -> str:
              """Format market overview"""
        output = "\n🌍 **Market Overview**\n"
        output += f"BTC Dominance: {data.get('btc_dominance', 'N/A')}\n"
        output += f"Total Market Cap: ${data.get('total_market_cap', 'N/A')}\n"
        output += f"Sentiment: {data.get('sentiment', 'NEUTRAL')}\n"
        return output

    def _format_top_performers(self, data: Dict[str, Any]) -> str:
              """Format top performers"""
        output = "\n🏆 **Top Performers**\n"
        if 'gainers' in data:
                      output += "\nGainers (24h):\n"
            for token, change in data['gainers'][:5]:
                              output += f"  {token}: +{change:.2f}%\n"
                      if 'losers' in data:
                                    output += "\nLosers (24h):\n"
                                    for token, change in data['losers'][:5]:
                                                      output += f"  {token}: {change:.2f}%\n"
                                              return output

    def _format_explanation(self, data: Dict[str, Any]) -> str:
              """Format methodology explanation"""
        output = "\n📚 **Scoring Methodology**\n\n"
        output += "The system scores assets across 4 key dimensions:\n\n"
        output += "**Fundamentals (25%)** - Token economics, development activity, on-chain metrics\n"
        output += "**Technicals (25%)** - Price action, volume patterns, momentum indicators\n"
        output += "**Sentiment (25%)** - Social media, news sentiment, community engagement\n"
        output += "**Smart Money (25%)** - Whale accumulation, exchange flows, pro positioning\n"
        return output

    def _format_error(self, error: str) -> str:
              """Format error message"""
        return f"\n❌ **Error**: {error}\n\nPlease try again or type 'help'."

                                    def _format_help(self) -> str:
                                              """Format help/usage information"""
                                              return """
                                      📖 **Available Commands**

                                      **Token Analysis:**
                                      - "Score BTC" → Get BTC score and signals
                                      - "Compare ETH vs SOL" → Compare tokens
                                      - "Explain scoring" → Learn scoring methodology

                                      **Market Data:**
                                      - "Market overview" → Overall market conditions  
                                      - "Top gainers" → Best 24h performers
                                      - "Top losers" → Worst 24h performers

                                      **Portfolio Management:**
                                      - "Analyze portfolio_1" → Review portfolio
                                      - "Set alert BTC 50000" → Create price alert

                                      **Parameters:** time (1h, 4h, 1d, 1w, 1mo), limit (top N)
                                      """

    def add_to_history(self, user_message: str, bot_response: str):
              """Add message pair to history"""
        self.conversation_history.append({
                      "timestamp": datetime.now().isoformat(),
                      "user": user_message,
                      "bot": bot_response
        })

    def get_history(self, limit: int = 10) -> List[Dict[str, str]]:
              """Get recent conversation history"""
        return self.conversation_history[-limit:]

    def clear_history(self):
              """Clear conversation history"""
        self.conversation_history = []
