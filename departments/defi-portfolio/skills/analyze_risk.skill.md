# Skill: Analyze Risk

## Metadata
- **ID**: `defi.analyze_risk`
- **Version**: 1.0.0
- **Category**: Risk Management
- **Risk Level**: Low (Read-only)
- **Required MCP**: ethereum, thegraph, defi-protocols

## Description

Analyzes portfolio risk across multiple dimensions including concentration risk, protocol risk, smart contract risk, liquidity risk, and market risk. Provides actionable recommendations for risk mitigation.

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "positions": {
      "type": "array",
      "description": "Portfolio positions to analyze"
    },
    "risk_tolerance": {
      "type": "string",
      "enum": ["conservative", "moderate", "aggressive"],
      "default": "moderate"
    },
    "include_historical_volatility": {
      "type": "boolean",
      "default": true
    }
  },
  "required": ["positions"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "risk_score": {
      "type": "number",
      "minimum": 0,
      "maximum": 10,
      "description": "Overall risk score (0=lowest, 10=highest)"
    },
    "risk_level": {
      "type": "string",
      "enum": ["very_low", "low", "medium", "high", "very_high"]
    },
    "risk_factors": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "category": {"type": "string"},
          "severity": {"type": "string"},
          "score": {"type": "number"},
          "message": {"type": "string"},
          "recommendation": {"type": "string"}
        }
      }
    },
    "recommendations": {
      "type": "array",
      "items": {"type": "string"}
    }
  }
}
```

## Risk Categories

### 1. Concentration Risk
Measures diversification across protocols, assets, and position types.

```python
def calculate_concentration_risk(positions: list) -> dict:
    """
    Check if portfolio is too concentrated.

    Red flags:
    - >50% in single protocol
    - >70% in single asset
    - <3 different protocols used
    """
    total_value = sum(p["value_usd"] for p in positions)

    # Protocol concentration
    protocol_values = {}
    for pos in positions:
        protocol = pos["protocol"]
        protocol_values[protocol] = protocol_values.get(protocol, 0) + pos["value_usd"]

    max_protocol_percent = max(protocol_values.values()) / total_value * 100

    if max_protocol_percent > 70:
        severity = "high"
        score = 8
    elif max_protocol_percent > 50:
        severity = "medium"
        score = 6
    else:
        severity = "low"
        score = 3

    return {
        "category": "concentration",
        "severity": severity,
        "score": score,
        "message": f"{max_protocol_percent:.1f}% of portfolio in single protocol",
        "recommendation": "Diversify across at least 3-4 protocols"
    }
```

### 2. Protocol Risk
Evaluates safety of protocols based on TVL, audits, age, exploits history.

```python
PROTOCOL_SCORES = {
    "aave": {"score": 9, "audits": 15, "age_years": 4},
    "compound": {"score": 9, "audits": 12, "age_years": 5},
    "uniswap": {"score": 10, "audits": 20, "age_years": 4},
    "lido": {"score": 9, "audits": 10, "age_years": 3},
    "curve": {"score": 8, "audits": 8, "age_years": 3},
}

def calculate_protocol_risk(positions: list) -> dict:
    """
    Assess protocol safety.

    Criteria:
    - Audit count and quality
    - TVL (> $1B = safer)
    - Time in production
    - Historical exploits
    - Governance maturity
    """
    risks = []

    for pos in positions:
        protocol = pos["protocol"].lower()
        info = PROTOCOL_SCORES.get(protocol, {"score": 5})

        if info["score"] < 7:
            risks.append({
                "protocol": protocol,
                "issue": "Lower audit coverage or newer protocol",
                "score": 10 - info["score"]
            })

    if not risks:
        return {
            "category": "protocol_risk",
            "severity": "low",
            "score": 2,
            "message": "All protocols have strong safety records",
            "recommendation": "Continue monitoring for governance changes"
        }

    avg_risk = sum(r["score"] for r in risks) / len(positions)
    return {
        "category": "protocol_risk",
        "severity": "medium" if avg_risk > 4 else "low",
        "score": avg_risk,
        "message": f"{len(risks)} position(s) in higher-risk protocols",
        "recommendation": "Consider moving to battle-tested protocols"
    }
```

### 3. Smart Contract Risk
Specific contract-level risks.

```python
def calculate_smart_contract_risk(positions: list) -> dict:
    """
    Check for contract-specific risks.

    - Upgradeable contracts (admin keys)
    - Unverified contracts
    - Complex/novel mechanisms
    """
    high_risk_contracts = []

    for pos in positions:
        # Check if contract is verified
        if not await is_contract_verified(pos.get("contract_address")):
            high_risk_contracts.append(pos)

        # Check for upgrade mechanisms
        if await has_admin_keys(pos.get("contract_address")):
            high_risk_contracts.append(pos)

    if len(high_risk_contracts) > 0:
        return {
            "category": "smart_contract",
            "severity": "high",
            "score": 8,
            "message": f"{len(high_risk_contracts)} position(s) with elevated contract risk",
            "recommendation": "Avoid unverified or upgradeable contracts"
        }

    return {
        "category": "smart_contract",
        "severity": "low",
        "score": 2,
        "message": "All contracts verified and immutable",
        "recommendation": "No action needed"
    }
```

### 4. Liquidity Risk
Can you exit positions quickly without high slippage?

```python
def calculate_liquidity_risk(positions: list) -> dict:
    """
    Assess ease of exiting positions.

    For LP positions:
    - Pool depth
    - 24h volume
    - Your position size vs pool

    For lending:
    - Utilization rate
    - Available liquidity
    """
    illiquid_positions = []

    for pos in positions:
        if pos["type"] == "liquidity":
            pool_liquidity = await get_pool_tvl(pos["pool"])
            position_percent = pos["value_usd"] / pool_liquidity * 100

            if position_percent > 10:  # >10% of pool
                illiquid_positions.append(pos)

        elif pos["type"] == "lending":
            utilization = await get_utilization_rate(pos["protocol"], pos["asset"])
            if utilization > 90:  # >90% utilized
                illiquid_positions.append(pos)

    if len(illiquid_positions) > 0:
        return {
            "category": "liquidity",
            "severity": "medium",
            "score": 6,
            "message": f"{len(illiquid_positions)} position(s) may have exit friction",
            "recommendation": "Keep positions <5% of pool liquidity"
        }

    return {
        "category": "liquidity",
        "severity": "low",
        "score": 2,
        "message": "All positions easily exitible",
        "recommendation": "No action needed"
    }
```

### 5. Market Risk
Exposure to volatile assets and price movements.

```python
def calculate_market_risk(positions: list) -> dict:
    """
    Analyze exposure to volatile assets.

    - Stablecoin % vs volatile assets
    - Correlation between holdings
    - IL exposure for LP positions
    """
    total_value = sum(p["value_usd"] for p in positions)
    volatile_value = 0
    stable_value = 0

    STABLECOINS = ["USDC", "USDT", "DAI", "FRAX"]

    for pos in positions:
        asset = pos["asset"]
        if any(stable in asset for stable in STABLECOINS):
            stable_value += pos["value_usd"]
        else:
            volatile_value += pos["value_usd"]

    volatile_percent = volatile_value / total_value * 100

    if volatile_percent > 70:
        severity = "high"
        score = 7
        message = f"{volatile_percent:.1f}% in volatile assets"
        recommendation = "Consider increasing stablecoin allocation"
    elif volatile_percent > 40:
        severity = "medium"
        score = 5
        message = f"{volatile_percent:.1f}% in volatile assets"
        recommendation = "Monitor market conditions closely"
    else:
        severity = "low"
        score = 3
        message = f"Well-balanced stable/volatile ratio"
        recommendation = "Maintain current allocation"

    return {
        "category": "market_risk",
        "severity": severity,
        "score": score,
        "message": message,
        "recommendation": recommendation
    }
```

## Overall Risk Score Calculation

```python
async def analyze_risk(positions: list, risk_tolerance: str = "moderate") -> dict:
    """
    Comprehensive risk analysis.
    """
    # Calculate individual risk factors
    concentration = calculate_concentration_risk(positions)
    protocol = calculate_protocol_risk(positions)
    smart_contract = await calculate_smart_contract_risk(positions)
    liquidity = await calculate_liquidity_risk(positions)
    market = calculate_market_risk(positions)

    risk_factors = [concentration, protocol, smart_contract, liquidity, market]

    # Weighted average (some factors more important)
    WEIGHTS = {
        "concentration": 0.25,
        "protocol_risk": 0.30,
        "smart_contract": 0.25,
        "liquidity": 0.10,
        "market_risk": 0.10
    }

    overall_score = sum(
        factor["score"] * WEIGHTS[factor["category"]]
        for factor in risk_factors
    )

    # Adjust for risk tolerance
    if risk_tolerance == "conservative":
        overall_score *= 1.2  # More sensitive
    elif risk_tolerance == "aggressive":
        overall_score *= 0.8  # Less sensitive

    # Classify risk level
    if overall_score < 3:
        risk_level = "very_low"
    elif overall_score < 5:
        risk_level = "low"
    elif overall_score < 7:
        risk_level = "medium"
    elif overall_score < 8.5:
        risk_level = "high"
    else:
        risk_level = "very_high"

    # Generate recommendations
    recommendations = []
    for factor in risk_factors:
        if factor["severity"] in ["medium", "high"]:
            recommendations.append(factor["recommendation"])

    return {
        "risk_score": round(overall_score, 1),
        "risk_level": risk_level,
        "risk_factors": risk_factors,
        "recommendations": recommendations,
        "timestamp": datetime.utcnow().isoformat()
    }
```

## Example Output

```json
{
  "risk_score": 6.5,
  "risk_level": "medium",
  "risk_factors": [
    {
      "category": "concentration",
      "severity": "medium",
      "score": 6,
      "message": "68% of portfolio in single protocol (Uniswap)",
      "recommendation": "Diversify across at least 3-4 protocols"
    },
    {
      "category": "protocol_risk",
      "severity": "low",
      "score": 2,
      "message": "All protocols have strong safety records",
      "recommendation": "Continue monitoring for governance changes"
    },
    {
      "category": "smart_contract",
      "severity": "low",
      "score": 2,
      "message": "All contracts verified and immutable",
      "recommendation": "No action needed"
    },
    {
      "category": "liquidity",
      "severity": "medium",
      "score": 6,
      "message": "1 position(s) may have exit friction",
      "recommendation": "Keep positions <5% of pool liquidity"
    },
    {
      "category": "market_risk",
      "severity": "medium",
      "score": 5,
      "message": "55% in volatile assets",
      "recommendation": "Monitor market conditions closely"
    }
  ],
  "recommendations": [
    "Diversify across at least 3-4 protocols",
    "Keep positions <5% of pool liquidity",
    "Monitor market conditions closely"
  ],
  "timestamp": "2025-01-15T10:30:00Z"
}
```

## Performance

- **Target Latency**: < 3 seconds
- **Cache Duration**: 10 minutes
- **Heavy Computation**: Protocol safety scores updated daily

## Notes

- Risk scores are relative, not absolute
- Always consider personal risk tolerance
- Review risk factors during market volatility
- Historical data improves accuracy
