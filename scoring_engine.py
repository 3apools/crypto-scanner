"""
CRYPTO SCANNER & INVESTOR ASSISTANT - SCORING ENGINE (Phase 1)
Implements multi-factor scoring with fundamentals, technicals, sentiment, smart money
"""

import json
from typing import Dict, Optional, Tuple
from datetime import datetime
from pydantic import BaseModel
from data_layer import TokenMetrics, ScoringResult
import logging

logger = logging.getLogger(__name__)


class ScoringRules(BaseModel):
      """Configuration for all scoring parameters."""
      fundamentals: Dict = {}
      technicals: Dict = {}
      sentiment: Dict = {}
      smart_money: Dict = {}
      weights: Dict = {}
      edge_cases: Dict = {}


class ScoringEngine:
      """Multi-factor scoring engine for cryptocurrency tokens."""

    def __init__(self, rules_path: str = "scoring_rules.json"):
              """Initialize with rules from JSON file."""
              with open(rules_path, 'r') as f:
                            self.rules_config = json.load(f)
                        self.weights = self.rules_config.get('weights', {})
        logger.info(f"Scoring engine initialized with rules from {rules_path}")

    def score_token(self, metrics: TokenMetrics) -> ScoringResult:
              """Calculate overall grade (0-100) and trading signal for a token."""
        fundamentals_score = self._score_fundamentals(metrics)
        technicals_score = self._score_technicals(metrics)
        sentiment_score = self._score_sentiment(metrics)
        smart_money_score = self._score_smart_money(metrics)

        weight_fund = self.weights.get('fundamentals', 0.25)
        weight_tech = self.weights.get('technicals', 0.25)
        weight_sent = self.weights.get('sentiment', 0.25)
        weight_smart = self.weights.get('smart_money', 0.25)

        total_weight = weight_fund + weight_tech + weight_sent + weight_smart
        if total_weight == 0:
                      total_weight = 1.0

        ensemble_score = (
                      (fundamentals_score * weight_fund +
                                    technicals_score * weight_tech +
                                    sentiment_score * weight_sent +
                                    smart_money_score * weight_smart) / total_weight
        )

        final_grade = max(0, min(100, round(ensemble_score)))
        signal = self._grade_to_signal(final_grade)

        component_scores = {
                      'fundamentals': round(fundamentals_score, 2),
                      'technicals': round(technicals_score, 2),
                      'sentiment': round(sentiment_score, 2),
                      'smart_money': round(smart_money_score, 2),
                      'ensemble': round(ensemble_score, 2)
        }

        confidence = self._calculate_confidence(metrics, ensemble_score)
        reasoning = self._generate_reasoning(metrics, final_grade, component_scores)

        return ScoringResult(
                      token_symbol=metrics.token_symbol,
                      grade=final_grade,
                      signal=signal,
                      timestamp=datetime.utcnow(),
                      component_scores=component_scores,
                      reasoning=reasoning,
                      confidence=confidence
        )

    def _score_fundamentals(self, metrics: TokenMetrics) -> float:
              """Score fundamentals: market cap, TVL, development activity."""
        score = 50

        if metrics.market_cap_usd:
                      if metrics.market_cap_usd > 1e9:
                                        score += 20
        elif metrics.market_cap_usd > 100e6:
                score += 15
elif metrics.market_cap_usd > 10e6:
                score += 10

        if metrics.tvl_usd:
                      if metrics.tvl_usd > 500e6:
                                        score += 15
        elif metrics.tvl_usd > 100e6:
                score += 10
elif metrics.tvl_usd > 10e6:
                score += 5

        if metrics.github_commits_90d:
                      if metrics.github_commits_90d > 200:
                                        score += 15
        elif metrics.github_commits_90d > 100:
                score += 10
elif metrics.github_commits_90d > 50:
                score += 5

        if metrics.github_stars:
                      if metrics.github_stars > 20000:
                                        score += 10
        elif metrics.github_stars > 5000:
                score += 5

        return max(0, min(100, score))

    def _score_technicals(self, metrics: TokenMetrics) -> float:
              """Score technical indicators."""
        score = 50

        if metrics.rsi_14:
                      if 30 < metrics.rsi_14 < 70:
                                        score += 5
        elif metrics.rsi_14 < 30:
                score += 15
elif metrics.rsi_14 > 70:
                score -= 10

        if metrics.macd is not None:
                      if metrics.macd > 0:
                                        score += 10
        else:
                score -= 5

                  if metrics.sma_50 and metrics.sma_200:
                                if metrics.sma_50 > metrics.sma_200:
                                                  score += 15
                  elif metrics.sma_50 < metrics.sma_200:
                                    score -= 10

        if metrics.volume_24h_usd and metrics.market_cap_usd:
                      volume_ratio = metrics.volume_24h_usd / metrics.market_cap_usd
                      if volume_ratio > 0.05:
                                        score += 10
        elif volume_ratio < 0.01:
                score -= 10

        if metrics.atr_14:
                      if metrics.atr_14 < 5:
                                        score += 5

                  return max(0, min(100, score))

    def _score_sentiment(self, metrics: TokenMetrics) -> float:
              """Score sentiment indicators."""
        score = 50

        if metrics.sentiment_score is not None:
                      if metrics.sentiment_score > 0.5:
                                        score += 20
        elif metrics.sentiment_score > 0.2:
                score += 10
elif metrics.sentiment_score < -0.5:
                score -= 20
elif metrics.sentiment_score < -0.2:
                score -= 10

        if metrics.social_volume_24h:
                      if metrics.social_volume_24h > 100000:
                                        score += 10
        elif metrics.social_volume_24h < 1000:
                score -= 5

        if metrics.mentions_positive and metrics.mentions_negative:
                      ratio = metrics.mentions_positive / (metrics.mentions_negative + 1)
                      if ratio > 3:
                                        score += 15
        elif ratio < 0.5:
                score -= 10

        return max(0, min(100, score))

    def _score_smart_money(self, metrics: TokenMetrics) -> float:
              """Score smart money activity."""
        score = 50

        if metrics.whale_transactions_24h:
                      if metrics.whale_transactions_24h > 50:
                                        score += 10
        elif metrics.whale_transactions_24h > 20:
                score += 5

        if metrics.exchange_netflow:
                      if metrics.exchange_netflow > 0:
                                        if metrics.exchange_netflow > 10e6:
                                                              score -= 5
                      else:
                                        score += 10

                  if metrics.holder_concentration:
                                if metrics.holder_concentration < 0.3:
                                                  score += 15
                  elif metrics.holder_concentration < 0.5:
                                    score += 5
else:
                score -= 10

        return max(0, min(100, score))

    def _grade_to_signal(self, grade: int) -> str:
              """Convert numeric grade to trading signal."""
        if grade >= 90:
                      return "Strong Buy"
elif grade >= 75:
            return "Buy"
elif grade >= 50:
            return "Hold"
elif grade >= 25:
            return "Sell"
else:
            return "Strong Sell"

    def _calculate_confidence(self, metrics: TokenMetrics, score: float) -> float:
              """Calculate confidence based on data availability."""
        available_metrics = 0
        required_metrics = 0

        for attr in ['price_usd', 'market_cap_usd', 'volume_24h_usd']:
                      required_metrics += 1
                      if getattr(metrics, attr, None):
                                        available_metrics += 1

                  for attr in ['rsi_14', 'macd', 'sma_50', 'sentiment_score', 'whale_transactions_24h']:
                                if getattr(metrics, attr, None) is not None:
                                                  available_metrics += 1

                            confidence = min(1.0, max(0.5, available_metrics / 12))
        return round(confidence, 2)

    def _generate_reasoning(self, metrics: TokenMetrics, grade: int, scores: Dict) -> str:
              """Generate human-readable explanation."""
        parts = [
                      f"{metrics.token_symbol} scored {grade}/100",
                      f"({self._grade_to_signal(grade)})"
        ]

        comp_scores = {k: v for k, v in scores.items() if k != 'ensemble'}
        if comp_scores:
                      best = max(comp_scores, key=comp_scores.get)
                      worst = min(comp_scores, key=comp_scores.get)
                      parts.append(f"Strongest: {best.capitalize()} ({scores[best]}/100)")
                      parts.append(f"Weakest: {worst.capitalize()} ({scores[worst]}/100)")

        return " | ".join(parts)


__all__ = ['ScoringEngine', 'ScoringRules']
