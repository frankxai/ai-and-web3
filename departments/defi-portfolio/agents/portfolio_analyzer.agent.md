# Agent: Portfolio Analyzer

## Metadata
- **ID**: `portfolio-analyzer-v1`
- **Type**: Analytical Agent
- **Framework**: LangGraph
- **Autonomy Level**: Supervised (read-only)
- **Version**: 1.0.0

## Purpose

The Portfolio Analyzer is a read-only agent that monitors DeFi portfolios, tracks positions across protocols, calculates total value, and generates comprehensive reports. It serves as the foundation agent that other specialized agents (Yield Optimizer, Risk Manager) build upon.

## Capabilities

1. **Position Tracking**
   - Query positions across Uniswap, Aave, Compound, Lido, Curve, Balancer
   - Aggregate holdings by protocol, asset, position type
   - Track historical position changes

2. **Valuation**
   - Convert all positions to USD using current prices
   - Calculate total portfolio value
   - Track value changes over time

3. **Reporting**
   - Generate daily/weekly/monthly portfolio summaries
   - Create visualizations (protocol breakdown, asset allocation)
   - Export data for external analysis

4. **Alerting**
   - Notify on significant position changes
   - Alert on unusual activity
   - Track milestones (portfolio value thresholds)

## Skills Used

- `query_positions` - Fetch current positions
- `calculate_value` - Convert to USD
- `track_history` - Store snapshots
- `generate_report` - Create summaries

## Agent Architecture (LangGraph)

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator

class AnalyzerState(TypedDict):
    address: str
    positions: list
    total_value_usd: float
    history: list
    report: dict
    errors: Annotated[Sequence[str], operator.add]

# Define nodes
def fetch_positions(state: AnalyzerState) -> AnalyzerState:
    """Node 1: Fetch all positions"""
    try:
        positions = await query_positions(
            address=state["address"],
            protocols=["uniswap", "aave", "compound", "lido"]
        )
        state["positions"] = positions["positions"]
    except Exception as e:
        state["errors"].append(f"Failed to fetch positions: {e}")
    return state

def calculate_values(state: AnalyzerState) -> AnalyzerState:
    """Node 2: Calculate USD values"""
    try:
        total_value = 0
        for pos in state["positions"]:
            # Get current price
            price = await get_token_price(pos["asset"])
            pos["value_usd"] = pos["amount"] * price
            total_value += pos["value_usd"]

        state["total_value_usd"] = total_value
    except Exception as e:
        state["errors"].append(f"Failed to calculate values: {e}")
    return state

def fetch_history(state: AnalyzerState) -> AnalyzerState:
    """Node 3: Get historical data"""
    try:
        history = await get_position_history(
            address=state["address"],
            days=30
        )
        state["history"] = history
    except Exception as e:
        state["errors"].append(f"Failed to fetch history: {e}")
    return state

def generate_report(state: AnalyzerState) -> AnalyzerState:
    """Node 4: Generate comprehensive report"""
    report = {
        "address": state["address"],
        "timestamp": datetime.utcnow().isoformat(),
        "total_value_usd": state["total_value_usd"],
        "position_count": len(state["positions"]),
        "positions": state["positions"],
        "breakdown": {
            "by_protocol": aggregate_by_protocol(state["positions"]),
            "by_asset": aggregate_by_asset(state["positions"]),
            "by_type": aggregate_by_type(state["positions"])
        },
        "history": state["history"]
    }
    state["report"] = report
    return state

# Build graph
workflow = StateGraph(AnalyzerState)

workflow.add_node("fetch_positions", fetch_positions)
workflow.add_node("calculate_values", calculate_values)
workflow.add_node("fetch_history", fetch_history)
workflow.add_node("generate_report", generate_report)

workflow.set_entry_point("fetch_positions")
workflow.add_edge("fetch_positions", "calculate_values")
workflow.add_edge("calculate_values", "fetch_history")
workflow.add_edge("fetch_history", "generate_report")
workflow.add_edge("generate_report", END)

app = workflow.compile()
```

## Example Usage

```python
# Initialize analyzer
analyzer = PortfolioAnalyzer()

# Run analysis
result = await analyzer.run({
    "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    "positions": [],
    "total_value_usd": 0,
    "history": [],
    "report": {},
    "errors": []
})

# Access report
print(result["report"])
```

## Output Example

```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "timestamp": "2025-01-15T10:30:00Z",
  "total_value_usd": 125430.50,
  "position_count": 4,
  "positions": [...],
  "breakdown": {
    "by_protocol": {
      "Uniswap V3": 75430.50,
      "Aave V3": 50000.00
    },
    "by_asset": {
      "USDC": 50000.00,
      "ETH": 40000.00,
      "stETH": 35430.50
    },
    "by_type": {
      "liquidity": 75430.50,
      "lending": 50000.00
    }
  },
  "history": [
    {"date": "2025-01-14", "value_usd": 123500},
    {"date": "2025-01-13", "value_usd": 122000}
  ]
}
```

## Performance Metrics

- **Target Latency**: < 3 seconds
- **Success Rate**: > 99%
- **Cache Strategy**: 5-minute cache for positions
- **Rate Limits**: Respects all RPC/API limits

## Error Handling

- Graceful degradation (partial results if some protocols fail)
- Retry logic with exponential backoff
- Detailed error logging
- User-friendly error messages

## Security

- Read-only operations (no transactions)
- No private key handling
- Rate limiting to prevent abuse
- Input validation on all addresses

## Integration Points

### Input
- Wallet address (Ethereum)
- Optional: protocol filter, time range

### Output
- Portfolio report (JSON)
- Historical data (time series)
- Alerts (if configured)

### Dependencies
- Ethereum MCP server
- The Graph MCP server
- Price feed API (CoinGecko/Chainlink)

## Testing

```bash
# Unit tests
pytest tests/test_portfolio_analyzer.py

# Integration test (requires test data)
pytest tests/integration/test_analyzer_e2e.py

# Load test
pytest tests/load/test_analyzer_load.py --users 100
```

## Deployment

```bash
# As standalone service
uvicorn agents.portfolio_analyzer:app --port 8001

# As part of department
docker-compose up portfolio-analyzer
```

## Monitoring

- Prometheus metrics exposed on `/metrics`
- Key metrics:
  - `portfolio_analysis_duration_seconds`
  - `position_fetch_errors_total`
  - `cache_hit_rate`

## Future Enhancements

- [ ] Multi-chain support (Polygon, Arbitrum, Optimism)
- [ ] NFT position tracking
- [ ] Advanced analytics (Sharpe ratio, drawdown)
- [ ] ML-powered anomaly detection
- [ ] Custom alert rules
