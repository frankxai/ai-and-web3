# Agent: Yield Optimizer

## Metadata
- **ID**: `yield-optimizer-v1`
- **Type**: Optimization Agent
- **Framework**: LangGraph
- **Autonomy Level**: Semi-Autonomous (suggestions only, requires approval)
- **Version**: 1.0.0

## Purpose

The Yield Optimizer analyzes current portfolio yields and identifies opportunities to improve returns by suggesting position rebalances, protocol migrations, and optimal capital allocation. All suggestions require human approval before execution.

## Capabilities

1. **Yield Analysis**
   - Calculate current APYs for all positions
   - Break down yield sources (base rate, rewards, fees)
   - Track historical yield trends

2. **Opportunity Discovery**
   - Find higher-yielding alternatives for each position
   - Consider gas costs vs yield improvement
   - Identify new protocols/pools with attractive yields

3. **Rebalancing Suggestions**
   - Generate optimal rebalancing strategies
   - Sequence multi-step transactions
   - Simulate outcomes before suggesting

4. **Cost-Benefit Analysis**
   - Calculate breakeven time for suggested moves
   - Estimate total costs (gas + slippage)
   - Project annual yield improvement

## Skills Used

- `calculate_yields` - Compute current APYs
- `suggest_rebalance` - Generate optimization strategies
- `estimate_costs` - Calculate transaction costs
- `simulate_transaction` - Test before suggesting

## Agent Architecture (LangGraph)

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class OptimizerState(TypedDict):
    positions: list
    current_yields: dict
    opportunities: list
    suggestions: list
    simulations: list
    final_recommendations: list

# Define nodes
def analyze_yields(state: OptimizerState) -> OptimizerState:
    """Node 1: Calculate current yields"""
    yields = await calculate_yields(
        positions=state["positions"],
        include_historical=True
    )
    state["current_yields"] = yields
    return state

def discover_opportunities(state: OptimizerState) -> OptimizerState:
    """Node 2: Find better yield opportunities"""
    opportunities = []

    for position in state["positions"]:
        current_yield = get_position_yield(position, state["current_yields"])

        # Search for better alternatives
        alternatives = await search_higher_yields(
            asset=position["asset"],
            position_type=position["type"],
            min_improvement=1.0  # 1% minimum improvement
        )

        for alt in alternatives:
            if alt["apy"] > current_yield + 1.0:
                opportunities.append({
                    "current": position,
                    "alternative": alt,
                    "improvement": alt["apy"] - current_yield
                })

    state["opportunities"] = sorted(
        opportunities,
        key=lambda x: x["improvement"],
        reverse=True
    )
    return state

def generate_suggestions(state: OptimizerState) -> OptimizerState:
    """Node 3: Create rebalancing suggestions"""
    suggestions = []

    for opp in state["opportunities"][:5]:  # Top 5 opportunities
        suggestion = await suggest_rebalance(
            current_positions=[opp["current"]],
            yields_data=state["current_yields"],
            risk_data={},  # Risk manager will provide this
            objective="maximize_yield"
        )

        suggestions.extend(suggestion["suggestions"])

    state["suggestions"] = suggestions
    return state

def simulate_suggestions(state: OptimizerState) -> OptimizerState:
    """Node 4: Simulate each suggestion"""
    simulations = []

    for sugg in state["suggestions"]:
        try:
            sim_result = await simulate_rebalance(sugg)
            simulations.append({
                "suggestion": sugg,
                "simulation": sim_result,
                "success": True
            })
        except Exception as e:
            simulations.append({
                "suggestion": sugg,
                "simulation": None,
                "success": False,
                "error": str(e)
            })

    state["simulations"] = simulations
    return state

def rank_recommendations(state: OptimizerState) -> OptimizerState:
    """Node 5: Rank and present final recommendations"""
    # Filter to only successful simulations
    valid_sims = [s for s in state["simulations"] if s["success"]]

    # Score each by yield improvement / cost
    for sim in valid_sims:
        sugg = sim["suggestion"]
        annual_gain = sugg["impact"]["yield_change_usd_annual"]
        cost = sugg["impact"]["estimated_cost_usd"]
        sim["score"] = annual_gain / cost if cost > 0 else annual_gain

    # Sort by score
    ranked = sorted(valid_sims, key=lambda x: x["score"], reverse=True)

    state["final_recommendations"] = ranked[:3]  # Top 3
    return state

# Build graph
workflow = StateGraph(OptimizerState)

workflow.add_node("analyze_yields", analyze_yields)
workflow.add_node("discover_opportunities", discover_opportunities)
workflow.add_node("generate_suggestions", generate_suggestions)
workflow.add_node("simulate_suggestions", simulate_suggestions)
workflow.add_node("rank_recommendations", rank_recommendations)

workflow.set_entry_point("analyze_yields")
workflow.add_edge("analyze_yields", "discover_opportunities")
workflow.add_edge("discover_opportunities", "generate_suggestions")
workflow.add_edge("generate_suggestions", "simulate_suggestions")
workflow.add_edge("simulate_suggestions", "rank_recommendations")
workflow.add_edge("rank_recommendations", END)

app = workflow.compile()
```

## Example Usage

```python
# Initialize optimizer
optimizer = YieldOptimizer()

# Run optimization
result = await optimizer.run({
    "positions": portfolio_positions,
    "current_yields": {},
    "opportunities": [],
    "suggestions": [],
    "simulations": [],
    "final_recommendations": []
})

# Review recommendations
for rec in result["final_recommendations"]:
    print(f"Recommendation: {rec['suggestion']['action_type']}")
    print(f"Expected gain: ${rec['suggestion']['impact']['yield_change_usd_annual']:.2f}/year")
    print(f"Cost: ${rec['suggestion']['impact']['estimated_cost_usd']:.2f}")
    print(f"Breakeven: {rec['suggestion']['impact']['breakeven_days']} days")
```

## Output Example

```json
{
  "final_recommendations": [
    {
      "suggestion": {
        "action_type": "move",
        "priority": "high",
        "from": {
          "protocol": "Compound",
          "asset": "USDC",
          "amount": 50000,
          "current_apy": 3.2
        },
        "to": {
          "protocol": "Aave",
          "asset": "USDC",
          "projected_apy": 4.8
        },
        "impact": {
          "yield_change_percent": 1.6,
          "yield_change_usd_annual": 800,
          "estimated_cost_usd": 15,
          "breakeven_days": 7
        }
      },
      "simulation": {
        "success": true,
        "estimated_gas": "400000",
        "projected_apy": 4.8,
        "warnings": []
      },
      "score": 53.33
    }
  ]
}
```

## Decision Logic

### When to Suggest Moving Position

```python
def should_suggest_move(current_apy, target_apy, amount_usd, gas_cost) -> bool:
    """
    Criteria for suggesting a move:
    1. Target APY at least 1% higher than current
    2. Breakeven time < 90 days
    3. Amount large enough to justify gas (>$1000)
    """
    apy_diff = target_apy - current_apy
    if apy_diff < 1.0:
        return False

    annual_gain = amount_usd * (apy_diff / 100)
    breakeven_days = (gas_cost / annual_gain) * 365

    if breakeven_days > 90:
        return False

    if amount_usd < 1000:
        return False

    return True
```

## Safety Guardrails

1. **Minimum Improvement**: 1% APY increase required
2. **Maximum Breakeven**: 90 days
3. **Simulation Required**: All suggestions pre-simulated
4. **Human Approval**: No auto-execution
5. **Gas Budget**: Respects max gas cost constraints

## Performance Metrics

- **Target Latency**: < 10 seconds
- **Opportunity Detection**: Scans 20+ protocols
- **Simulation Success Rate**: > 95%

## Integration Points

### Input
- Portfolio positions (from Portfolio Analyzer)
- Current yields (from calculate_yields)
- Constraints (gas budget, min improvement)

### Output
- Ranked recommendations
- Simulation results
- Transaction sequences

### Dependencies
- Portfolio Analyzer agent
- Ethereum MCP (for simulations)
- DeFi Protocols MCP (for yield data)

## Testing

```bash
# Test yield analysis
pytest tests/test_yield_optimizer.py::test_analyze_yields

# Test opportunity discovery
pytest tests/test_yield_optimizer.py::test_find_opportunities

# Test simulation
pytest tests/test_yield_optimizer.py::test_simulate_suggestions
```

## Monitoring

- Track suggestions accepted vs rejected by users
- Monitor actual yield improvements post-rebalance
- Alert on simulation failures

## Future Enhancements

- [ ] Multi-hop strategies (A→B→C for better yields)
- [ ] Tax-loss harvesting awareness
- [ ] Optimal timing (gas prices, market conditions)
- [ ] Backtesting on historical data
- [ ] ML-powered yield prediction
