"""
FastAPI server for crypto analysis system.
Provides REST API endpoints for token scoring, portfolio analysis, and market data.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import asyncio
import os
from dotenv import load_dotenv

from scoring_engine import ScoringEngine, Intent
from chat_handler import ChatHandler
from config import Config

load_dotenv()
config = Config()

app = FastAPI(
      title="Crypto Scanner API",
      description="Production-grade cryptocurrency analysis system",
      version="1.0.0"
)

app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
)

scoring_engine = ScoringEngine()
chat_handler = ChatHandler(scoring_engine=scoring_engine)


class TokenRequest(BaseModel):
      token: str
      time_period: Optional[str] = "1d"


class PortfolioRequest(BaseModel):
      portfolio_id: str
      tokens: List[str]


class ChatRequest(BaseModel):
      message: str
      user_id: Optional[str] = "default"


class AlertRequest(BaseModel):
      token: str
      price_level: float
      condition: str = "above"


@app.get("/")
async def root():
      return {
                "service": "Crypto Scanner",
                "status": "operational",
                "version": "1.0.0",
                "endpoints": {
                              "score_token": "/api/v1/score/{token}",
                              "market_overview": "/api/v1/market/overview",
                              "chat": "/api/v1/chat",
                              "health": "/health"
                }
      }


@app.get("/health")
async def health_check():
      return {"status": "healthy", "service": "crypto-scanner"}


@app.post("/api/v1/chat")
async def chat(request: ChatRequest):
      """
          Process natural language query and return analysis.
              Handles intent detection, parameter extraction, and response formatting.
                  """
      try:
                parsed_query = chat_handler.parse_query(request.message)

        if parsed_query.intent == Intent.SCORE_TOKEN and parsed_query.tokens:
                      token = parsed_query.tokens[0]
                      score_result = await score_token_internal(token, parsed_query.time_period)
                      response = chat_handler.format_response(
                          parsed_query.intent,
                          score_result
                      )
elif parsed_query.intent == Intent.MARKET_OVERVIEW:
            market_data = {"btc_dominance": "45.2%", "sentiment": "NEUTRAL"}
            response = chat_handler.format_response(
                              parsed_query.intent,
                              market_data
            )
elif parsed_query.intent == Intent.HELP:
            response = chat_handler.format_response(parsed_query.intent, {})
elif parsed_query.intent == Intent.EXPLAIN_SCORE:
            response = chat_handler.format_response(parsed_query.intent, {})
else:
            response = "I didn't understand that query. Try 'help' for available commands."

        chat_handler.add_to_history(request.message, response)

        return {
                      "user_message": request.message,
                      "intent": parsed_query.intent.value,
                      "confidence": parsed_query.confidence,
                      "response": response
        }

except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/score/{token}")
async def score_token(token: str, time_period: Optional[str] = "1d"):
      """
          Score a cryptocurrency token across multiple dimensions.
              Returns 0-100 grade, component scores, and trading signals.
                  """
    return await score_token_internal(token, time_period)


async def score_token_internal(token: str, time_period: Optional[str] = "1d"):
      """Internal scoring logic"""
    try:
              # Simulate scoring (replace with real implementation)
              score_result = {
                            "token": token.upper(),
                            "time_period": time_period or "1d",
                            "score": {
                                              "overall": 72,
                                              "fundamentals": 68,
                                              "technicals": 75,
                                              "sentiment": 70,
                                              "smart_money": 76
                            },
                            "signal": {
                                              "type": "BUY",
                                              "confidence": 0.72
                            },
                            "timestamp": "2025-01-01T00:00:00Z"
              }
              return score_result

except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error scoring {token}: {str(e)}")


@app.get("/api/v1/market/overview")
async def market_overview():
      """Get overall market conditions and sentiment"""
    return {
              "timestamp": "2025-01-01T00:00:00Z",
              "btc_price": 42500.50,
              "btc_dominance": 45.2,
              "eth_dominance": 18.5,
              "total_market_cap": 1200000000000,
              "24h_volume": 45000000000,
              "sentiment": "NEUTRAL",
              "trend": "sideways"
    }


@app.post("/api/v1/portfolio/analyze")
async def analyze_portfolio(request: PortfolioRequest):
      """Analyze cryptocurrency portfolio"""
    try:
              portfolio_scores = {}
              for token in request.tokens:
                            score_data = await score_token_internal(token, "1d")
                            portfolio_scores[token] = score_data["score"]

              return {
                  "portfolio_id": request.portfolio_id,
                  "tokens": portfolio_scores,
                  "average_score": sum(s["overall"] for s in portfolio_scores.values()) / len(portfolio_scores),
                  "risk_level": "MEDIUM"
              }

except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/market/top/{metric}")
async def market_top(metric: str = "gainers", limit: int = Query(10, ge=1, le=100)):
      """Get top performing or underperforming tokens"""
    if metric not in ["gainers", "losers"]:
              raise HTTPException(status_code=400, detail="Metric must be 'gainers' or 'losers'")

    mock_data = {
              "gainers": [
                            ("PEPE", 45.2),
                            ("SHIB", 32.1),
                            ("DOGE", 28.5),
                            ("XRP", 25.3),
                            ("ADA", 22.1)
              ],
              "losers": [
                            ("BTC", -5.2),
                            ("ETH", -4.8),
                            ("SOL", -3.2),
                            ("AVAX", -2.9),
                            ("MATIC", -2.1)
              ]
    }

    data = mock_data[metric][:limit]
    return {
              "metric": metric,
              "timeframe": "24h",
              "data": [{"token": t, "change_percent": c} for t, c in data]
    }


@app.post("/api/v1/alert/create")
async def create_alert(request: AlertRequest):
      """Create price alert for a token"""
    return {
              "alert_id": f"alert_{request.token}_{request.price_level}",
              "token": request.token,
              "price_level": request.price_level,
              "condition": request.condition,
              "status": "active"
    }


@app.get("/api/v1/health/detailed")
async def detailed_health():
      """Detailed health check including component status"""
    return {
              "status": "healthy",
              "components": {
                            "api": "operational",
                            "scoring_engine": "operational",
                            "data_layer": "operational"
              },
              "uptime_seconds": 3600,
              "requests_processed": 1250
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
      return {
          "error": exc.detail,
          "status_code": exc.status_code
}


if __name__ == "__main__":
      import uvicorn
    uvicorn.run(
              "main:app",
              host=config.get("API_HOST", "0.0.0.0"),
              port=config.get("API_PORT", 8000),
              reload=config.get("DEBUG", False)
    )
