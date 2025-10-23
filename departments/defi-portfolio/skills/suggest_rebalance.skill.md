# Skill: Suggest Rebalance

## Metadata
- **ID**: `defi.suggest_rebalance`
- **Version**: 1.0.0
- **Category**: Optimization
- **Risk Level**: Medium (Generates transaction suggestions)
- **Required MCP**: ethereum, defi-protocols
- **Requires Approval**: Yes

## Description

Analyzes current portfolio and suggests optimal rebalancing strategies to improve yields, reduce risk, or achieve target allocation. All suggestions require human approval before execution.

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "current_positions": {
      "type": "array",
      "description": "Current portfolio positions"
    },
    "yields_data": {
      "type": "object",
      "description": "Output from calculate_yields skill"
    },
    "risk_data": {
      "type": "object",
      "description": "Output from analyze_risk skill"
    },
    "objective": {
      "type": "string",
      "enum": ["maximize_yield", "minimize_risk", "balanced"],
      "default": "balanced"
    },
    "constraints": {
      "type": "object",
      "properties": {
        "max_gas_usd": {"type": "number", "default": 100},
        "min_yield_improvement_percent": {"type": "number", "default": 1.0},
        "max_slippage_percent": {"type": "number", "default": 0.5},
        "preserve_protocols": {
          "type": "array",
          "description": "Protocols to keep positions in"
        }
      }
    }
  },
  "required": ["current_positions", "yields_data", "risk_data"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "suggestions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "action_type": {
            "type": "string",
            "enum": ["move", "add", "remove", "adjust"]
          },
          "priority": {
            "type": "string",
            "enum": ["high", "medium", "low"]
          },
          "from": {"type": "object", "nullable": true},
          "to": {"type": "object"},
          "impact": {
            "type": "object",
            "properties": {
              "yield_change_percent": {"type": "number"},
              "yield_change_usd_annual": {"type": "number"},
              "risk_change": {"type": "number"},
              "estimated_cost_usd": {"type": "number"},
              "breakeven_days": {"type": "number"}
            }
          },
          "steps": {
            "type": "array",
            "description": "Transaction sequence required"
          }
        }
      }
    },
    "summary": {
      "type": "object",
      "properties": {
        "total_suggestions": {"type": "integer"},
        "projected_yield_improvement": {"type": "number"},
        "projected_risk_reduction": {"type": "number"},
        "total_estimated_cost": {"type": "number"}
      }
    }
  }
}
```

## Rebalancing Strategies

### 1. Yield Optimization

```python
def find_yield_opportunities(current_positions, yields_data) -> list:
    """
    Find positions that can be moved to higher-yielding alternatives.

    Strategy:
    1. Identify low-yield positions (below portfolio average)
    2. Find similar positions with higher yields
    3. Calculate net benefit after gas costs
    """
    suggestions = []
    avg_apy = yields_data["summary"]["weighted_avg_apy"]

    for pos in current_positions:
        pos_yield = next((y for y in yields_data["yields"] if y["asset"] == pos["asset"]), None)

        if pos_yield and pos_yield["current_apy"] < avg_apy - 1.0:
            # Find better alternatives
            alternatives = await find_better_yields(pos["asset"], pos_yield["current_apy"])

            for alt in alternatives:
                # Calculate costs
                gas_cost = await estimate_move_cost(pos, alt)

                # Calculate benefit
                apy_diff = alt["apy"] - pos_yield["current_apy"]
                annual_gain = pos["value_usd"] * (apy_diff / 100)

                # Only suggest if ROI positive
                if annual_gain > gas_cost * 4:  # 3-month breakeven max
                    suggestions.append({
                        "action_type": "move",
                        "priority": "high" if apy_diff > 3 else "medium",
                        "from": {
                            "protocol": pos["protocol"],
                            "asset": pos["asset"],
                            "current_apy": pos_yield["current_apy"]
                        },
                        "to": {
                            "protocol": alt["protocol"],
                            "asset": alt["asset"],
                            "projected_apy": alt["apy"]
                        },
                        "impact": {
                            "yield_change_percent": apy_diff,
                            "yield_change_usd_annual": annual_gain,
                            "estimated_cost_usd": gas_cost,
                            "breakeven_days": int(gas_cost / (annual_gain / 365))
                        }
                    })

    return suggestions
```

### 2. Risk Reduction

```python
def suggest_risk_reduction(positions, risk_data) -> list:
    """
    Suggest changes to reduce portfolio risk.

    Strategies:
    - Reduce concentration
    - Move to safer protocols
    - Increase stablecoin allocation
    - Reduce IL exposure
    """
    suggestions = []

    # Address concentration risk
    for risk_factor in risk_data["risk_factors"]:
        if risk_factor["category"] == "concentration" and risk_factor["severity"] in ["medium", "high"]:
            # Find which protocol is over-concentrated
            protocol_concentrations = calculate_protocol_concentration(positions)

            for protocol, percent in protocol_concentrations.items():
                if percent > 50:
                    # Suggest diversification
                    amount_to_move = sum(p["value_usd"] for p in positions if p["protocol"] == protocol) * 0.3

                    suggestions.append({
                        "action_type": "move",
                        "priority": "high",
                        "from": {
                            "protocol": protocol,
                            "amount_usd": amount_to_move
                        },
                        "to": {
                            "suggestion": "Diversify across 2-3 other major protocols"
                        },
                        "impact": {
                            "risk_change": -2.0,  # Reduces risk score
                            "yield_change_percent": 0,  # Neutral
                            "estimated_cost_usd": amount_to_move * 0.003  # ~0.3% in gas
                        }
                    })

    # Address protocol risk
    for risk_factor in risk_data["risk_factors"]:
        if risk_factor["category"] == "protocol_risk" and risk_factor["severity"] == "high":
            # Suggest moving to safer alternatives
            risky_positions = [p for p in positions if get_protocol_score(p["protocol"]) < 7]

            for pos in risky_positions:
                safer_alternatives = get_safer_protocols(pos["asset"])

                suggestions.append({
                    "action_type": "move",
                    "priority": "medium",
                    "from": {
                        "protocol": pos["protocol"],
                        "asset": pos["asset"],
                        "safety_score": get_protocol_score(pos["protocol"])
                    },
                    "to": {
                        "alternatives": safer_alternatives
                    },
                    "impact": {
                        "risk_change": -1.5,
                        "yield_change_percent": -0.5,  # Might sacrifice some yield
                        "estimated_cost_usd": pos["value_usd"] * 0.002
                    }
                })

    return suggestions
```

### 3. Balanced Approach

```python
def suggest_balanced_rebalance(positions, yields_data, risk_data) -> list:
    """
    Balance between yield optimization and risk reduction.

    Pareto optimization: maximize yield / risk ratio.
    """
    yield_suggestions = find_yield_opportunities(positions, yields_data)
    risk_suggestions = suggest_risk_reduction(positions, risk_data)

    # Score each suggestion by yield/risk improvement
    all_suggestions = yield_suggestions + risk_suggestions

    for sugg in all_suggestions:
        yield_score = sugg["impact"].get("yield_change_percent", 0)
        risk_score = abs(sugg["impact"].get("risk_change", 0))

        # Pareto score
        sugg["pareto_score"] = (yield_score * 0.6) + (risk_score * 0.4)

    # Sort by pareto score
    all_suggestions.sort(key=lambda x: x.get("pareto_score", 0), reverse=True)

    return all_suggestions[:5]  # Top 5 suggestions
```

## Transaction Sequence Generation

```python
def generate_transaction_steps(suggestion: dict) -> list:
    """
    Generate exact transaction sequence for a rebalancing suggestion.

    Example for moving USDC from Compound to Aave:
    1. Withdraw USDC from Compound
    2. Approve Aave to spend USDC
    3. Deposit USDC to Aave
    """
    steps = []

    if suggestion["action_type"] == "move":
        from_protocol = suggestion["from"]["protocol"]
        to_protocol = suggestion["to"]["protocol"]
        asset = suggestion["from"]["asset"]

        # Step 1: Withdraw
        if from_protocol.lower() == "compound":
            steps.append({
                "action": "withdraw",
                "protocol": "compound",
                "method": "redeem",
                "params": {
                    "cToken": get_ctoken_address(asset),
                    "amount": suggestion["from"]["amount"]
                }
            })

        elif from_protocol.lower() == "aave":
            steps.append({
                "action": "withdraw",
                "protocol": "aave",
                "method": "withdraw",
                "params": {
                    "asset": get_token_address(asset),
                    "amount": suggestion["from"]["amount"],
                    "to": "${USER_ADDRESS}"
                }
            })

        # Step 2: Approve (if needed)
        steps.append({
            "action": "approve",
            "protocol": to_protocol,
            "method": "approve",
            "params": {
                "token": get_token_address(asset),
                "spender": get_protocol_address(to_protocol),
                "amount": suggestion["from"]["amount"]
            }
        })

        # Step 3: Deposit
        if to_protocol.lower() == "aave":
            steps.append({
                "action": "deposit",
                "protocol": "aave",
                "method": "supply",
                "params": {
                    "asset": get_token_address(asset),
                    "amount": suggestion["from"]["amount"],
                    "onBehalfOf": "${USER_ADDRESS}",
                    "referralCode": 0
                }
            })

    return steps
```

## Example Output

```json
{
  "suggestions": [
    {
      "action_type": "move",
      "priority": "high",
      "from": {
        "protocol": "Compound V3",
        "asset": "USDC",
        "amount": 50000,
        "current_apy": 3.2
      },
      "to": {
        "protocol": "Aave V3",
        "asset": "USDC",
        "projected_apy": 4.8
      },
      "impact": {
        "yield_change_percent": 1.6,
        "yield_change_usd_annual": 800,
        "risk_change": 0,
        "estimated_cost_usd": 15,
        "breakeven_days": 7
      },
      "steps": [
        {
          "step": 1,
          "action": "withdraw",
          "protocol": "Compound",
          "description": "Withdraw 50,000 USDC from Compound",
          "estimated_gas": "150000"
        },
        {
          "step": 2,
          "action": "approve",
          "protocol": "Aave",
          "description": "Approve Aave to spend USDC",
          "estimated_gas": "50000"
        },
        {
          "step": 3,
          "action": "deposit",
          "protocol": "Aave",
          "description": "Supply 50,000 USDC to Aave",
          "estimated_gas": "200000"
        }
      ],
      "simulation_required": true,
      "requires_approval": true
    },
    {
      "action_type": "adjust",
      "priority": "medium",
      "description": "Reduce Uniswap V3 concentration",
      "from": {
        "protocol": "Uniswap V3",
        "current_allocation_percent": 60
      },
      "to": {
        "target_allocation_percent": 40,
        "suggestion": "Move $25k to Curve stablecoin pool"
      },
      "impact": {
        "yield_change_percent": -1.0,
        "yield_change_usd_annual": -250,
        "risk_change": -2.5,
        "estimated_cost_usd": 75,
        "breakeven_days": null
      },
      "rationale": "Reduces concentration risk significantly with minor yield sacrifice"
    }
  ],
  "summary": {
    "total_suggestions": 2,
    "projected_yield_improvement": 0.6,
    "projected_risk_reduction": 2.5,
    "total_estimated_cost": 90,
    "net_annual_benefit": 550
  }
}
```

## Safety Checks

Before suggesting rebalancing:

1. **Gas Cost vs Benefit**: Only suggest if breakeven < 90 days
2. **Slippage**: Estimate price impact for large moves
3. **Liquidity**: Ensure destination protocol has capacity
4. **Smart Contract Risk**: Warn if moving to newer protocols
5. **Approval Required**: All suggestions need human review

## Performance

- **Target Latency**: < 5 seconds
- **Optimization Depth**: Top 5 suggestions
- **Simulation**: All suggestions pre-simulated on Tenderly

## Notes

- Never auto-execute rebalancing
- Always show transaction sequence before approval
- Consider tax implications (not calculated here)
- Re-evaluate after each executed suggestion
