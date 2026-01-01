# Nansen API Integration Guide

## Overview

This guide explains how to integrate Nansen API keys into the crypto-scanner system for **Smart Money Tracking**. The Nansen API provides sophisticated whale tracking, exchange flow analysis, and professional trader positioning data that feeds into the system's 4-factor scoring methodology.

## What is Smart Money Tracking?

Smart Money Tracking represents the **4th dimension** of our multi-factor scoring system:
- **Fundamentals** (25%): Token economics, development, on-chain metrics
- - **Technicals** (25%): Price action, RSI, MACD, moving averages
  - - **Sentiment** (25%): Community mood, social signals
    - - **Smart Money** (25%): Whale activity, exchange flows, professional positioning ← **YOU ARE HERE**
     
      - The smart money dimension is calculated by three sub-components:
      - 1. **Whale Tracking** (±15 points): Accumulation vs distribution patterns
        2. 2. **Exchange Flows** (±15 points): Inflow/outflow sentiment analysis
           3. 3. **Professional Traders** (±20 points): Positioning by institutional players
             
              4. Final score range: **0-100**
             
              5. ## Setup Instructions
             
              6. ### Step 1: Obtain Nansen API Keys
             
              7. You need two API keys from Nansen (they provide failover redundancy):
             
              8. **Option A: Get Keys Directly**
              9. 1. Visit https://www.nansen.ai/api
                 2. 2. Sign up or log in to your account
                    3. 3. Navigate to API settings
                       4. 4. Generate two API keys (recommended for production resilience)
                          5. 5. Copy both keys
                            
                             6. **Option B: Using Provided Test Keys**
                             7. If you're using provided test keys, skip to Step 2.
                            
                             8. ### Step 2: Update .env.example
                            
                             9. The `.env.example` file now includes two Nansen API key variables:
                            
                             10. ```bash
                                 # Nansen API Keys (For Smart Money Tracking)
                                 NANSEN_API_KEY_1=your_first_api_key_here
                                 NANSEN_API_KEY_2=your_second_api_key_here
                                 ```

                                 ### Step 3: Create .env File (Local Development)

                                 1. Copy `.env.example` to `.env`:
                                 2.    ```bash
                                          cp .env.example .env
                                          ```

                                       2. Update the Nansen keys in your local `.env`:
                                       3.    ```bash
                                                # Nansen API Keys (For Smart Money Tracking)
                                                NANSEN_API_KEY_1=E7lEmOj6RBnH6nTPHQvDMo7q52z2tL75
                                                NANSEN_API_KEY_2=dnIogOVzvZBoMaVOJ8axpnOQrLnFLgkA
                                                ```

                                             3. **DO NOT commit `.env` to Git** - it contains secrets
                                             4.    - `.gitignore` already excludes it (production safety measure)
                                               
                                                   - ### Step 4: Environment Variable Setup (Production)
                                               
                                                   - For Docker/production deployment:
                                               
                                                   - **Docker Compose:**
                                                   - ```yaml
                                                     services:
                                                       crypto-scanner:
                                                         environment:
                                                           NANSEN_API_KEY_1: ${NANSEN_API_KEY_1}
                                                           NANSEN_API_KEY_2: ${NANSEN_API_KEY_2}
                                                     ```

                                                     **Docker Run:**
                                                     ```bash
                                                     docker run \
                                                       -e NANSEN_API_KEY_1=your_key_here \
                                                       -e NANSEN_API_KEY_2=your_key_here \
                                                       crypto-scanner:latest
                                                     ```

                                                     **Kubernetes:**
                                                     ```yaml
                                                     env:
                                                       - name: NANSEN_API_KEY_1
                                                         valueFrom:
                                                           secretKeyRef:
                                                             name: nansen-secrets
                                                             key: api-key-1
                                                     ```

                                                     ## How Smart Money Scoring Works

                                                     ### Data Flow

                                                     ```
                                                     ┌─────────────────────────────────────────────────┐
                                                     │         Smart Money Analyzer Module             │
                                                     │         (smart_money.py)                        │
                                                     └────────────────┬────────────────────────────────┘
                                                                      │
                                                          ┌───────────┼───────────┐
                                                          ▼           ▼           ▼
                                                       Whale       Exchange    Professional
                                                      Tracking     Flows       Traders
                                                          │           │           │
                                                          └───────────┼───────────┘
                                                                      │
                                                             Score Composition:
                                                             Base: 50 (neutral)
                                                             Whale: ±15 (accumulation/distribution)
                                                             Flow: ±15 (inflow/outflow sentiment)
                                                             Professional: ±20 (institutional positioning)
                                                             ─────────────────────────
                                                             Final: 0-100 (normalized)
                                                     ```

                                                     ### Whale Tracking Component

                                                     **What it measures:**
                                                     - Wallets holding 1000+ BTC or equivalent
                                                     - - Large buy/sell activity in past 24-48 hours
                                                       - - Long-term accumulation vs distribution trends
                                                        
                                                         - **Score impact:**
                                                         - - Strong accumulation: **+15 points** (bullish signal)
                                                           - - Balanced activity: **0 points** (neutral)
                                                             - - Strong distribution: **-15 points** (bearish signal)
                                                              
                                                               - **Data sources:**
                                                               - - On-chain whale transaction analysis
                                                                 - - Mega-whale monitoring (1000+ BTC)
                                                                   - - 7-day moving average of whale flows
                                                                    
                                                                     - ### Exchange Flow Component
                                                                    
                                                                     - **What it measures:**
                                                                     - - Cryptocurrency inflow to exchanges (selling pressure)
                                                                       - - Cryptocurrency outflow from exchanges (buying pressure)
                                                                         - - Exchange deposit/withdrawal ratios
                                                                          
                                                                           - **Score impact:**
                                                                           - - Net outflows (hodling): **+15 points** (bullish)
                                                                             - - Balanced flows: **0 points** (neutral)
                                                                               - - Net inflows (selling): **-15 points** (bearish)
                                                                                
                                                                                 - **Interpretation:**
                                                                                 - - High outflow = whales moving to cold storage = bullish
                                                                                   - - High inflow = preparation for exchange selling = bearish
                                                                                     - - Extreme values are mean-reverting
                                                                                      
                                                                                       - ### Professional Trader Component
                                                                                      
                                                                                       - **What it measures:**
                                                                                       - - Positioning by institutional traders
                                                                                         - - Derivatives market sentiment
                                                                                           - - Professional fund accumulation/distribution
                                                                                            
                                                                                             - **Score impact:**
                                                                                             - - Long bias: **+20 points** (bullish)
                                                                                               - - Neutral: **0 points**
                                                                                                 - - Short bias: **-20 points** (bearish)
                                                                                                  
                                                                                                   - **Data sources:**
                                                                                                   - - Nansen entity labels (professional traders, funds)
                                                                                                     - - Portfolio aggregation across addresses
                                                                                                       - - Historical position tracking
                                                                                                        
                                                                                                         - ## Usage Example
                                                                                                        
                                                                                                         - ### Basic Integration
                                                                                                        
                                                                                                         - ```python
                                                                                                           from smart_money import SmartMoneyAnalyzer

                                                                                                           # Initialize analyzer
                                                                                                           analyzer = SmartMoneyAnalyzer(
                                                                                                               api_key_1="your_first_key",
                                                                                                               api_key_2="your_second_key"
                                                                                                           )

                                                                                                           # Analyze a specific token
                                                                                                           token = "ethereum"  # or contract address
                                                                                                           chain = "ethereum"  # or "polygon", "arbitrum", etc.

                                                                                                           smart_money_score = analyzer.analyze_token(token, chain)

                                                                                                           # Returns:
                                                                                                           # {
                                                                                                           #   "token": "ethereum",
                                                                                                           #   "smart_money_score": 72,          # 0-100
                                                                                                           #   "whale_sentiment": "bullish",     # bullish/neutral/bearish
                                                                                                           #   "exchange_flow_sentiment": "bullish",
                                                                                                           #   "professional_sentiment": "neutral",
                                                                                                           #   "details": {
                                                                                                           #     "whale_component": 12,          # ±15 points
                                                                                                           #     "flow_component": 13,           # ±15 points
                                                                                                           #     "professional_component": 8,    # ±20 points
                                                                                                           #     "base_score": 50
                                                                                                           #   },
                                                                                                           #   "updated_at": "2025-01-09T12:34:56Z"
                                                                                                           # }
                                                                                                           ```
                                                                                                           
                                                                                                           ### Integration with Multi-Factor Scoring
                                                                                                           
                                                                                                           ```python
                                                                                                           from scoring_engine import ScoringEngine
                                                                                                           from smart_money import SmartMoneyAnalyzer

                                                                                                           # Initialize components
                                                                                                           scorer = ScoringEngine()
                                                                                                           smart_money = SmartMoneyAnalyzer(
                                                                                                               api_key_1=os.getenv("NANSEN_API_KEY_1"),
                                                                                                               api_key_2=os.getenv("NANSEN_API_KEY_2")
                                                                                                           )

                                                                                                           # Calculate token score (all 4 dimensions)
                                                                                                           def calculate_full_score(token: str, contract: str) -> dict:
                                                                                                               # Fundamentals (25%)
                                                                                                               fundamentals = scorer.score_fundamentals(token)

                                                                                                               # Technicals (25%)
                                                                                                               technicals = scorer.score_technicals(token)

                                                                                                               # Sentiment (25%)
                                                                                                               sentiment = scorer.score_sentiment(token)

                                                                                                               # Smart Money (25%)
                                                                                                               smart_money_data = smart_money.analyze_token(contract, "ethereum")
                                                                                                               smart_money_score = smart_money_data["smart_money_score"]

                                                                                                               # Combine all 4 factors (25% weight each)
                                                                                                               final_score = (
                                                                                                                   fundamentals * 0.25 +
                                                                                                                   technicals * 0.25 +
                                                                                                                   sentiment * 0.25 +
                                                                                                                   smart_money_score * 0.25
                                                                                                               )

                                                                                                               return {
                                                                                                                   "token": token,
                                                                                                                   "final_score": final_score,
                                                                                                                   "components": {
                                                                                                                       "fundamentals": fundamentals,
                                                                                                                       "technicals": technicals,
                                                                                                                       "sentiment": sentiment,
                                                                                                                       "smart_money": smart_money_score
                                                                                                                   }
                                                                                                               }
                                                                                                           ```
                                                                                                           
                                                                                                           ## API Rate Limits & Best Practices
                                                                                                           
                                                                                                           ### Rate Limits
                                                                                                           
                                                                                                           **Nansen API limits (standard tier):**
                                                                                                           - 100 requests per minute
                                                                                                           - - Dual keys allow ~200 requests/min (automatic failover)
                                                                                                             - 
                                                                                                             ### Optimization Tips
                                                                                                             
                                                                                                             1. **Use Caching** (5-minute TTL):
                                                                                                             2.    ```python
                                                                                                                      @cache(ttl=300)  # 5 minutes
                                                                                                                      def get_smart_money_score(token: str):
                                                                                                                          return analyzer.analyze_token(token)
                                                                                                                      ```
                                                                                                                   
                                                                                                                   2. **Batch Requests**:
                                                                                                                   3.    ```python
                                                                                                                            tokens = ["ethereum", "polygon", "arbitrum"]
                                                                                                                            scores = asyncio.gather(*[
                                                                                                                                analyzer.analyze_token(token) for token in tokens
                                                                                                                            ])
                                                                                                                            ```
                                                                                                                         
                                                                                                                         3. **Request Queuing**:
                                                                                                                         4.    - Queue large scans (100+ tokens)
                                                                                                                               -    - Process sequentially to avoid hitting rate limits
                                                                                                                                    -    - Monitor API response times
                                                                                                                                     
                                                                                                                                         - 4. **Dual Key Failover**:
                                                                                                                                           5.    - System automatically switches to KEY_2 if KEY_1 fails
                                                                                                                                                 -    - Add retry logic with exponential backoff (1s, 2s, 4s)
                                                                                                                                                  
                                                                                                                                                      - ## Troubleshooting
                                                                                                                                                  
                                                                                                                                                      - ### Issue: "401 Unauthorized" Error
                                                                                                                                                  
                                                                                                                                                      - **Cause:** Invalid or expired API keys
                                                                                                                                                  
                                                                                                                                                      - **Solution:**
                                                                                                                                                      - 1. Verify keys are correctly set in `.env`
                                                                                                                                                        2. 2. Check that keys haven't been rotated at Nansen
                                                                                                                                                           3. 3. Test keys directly with curl:
                                                                                                                                                              4.    ```bash
                                                                                                                                                                       curl -H "Authorization: Bearer YOUR_KEY" \
                                                                                                                                                                            https://api.nansen.ai/v1/wallet/whale-tracking
                                                                                                                                                                       ```
                                                                                                                                                                    
                                                                                                                                                                    ### Issue: "429 Too Many Requests" Error
                                                                                                                                                                
                                                                                                                                                                **Cause:** Rate limit exceeded
                                                                                                                                                              
                                                                                                                                                              **Solution:**
                                                                                                                                                              1. Implement request queuing
                                                                                                                                                              2. 2. Reduce polling frequency
                                                                                                                                                                 3. 3. Use caching (5-minute TTL)
                                                                                                                                                                    4. 4. Consider upgrading Nansen tier
                                                                                                                                                                      
                                                                                                                                                                       5. ### Issue: "503 Service Unavailable" Error
                                                                                                                                                                      
                                                                                                                                                                       6. **Cause:** Nansen API outage or maintenance
                                                                                                                                                                      
                                                                                                                                                                       7. **Solution:**
                                                                                                                                                                       8. 1. Check Nansen status page
                                                                                                                                                                          2. 2. Implement graceful degradation:
                                                                                                                                                                             3.    ```python
                                                                                                                                                                                      try:
                                                                                                                                                                                          smart_money_score = analyzer.analyze_token(token)
                                                                                                                                                                                      except ServiceUnavailable:
                                                                                                                                                                                          # Fall back to cached score or neutral (50)
                                                                                                                                                                                          smart_money_score = 50
                                                                                                                                                                                      ```
                                                                                                                                                                                   
                                                                                                                                                                                   ### Issue: Missing Module Error
                                                                                                                                                                               
                                                                                                                                                                               **Cause:** `smart_money` module not found
                                                                                                                                                                             
                                                                                                                                                                             **Solution:**
                                                                                                                                                                             1. Verify `smart_money.py` is in the repo root
                                                                                                                                                                             2. 2. Ensure correct Python path:
                                                                                                                                                                                3.    ```bash
                                                                                                                                                                                         export PYTHONPATH="${PYTHONPATH}:$(pwd)"
                                                                                                                                                                                         ```
                                                                                                                                                                                      3. Install dependencies:
                                                                                                                                                                                      4.    ```bash
                                                                                                                                                                                               pip install -r requirements.txt
                                                                                                                                                                                               ```
                                                                                                                                                                                            
                                                                                                                                                                                            ## Testing Your Integration
                                                                                                                                                                                        
                                                                                                                                                                                        ### Unit Test Example
                                                                                                                                                                                  
                                                                                                                                                                                  ```python
                                                                                                                                                                                  import pytest
                                                                                                                                                                                  from smart_money import SmartMoneyAnalyzer

                                                                                                                                                                                  @pytest.fixture
                                                                                                                                                                                  def analyzer():
                                                                                                                                                                                      return SmartMoneyAnalyzer(
                                                                                                                                                                                          api_key_1="test_key_1",
                                                                                                                                                                                          api_key_2="test_key_2"
                                                                                                                                                                                      )

                                                                                                                                                                                  def test_smart_money_score_range(analyzer):
                                                                                                                                                                                      """Score should be between 0 and 100"""
                                                                                                                                                                                      result = analyzer.analyze_token("ethereum")
                                                                                                                                                                                      assert 0 <= result["smart_money_score"] <= 100

                                                                                                                                                                                  def test_whale_sentiment_values(analyzer):
                                                                                                                                                                                      """Sentiment should be bullish, neutral, or bearish"""
                                                                                                                                                                                      result = analyzer.analyze_token("ethereum")
                                                                                                                                                                                      assert result["whale_sentiment"] in ["bullish", "neutral", "bearish"]

                                                                                                                                                                                  def test_score_components_sum_correctly(analyzer):
                                                                                                                                                                                      """Components should sum to correct final score"""
                                                                                                                                                                                      result = analyzer.analyze_token("ethereum")
                                                                                                                                                                                      calculated = (
                                                                                                                                                                                          result["details"]["whale_component"] +
                                                                                                                                                                                          result["details"]["flow_component"] +
                                                                                                                                                                                          result["details"]["professional_component"] +
                                                                                                                                                                                          result["details"]["base_score"]
                                                                                                                                                                                      )
                                                                                                                                                                                      # Allow for rounding differences
                                                                                                                                                                                      assert abs(calculated - result["smart_money_score"]) < 1
                                                                                                                                                                                  ```
                                                                                                                                                                                  
                                                                                                                                                                                  ### Integration Test
                                                                                                                                                                                
                                                                                                                                                                                ```python
                                                                                                                                                                                def test_full_multi_factor_scoring():
                                                                                                                                                                                    """Test all 4 scoring dimensions working together"""
                                                                                                                                                                                    token = "ethereum"

                                                                                                                                                                                    # Run full scoring pipeline
                                                                                                                                                                                    full_score = calculate_full_score(token, "0x...contract")

                                                                                                                                                                                    # Verify structure
                                                                                                                                                                                    assert "final_score" in full_score
                                                                                                                                                                                    assert "components" in full_score
                                                                                                                                                                                    assert all(k in full_score["components"] for k in [
                                                                                                                                                                                        "fundamentals", "technicals", "sentiment", "smart_money"
                                                                                                                                                                                    ])

                                                                                                                                                                                    # Verify scoring range
                                                                                                                                                                                    assert 0 <= full_score["final_score"] <= 100
                                                                                                                                                                                    for component_score in full_score["components"].values():
                                                                                                                                                                                        assert 0 <= component_score <= 100
                                                                                                                                                                                ```
                                                                                                                                                                                
                                                                                                                                                                                ## Next Steps
                                                                                                                                                                                
                                                                                                                                                                                After setting up Nansen integration:
                                                                                                                                                                                
                                                                                                                                                                                1. **Test with live data** - Run the integration tests
                                                                                                                                                                                2. 2. **Monitor performance** - Check API response times
                                                                                                                                                                                   3. 3. **Backtest historical** - Validate smart money signals
                                                                                                                                                                                      4. 4. **Combine factors** - Integrate with fundamentals + technicals + sentiment
                                                                                                                                                                                         5. 5. **Deploy to production** - Use environment variables for secrets
                                                                                                                                                                                           
                                                                                                                                                                                            6. ## Support & Resources
                                                                                                                                                                                           
                                                                                                                                                                                            7. - **Nansen API Docs:** https://docs.nansen.ai/
                                                                                                                                                                                               - - **GitHub Issues:** https://github.com/3apools/crypto-scanner/issues
                                                                                                                                                                                                 - - **Smart Money Module:** See `smart_money.py` for implementation details
                                                                                                                                                                                                   - - **Scoring Engine:** See `scoring_engine.py` for multi-factor integration
                                                                                                                                                                                                    
                                                                                                                                                                                                     - ## Security Notes
                                                                                                                                                                                                    
                                                                                                                                                                                                     - 🔒 **CRITICAL SECURITY PRACTICES:**
                                                                                                                                                                                                    
                                                                                                                                                                                                     - 1. **Never commit `.env`** - Always use `.gitignore`
                                                                                                                                                                                                       2. 2. **Rotate keys regularly** - Every 90 days or after team changes
                                                                                                                                                                                                          3. 3. **Use different keys per environment** - Dev, staging, production
                                                                                                                                                                                                             4. 4. **Monitor API usage** - Set up billing alerts
                                                                                                                                                                                                                5. 5. **Implement key rotation** - Without downtime using dual keys
                                                                                                                                                                                                                   6. 6. **Use secrets manager** - Kubernetes Secrets, AWS Secrets Manager, etc. for production
                                                                                                                                                                                                                     
                                                                                                                                                                                                                      7. ---
                                                                                                                                                                                                                     
                                                                                                                                                                                                                      8. **Last Updated:** January 2025
                                                                                                                                                                                                                      9. **Version:** 2.0 (Smart Money Integration)
                                                                                                                                                                                                                      10. **Status:** Production Ready ✅
