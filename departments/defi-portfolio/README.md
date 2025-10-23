# DeFi Portfolio Agent Department

An intelligent multi-agent system for monitoring, analyzing, and optimizing DeFi portfolios across multiple protocols.

## Overview

The DeFi Portfolio Department consists of specialized agents that work together to:
- Track positions across Uniswap, Aave, Compound, Lido, and more
- Calculate real-time yields and APYs
- Analyze risk exposure and concentration
- Suggest optimal rebalancing strategies
- Generate portfolio performance reports

## Architecture

```mermaid
flowchart TB
    User[User] --> API[FastAPI Backend]
    API --> PA[Portfolio Analyzer Agent]
    API --> YO[Yield Optimizer Agent]
    API --> RM[Risk Manager Agent]

    PA --> QP[Query Positions Skill]
    PA --> CV[Calculate Value Skill]

    YO --> CY[Calculate Yields Skill]
    YO --> SR[Suggest Rebalance Skill]

    RM --> AR[Analyze Risk Skill]
    RM --> VL[Validate Limits Skill]

    QP --> MCP[MCP Servers]
    CY --> MCP
    AR --> MCP

    MCP --> ETH[Ethereum RPC]
    MCP --> TG[The Graph]
    MCP --> DeFi[DeFi Protocol APIs]
```

## Agents

### 1. Portfolio Analyzer Agent
**Purpose**: Read-only analysis of current positions
- Queries positions across all supported protocols
- Calculates total portfolio value in USD
- Tracks historical performance
- Generates visual reports

**Skills Used**:
- `query_positions` - Fetch positions from protocols
- `calculate_value` - Convert to USD values
- `track_history` - Store snapshots over time

### 2. Yield Optimizer Agent
**Purpose**: Find better yield opportunities
- Monitors current APYs across protocols
- Identifies higher-yield alternatives
- Suggests rebalancing strategies
- Estimates gas costs vs yield gains

**Skills Used**:
- `calculate_yields` - Get current APYs
- `suggest_rebalance` - Propose optimal moves
- `estimate_costs` - Calculate gas + slippage

### 3. Risk Manager Agent
**Purpose**: Ensure portfolio safety
- Analyzes concentration risk
- Checks protocol health scores
- Validates proposed actions against policies
- Alerts on anomalies

**Skills Used**:
- `analyze_risk` - Calculate risk metrics
- `validate_limits` - Check policy compliance
- `monitor_health` - Track protocol TVL/audits

## Skills Reference

All skills are defined in `skills/*.skill.md`:
- `query_positions.skill.md` - Fetch balances from protocols
- `calculate_yields.skill.md` - Compute APYs and returns
- `analyze_risk.skill.md` - Risk scoring and concentration
- `suggest_rebalance.skill.md` - Optimization strategies
- `estimate_costs.skill.md` - Gas and fee estimation
- `track_history.skill.md` - Time-series data management

## Required APIs & MCP Servers

### Core MCP Servers (Required)

1. **mcp-ethereum** - Ethereum RPC operations
   - Read balances
   - Query contract state
   - Simulate transactions
   - Configuration: `mcp-servers/ethereum.mcp.json`

2. **mcp-thegraph** - Historical data queries
   - Uniswap V3 positions
   - Aave lending positions
   - Compound supply/borrow
   - Configuration: `mcp-servers/thegraph.mcp.json`

3. **mcp-defi-protocols** - Protocol-specific APIs
   - Direct protocol queries
   - APY calculations
   - Health factors
   - Configuration: `mcp-servers/defi_protocols.mcp.json`

### External APIs (Required)

1. **Ethereum RPC Provider** (Choose one)
   - Alchemy: `https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY`
   - Infura: `https://mainnet.infura.io/v3/YOUR_KEY`
   - QuickNode: `https://YOUR_ENDPOINT.quiknode.pro/YOUR_KEY`

2. **The Graph API**
   - Hosted Service: `https://api.thegraph.com/subgraphs/name/...`
   - Decentralized Network: Query specific subgraphs
   - Required subgraphs:
     - `uniswap/uniswap-v3`
     - `aave/protocol-v3`
     - `compound-finance/compound-v3`

3. **Price Feeds** (Choose one)
   - CoinGecko API: `https://api.coingecko.com/api/v3`
   - CoinMarketCap API: `https://pro-api.coinmarketcap.com/v1`
   - Chainlink Price Feeds (on-chain, free)

### Optional APIs (Enhanced Features)

4. **DeFi Llama API** - TVL and protocol metrics
   - `https://api.llama.fi/protocol/{protocol}`
   - No auth required, rate-limited

5. **Tenderly API** - Transaction simulation
   - Fork networks for testing
   - Simulate rebalancing before execution

6. **Etherscan API** - Contract verification and history
   - `https://api.etherscan.io/api`

## Deployment Options

### Option 1: Local Development (Recommended for Testing)

**Prerequisites**:
- Node.js 18+
- Python 3.10+
- Docker & Docker Compose
- pnpm or npm

**Setup**:
```bash
# Clone and navigate
cd departments/defi-portfolio

# Copy environment template
cp .env.example .env
# Edit .env with your API keys

# Install dependencies
pnpm install
pip install -r requirements.txt

# Start local services (PostgreSQL, Redis)
docker-compose up -d

# Start MCP servers
node mcp-servers/ethereum/server.js &
node mcp-servers/thegraph/server.js &

# Start FastAPI backend
uvicorn api.main:app --reload --port 8000

# Start Next.js frontend (optional)
cd ui && pnpm dev
```

**Access**:
- API: `http://localhost:8000`
- UI: `http://localhost:3000`
- API Docs: `http://localhost:8000/docs`

### Option 2: Docker Compose (Recommended for Production)

**Single command deployment**:
```bash
# Build and start all services
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

**Services included**:
- FastAPI backend (port 8000)
- PostgreSQL database (port 5432)
- Redis cache (port 6379)
- MCP server cluster
- Nginx reverse proxy (port 80)
- Optional: Next.js UI (port 3000)

**Access**:
- API: `http://localhost/api`
- UI: `http://localhost`
- Health: `http://localhost/api/health`

### Option 3: Vercel (Frontend) + Railway (Backend)

**Frontend (Next.js UI) on Vercel**:
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from ui/ directory
cd ui
vercel --prod

# Configure environment variables in Vercel dashboard:
# NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

**Backend (FastAPI) on Railway**:
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and init
railway login
railway init

# Deploy from root
railway up

# Add environment variables via Railway dashboard
```

**Configuration**:
- Edit `deploy/vercel.json` for Vercel settings
- Edit `deploy/railway.json` for Railway settings
- Set API keys in respective dashboards

### Option 4: Cloud Deployment (AWS/GCP/Azure)

**AWS ECS + RDS**:
```bash
# Use provided Terraform configs
cd deploy/terraform/aws
terraform init
terraform plan
terraform apply

# Outputs ECS cluster, RDS endpoint, ALB DNS
```

**Google Cloud Run + Cloud SQL**:
```bash
# Deploy with gcloud
cd deploy/gcp
./deploy.sh

# Follow prompts for project ID, region
```

**Azure Container Instances + PostgreSQL**:
```bash
# Deploy with Azure CLI
cd deploy/azure
./deploy.sh

# Provide subscription ID and resource group
```

### Option 5: Kubernetes (Production Scale)

**Deploy to any K8s cluster**:
```bash
# Apply manifests
kubectl apply -f deploy/k8s/

# Check status
kubectl get pods -n defi-portfolio

# Access via ingress
kubectl get ingress -n defi-portfolio
```

**Includes**:
- API deployment (3 replicas)
- PostgreSQL StatefulSet
- Redis deployment
- HPA for auto-scaling
- Ingress with TLS
- ConfigMaps and Secrets

## Environment Variables

Create `.env` file with the following:

```bash
# Ethereum RPC
ETHEREUM_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
ETHEREUM_RPC_WSS=wss://eth-mainnet.g.alchemy.com/v2/YOUR_KEY

# The Graph
THEGRAPH_API_KEY=YOUR_THEGRAPH_KEY

# Price Feeds
COINGECKO_API_KEY=YOUR_COINGECKO_KEY  # Optional, for higher rate limits

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/defi_portfolio

# Redis Cache
REDIS_URL=redis://localhost:6379/0

# MCP Server Endpoints
MCP_ETHEREUM_URL=http://localhost:3001
MCP_THEGRAPH_URL=http://localhost:3002
MCP_DEFI_PROTOCOLS_URL=http://localhost:3003

# API Configuration
API_PORT=8000
API_HOST=0.0.0.0
LOG_LEVEL=info

# Security
JWT_SECRET=your-secret-key-here
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com

# Policies
MAX_PORTFOLIO_VALUE_USD=1000000
MAX_SINGLE_POSITION_PERCENT=25
MIN_PROTOCOL_TVL_USD=100000000
REQUIRE_HUMAN_APPROVAL=true

# Optional: Monitoring
SENTRY_DSN=your-sentry-dsn
PROMETHEUS_PORT=9090
```

## Quick Start Examples

### Example 1: Get Portfolio Summary
```bash
# Using curl
curl http://localhost:8000/api/portfolio/summary \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"address": "0x1234...5678"}'

# Response
{
  "total_value_usd": 125430.50,
  "positions": [
    {
      "protocol": "Aave",
      "type": "supply",
      "asset": "USDC",
      "amount": 50000,
      "value_usd": 50000,
      "apy": 4.5
    },
    {
      "protocol": "Uniswap V3",
      "type": "liquidity",
      "pool": "USDC/ETH 0.3%",
      "value_usd": 75430.50,
      "apy": 12.3
    }
  ]
}
```

### Example 2: Get Yield Optimization Suggestions
```bash
curl http://localhost:8000/api/optimize/yields \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "address": "0x1234...5678",
    "risk_tolerance": "medium"
  }'

# Response
{
  "suggestions": [
    {
      "action": "move",
      "from": {
        "protocol": "Compound",
        "asset": "USDC",
        "current_apy": 3.2
      },
      "to": {
        "protocol": "Aave",
        "asset": "USDC",
        "projected_apy": 4.8
      },
      "impact": {
        "apy_increase": 1.6,
        "annual_gain_usd": 800,
        "estimated_gas_usd": 15
      }
    }
  ]
}
```

### Example 3: Risk Analysis
```bash
curl http://localhost:8000/api/risk/analyze \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"address": "0x1234...5678"}'

# Response
{
  "risk_score": 6.5,
  "risk_level": "medium",
  "factors": [
    {
      "type": "concentration",
      "severity": "medium",
      "message": "75% of portfolio in single protocol (Aave)",
      "recommendation": "Diversify across 3+ protocols"
    },
    {
      "type": "protocol_risk",
      "severity": "low",
      "message": "All protocols have strong audit history"
    }
  ]
}
```

## Development Workflow

### Adding a New Protocol

1. **Define skill** in `skills/query_{protocol}.skill.md`
2. **Implement tool** in `tools/{protocol}.py`
3. **Update MCP config** in `mcp-servers/defi_protocols.mcp.json`
4. **Add tests** in `tests/test_{protocol}.py`
5. **Update documentation** in this README

### Testing

```bash
# Run all tests
pnpm test

# Run specific test suite
pytest tests/test_uniswap.py -v

# Run integration tests (requires local node)
pytest tests/integration/ -v

# Run MCP server tests
node mcp-servers/ethereum/test.js
```

### Monitoring

**Access dashboards**:
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001` (admin/admin)
- Logs: `docker-compose logs -f api`

**Key metrics**:
- API request latency
- RPC call success rate
- Portfolio query duration
- Cache hit rate

## Security Considerations

1. **Read-Only by Default**: All queries are read-only unless explicitly enabled
2. **Human Approval**: Rebalancing suggestions require manual approval
3. **Policy Enforcement**: All actions checked against `config/policies.yaml`
4. **Rate Limiting**: API and RPC calls are rate-limited
5. **Secret Management**: Never commit API keys; use environment variables
6. **Audit Logging**: All suggestions and actions are logged

## Troubleshooting

### Common Issues

**RPC rate limits**:
```bash
# Use multiple RPC providers with fallback
ETHEREUM_RPC_URLS=url1,url2,url3
```

**Database connection errors**:
```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres
python scripts/init_db.py
```

**MCP server not responding**:
```bash
# Check logs
docker-compose logs mcp-ethereum

# Restart specific service
docker-compose restart mcp-ethereum
```

## Roadmap

- [x] Core portfolio querying (Uniswap, Aave, Compound)
- [x] Yield optimization suggestions
- [x] Risk analysis engine
- [ ] Support for Lido, Curve, Balancer
- [ ] Automated rebalancing (with approval)
- [ ] Multi-chain support (Polygon, Arbitrum, Optimism)
- [ ] Historical performance tracking
- [ ] Telegram/Discord bot interface
- [ ] Mobile app (React Native)

## Contributing

See main repo's `CONTRIBUTING.md` for guidelines.

## License

MIT - See main repo's LICENSE file.

## Support

- Issues: https://github.com/frankxai/ai-and-web3/issues
- Discord: [Link to community]
- Documentation: https://frankxai.github.io/ai-and-web3/
