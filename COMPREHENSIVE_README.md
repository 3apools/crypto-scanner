# Crypto Scanner & Investor Assistant

**Production-grade cryptocurrency analysis system** with 0-100 grading, trading signals, and multi-factor scoring across fundamentals, technicals, sentiment, and smart money metrics.

## 🎯 System Architecture

### Core Components
- **Scoring Engine**: Multi-factor analysis (25% each: fundamentals, technicals, sentiment, smart money)
- - **Chat Interface**: Natural language processing with intent detection and parameter extraction
  - - **Data Layer**: 6 API clients (CoinGecko, TAAPI, LunarCrush, Dune, Nansen, GitHub)
    - - **FastAPI Server**: RESTful endpoints for integration
      - - **Configuration Management**: Environment-based, type-safe configuration
       
        - ### Directory Structure
        - ```
          crypto-scanner/
          ├── main.py                    # FastAPI server & endpoints
          ├── scoring_engine.py          # Multi-factor scoring logic
          ├── chat_handler.py            # NLP & intent detection
          ├── data_layer.py              # API client aggregation
          ├── config.py                  # Environment configuration
          ├── tests.py                   # Comprehensive unit tests
          ├── scoring_rules.json         # Parametrized rules & thresholds
          ├── requirements.txt           # Python dependencies
          ├── .env.example               # Environment template
          ├── Dockerfile                 # Container definition
          ├── docker-compose.yml         # Multi-service orchestration
          └── README.md                  # This file
          ```

          ## 🚀 Quick Start

          ### Prerequisites
          - Python 3.11+
          - - Docker & Docker Compose (optional)
            - - API Keys: CoinGecko, TAAPI, LunarCrush, Dune, GitHub
             
              - ### Installation
             
              - 1. **Clone repository**
                2.    ```bash
                         git clone https://github.com/3apools/crypto-scanner.git
                         cd crypto-scanner
                         ```

                      2. **Setup environment**
                      3.    ```bash
                               cp .env.example .env
                               # Edit .env with your API keys
                               ```

                            3. **Install dependencies**
                            4.    ```bash
                                     pip install -r requirements.txt
                                     ```

                                  4. **Run server**
                                  5.    ```bash
                                           python main.py
                                           # API available at http://localhost:8000
                                           ```

                                        ### Docker Deployment

                                    ```bash
                                    # Single container
                                    docker build -t crypto-scanner .
                                    docker run -p 8000:8000 --env-file .env crypto-scanner

                                    # Multi-service with Redis
                                    docker-compose up
                                    ```

                                    ## 📊 Scoring Methodology

                              ### Four Dimensions (25% weight each)

                        **Fundamentals (25%)**
                  - Token economics (supply, burn, vesting)
                  - - Development activity (GitHub commits, velocity)
                    - - On-chain metrics (active addresses, transaction volume)
                     
                      - **Technicals (25%)**
                      - - Price action (support/resistance, trend strength)
                        - - Volume patterns (conviction, liquidity)
                          - - Momentum indicators (RSI, MACD, moving averages)
                           
                            - **Sentiment (25%)**
                            - - Social media mentions and sentiment
                              - - News sentiment analysis
                                - - Community engagement metrics
                                 
                                  - **Smart Money (25%)**
                                  - - Whale accumulation patterns
                                    - - Exchange flows (inflows vs outflows)
                                      - - Professional trader positioning
                                       
                                        - ### Signal Thresholds
                                        - - **Strong Buy**: 80+ score
                                          - - **Buy**: 65-79 score
                                            - - **Hold**: 50-64 score
                                              - - **Sell**: 35-49 score
                                                - - **Strong Sell**: 0-34 score
                                                 
                                                  - ### Edge Cases Handled
                                                  - - **Stablecoins**: Skip technicals, max 60 score, focus on reserves
                                                    - - **New Tokens (<30d)**: Reduced confidence (<40%), skip historical metrics
                                                      - - **Flash Crashes**: Ignore >15% 1h moves, use VWAP not spot
                                                        - - **Low Liquidity**: <$100K volume flagged, -20% score penalty
                                                          - - **Dynamic Rebalancing**: Bull/bear mode weights based on BTC dominance
                                                           
                                                            - ## 💬 Chat Interface Examples
                                                           
                                                            - ### Token Analysis
                                                            - ```
                                                              User: "Score BTC"
                                                              Bot: 📊 **BTC Analysis**
                                                                   Overall Score: 76/100
                                                                   - Fundamentals: 75/100
                                                                   - Technicals: 78/100
                                                                   - Sentiment: 72/100
                                                                   - Smart Money: 80/100
                                                                   Signal: BUY
                                                                   Confidence: 76%
                                                              ```

                                                              ### Comparison
                                                              ```
                                                              User: "Compare ETH vs SOL 1d"
                                                              Bot: 📈 **Token Comparison**
                                                                   ETH: Score 72, Signal: BUY
                                                                   SOL: Score 68, Signal: HOLD
                                                              ```

                                                              ### Market Data
                                                              ```
                                                              User: "Market overview"
                                                              Bot: 🌍 **Market Overview**
                                                                   BTC Dominance: 45.2%
                                                                   Total Market Cap: $1.2T
                                                                   Sentiment: NEUTRAL
                                                                   Trend: Sideways
                                                              ```

                                                              ## 🔌 API Endpoints

                                                              ### Token Analysis
                                                              - `GET /api/v1/score/{token}` - Score individual token
                                                              - - `GET /api/v1/score/{token}?time_period=1d` - Time-specific analysis
                                                               
                                                                - ### Market Data
                                                                - - `GET /api/v1/market/overview` - Overall market conditions
                                                                  - - `GET /api/v1/market/top/gainers?limit=10` - Top performers
                                                                    - - `GET /api/v1/market/top/losers?limit=10` - Worst performers
                                                                     
                                                                      - ### Portfolio Management
                                                                      - - `POST /api/v1/portfolio/analyze` - Analyze token portfolio
                                                                        - - `POST /api/v1/alert/create` - Create price alert
                                                                         
                                                                          - ### Chat Interface
                                                                          - - `POST /api/v1/chat` - Natural language queries
                                                                           
                                                                            - ### Health
                                                                            - - `GET /health` - Basic health check
                                                                              - - `GET /api/v1/health/detailed` - Component status
                                                                               
                                                                                - ## 🧪 Testing
                                                                               
                                                                                - ```bash
                                                                                  # Run all tests
                                                                                  pytest tests.py -v

                                                                                  # Specific test class
                                                                                  pytest tests.py::TestChatHandler -v

                                                                                  # With coverage
                                                                                  pytest --cov=. tests.py
                                                                                  ```

                                                                                  ## 🔐 Security & Configuration

                                                                                  ### Environment Variables (Required)
                                                                                  ```
                                                                                  COINGECKO_API_KEY=xxx
                                                                                  TAAPI_API_KEY=xxx
                                                                                  LUNARCRUSH_API_KEY=xxx
                                                                                  DUNE_API_KEY=xxx
                                                                                  GITHUB_TOKEN=xxx
                                                                                  ```

                                                                                  ### Optional Configuration
                                                                                  ```
                                                                                  API_HOST=0.0.0.0
                                                                                  API_PORT=8000
                                                                                  DEBUG=False
                                                                                  CACHE_ENABLED=True
                                                                                  CACHE_TTL_SECONDS=300
                                                                                  LOG_LEVEL=INFO
                                                                                  ```

                                                                                  ### Best Practices
                                                                                  - Never hardcode API keys - use environment variables
                                                                                  - - All configuration loaded from `.env`
                                                                                    - - All thresholds parametrized in `scoring_rules.json`
                                                                                      - - Type validation with Pydantic models
                                                                                        - - No magic numbers in code
                                                                                         
                                                                                          - ## 📈 Data Sources
                                                                                         
                                                                                          - | API | Purpose | Status |
                                                                                          - |-----|---------|--------|
                                                                                          - | **CoinGecko** | Price, market cap, volume | Mock |
                                                                                          - | **TAAPI** | Technical indicators | Mock |
                                                                                          - | **LunarCrush** | Sentiment, social metrics | Mock |
                                                                                          - | **Dune Analytics** | On-chain data | Mock |
                                                                                          - | **Nansen** | Smart money flows | Mock |
                                                                                          - | **GitHub** | Development activity | Mock |
                                                                                         
                                                                                          - *Phase 1 uses mock data. Phase 2 will integrate real APIs.*
                                                                                         
                                                                                          - ## 🔄 Workflow
                                                                                         
                                                                                          - ### Phase 1: Foundation (✅ COMPLETE)
                                                                                          - - System architecture & design
                                                                                            - - Pydantic schemas & interfaces
                                                                                              - - Mock data implementations
                                                                                                - - Comprehensive documentation
                                                                                                 
                                                                                                  - ### Phase 2: Integration (NEXT)
                                                                                                  - - Connect real APIs (swap mocks for live)
                                                                                                    - - Implement caching (Redis/SQLite)
                                                                                                      - - Add portfolio tracking
                                                                                                        - - Create alert system
                                                                                                          - - Backtesting module
                                                                                                           
                                                                                                            - ### Phase 3: Refinement (FUTURE)
                                                                                                            - - ML-based signal generation
                                                                                                              - - Advanced portfolio analytics
                                                                                                                - - Risk metrics & drawdown analysis
                                                                                                                  - - Real-time monitoring dashboard
                                                                                                                    - - Mobile app support
                                                                                                                     
                                                                                                                      - ## 📝 Code Quality
                                                                                                                     
                                                                                                                      - - **Type Safety**: 100% Pydantic validation
                                                                                                                        - - **Testing**: Unit tests for all components
                                                                                                                          - - **Documentation**: Comprehensive docstrings
                                                                                                                            - - **Separation of Concerns**: 6-layer architecture
                                                                                                                              - - **Extensibility**: Easy config changes without code rewrites
                                                                                                                                - - **Production Ready**: Error handling, logging, health checks
                                                                                                                                 
                                                                                                                                  - ## 🤝 Contributing
                                                                                                                                 
                                                                                                                                  - 1. Create feature branch: `git checkout -b feature/description`
                                                                                                                                    2. 2. Commit changes: `git commit -am 'Add feature'`
                                                                                                                                       3. 3. Push to GitHub: `git push origin feature/description`
                                                                                                                                          4. 4. Submit pull request
                                                                                                                                            
                                                                                                                                             5. ## 📄 License
                                                                                                                                            
                                                                                                                                             6. MIT License - See LICENSE file for details
                                                                                                                                            
                                                                                                                                             7. ## 👨‍💻 Author
                                                                                                                                            
                                                                                                                                             8. Built with 🚀 for crypto investors who demand production-grade analysis.
                                                                                                                                            
                                                                                                                                             9. ---
                                                                                                                                            
                                                                                                                                             10. **Ready to use.** Clone, configure API keys, and start analyzing!
                                                                                                                                             11. 
