# Skill: Calculate Yields

## Metadata
- **ID**: `defi.calculate_yields`
- **Version**: 1.0.0
- **Category**: Analytics
- **Risk Level**: Low (Read-only)
- **Required MCP**: ethereum, thegraph, defi-protocols

## Description

Calculates current and projected yields (APY/APR) for DeFi positions. Includes historical yield trends, yield composition breakdown, and projected earnings based on current rates.

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "positions": {
      "type": "array",
      "description": "Positions to analyze (from query_positions)",
      "items": {
        "type": "object"
      }
    },
    "time_horizon_days": {
      "type": "integer",
      "description": "Projection time horizon in days",
      "default": 30,
      "minimum": 1,
      "maximum": 365
    },
    "include_il": {
      "type": "boolean",
      "description": "Include impermanent loss calculations for LP positions",
      "default": true
    },
    "include_historical": {
      "type": "boolean",
      "description": "Include 30-day historical yield data",
      "default": false
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
    "summary": {
      "type": "object",
      "properties": {
        "total_value_usd": {"type": "number"},
        "weighted_avg_apy": {"type": "number"},
        "projected_earnings_usd": {"type": "number"},
        "timestamp": {"type": "string"}
      }
    },
    "yields": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "protocol": {"type": "string"},
          "position_type": {"type": "string"},
          "asset": {"type": "string"},
          "current_apy": {"type": "number"},
          "apy_breakdown": {
            "type": "object",
            "description": "Yield sources (base, rewards, fees)"
          },
          "projected_earnings": {
            "type": "object",
            "properties": {
              "daily_usd": {"type": "number"},
              "monthly_usd": {"type": "number"},
              "annual_usd": {"type": "number"}
            }
          },
          "impermanent_loss": {
            "type": "object",
            "nullable": true
          }
        }
      }
    }
  }
}
```

## Implementation

### Yield Calculation Methods

#### 1. Lending/Borrowing (Aave, Compound)
```python
def calculate_lending_apy(protocol: str, asset: str) -> float:
    """
    Get current lending APY from protocol.

    Aave: Use LendingPoolDataProvider.getReserveData()
    Compound: Use CToken.supplyRatePerBlock() * blocks_per_year
    """
    if protocol == "aave":
        reserve_data = await aave_data_provider.getReserveData(asset)
        return reserve_data.liquidityRate / 1e27 * 100  # Convert to %

    elif protocol == "compound":
        ctoken = get_ctoken(asset)
        rate_per_block = await ctoken.supplyRatePerBlock()
        blocks_per_year = 2628000  # ~12s blocks
        return ((rate_per_block / 1e18 * blocks_per_year) + 1) ** 1 - 1
```

#### 2. Liquidity Positions (Uniswap V3)
```python
def calculate_lp_apy(pool: str, position: dict) -> dict:
    """
    Calculate LP position APY including fees and IL.

    Components:
    - Fee APY: (24h fees / liquidity) * 365
    - Reward APY: Protocol incentives
    - IL: Estimated based on price volatility
    """
    # Get 24h fee revenue
    fees_24h = await get_pool_fees_24h(pool)
    liquidity = await get_pool_liquidity(pool)
    fee_apy = (fees_24h / liquidity) * 365 * 100

    # Get incentive rewards (if any)
    rewards_apy = await get_incentive_apy(pool)

    # Estimate IL based on volatility
    il_estimate = calculate_il_estimate(position, pool)

    return {
        "total_apy": fee_apy + rewards_apy,
        "fee_apy": fee_apy,
        "reward_apy": rewards_apy,
        "estimated_il_percent": il_estimate
    }
```

#### 3. Staking (Lido)
```python
def calculate_staking_apy(protocol: str, asset: str) -> float:
    """
    Get staking APY.

    Lido: API endpoint or oracle
    """
    if protocol == "lido" and asset == "stETH":
        response = await fetch("https://stake.lido.fi/api/sma-steth-apr")
        return response["smaApr"]
```

### Yield Aggregation

```python
async def calculate_yields(positions: list, time_horizon_days: int = 30) -> dict:
    """
    Calculate yields for all positions.
    """
    yields = []
    total_value = 0

    for position in positions:
        protocol = position["protocol"]
        pos_type = position["type"]
        value_usd = position.get("value_usd", 0)

        if pos_type == "lending":
            apy = await calculate_lending_apy(protocol, position["asset"])
        elif pos_type == "liquidity":
            apy_data = await calculate_lp_apy(position["pool"], position)
            apy = apy_data["total_apy"]
        elif pos_type == "staking":
            apy = await calculate_staking_apy(protocol, position["asset"])
        else:
            apy = 0

        # Project earnings
        daily_earnings = value_usd * (apy / 100) / 365
        projected = {
            "daily_usd": daily_earnings,
            "monthly_usd": daily_earnings * 30,
            "annual_usd": daily_earnings * 365
        }

        yields.append({
            "protocol": protocol,
            "position_type": pos_type,
            "asset": position["asset"],
            "value_usd": value_usd,
            "current_apy": round(apy, 2),
            "projected_earnings": projected
        })

        total_value += value_usd

    # Calculate weighted average APY
    weighted_apy = sum(y["current_apy"] * y["value_usd"] for y in yields) / total_value

    return {
        "summary": {
            "total_value_usd": round(total_value, 2),
            "weighted_avg_apy": round(weighted_apy, 2),
            "projected_earnings_usd": sum(y["projected_earnings"]["monthly_usd"] for y in yields),
            "timestamp": datetime.utcnow().isoformat()
        },
        "yields": yields
    }
```

## Example Usage

### Input
```json
{
  "positions": [
    {
      "protocol": "Aave V3",
      "type": "lending",
      "asset": "USDC",
      "amount": 50000,
      "value_usd": 50000
    },
    {
      "protocol": "Uniswap V3",
      "type": "liquidity",
      "asset": "USDC/ETH",
      "pool": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
      "value_usd": 75000
    }
  ],
  "time_horizon_days": 30
}
```

### Output
```json
{
  "summary": {
    "total_value_usd": 125000,
    "weighted_avg_apy": 9.2,
    "projected_earnings_usd": 958.33,
    "timestamp": "2025-01-15T10:30:00Z"
  },
  "yields": [
    {
      "protocol": "Aave V3",
      "position_type": "lending",
      "asset": "USDC",
      "value_usd": 50000,
      "current_apy": 4.5,
      "apy_breakdown": {
        "base_rate": 3.2,
        "bonus_rewards": 1.3
      },
      "projected_earnings": {
        "daily_usd": 6.16,
        "monthly_usd": 187.5,
        "annual_usd": 2250
      }
    },
    {
      "protocol": "Uniswap V3",
      "position_type": "liquidity",
      "asset": "USDC/ETH",
      "value_usd": 75000,
      "current_apy": 12.3,
      "apy_breakdown": {
        "fee_apy": 12.3,
        "reward_apy": 0
      },
      "projected_earnings": {
        "daily_usd": 25.27,
        "monthly_usd": 770.83,
        "annual_usd": 9225
      },
      "impermanent_loss": {
        "current_percent": -2.1,
        "breakeven_days": 45,
        "note": "Current IL offset by fees in ~45 days at current rate"
      }
    }
  ]
}
```

## Performance

- **Target Latency**: < 2 seconds
- **Cache Duration**: 1 minute (APYs change frequently)
- **Batch Queries**: Use multicall for on-chain data

## Dependencies

- Protocol contracts (Aave, Compound, Uniswap)
- The Graph for historical fee data
- Price feeds for IL calculations

## Notes

- APYs are dynamic and change constantly
- LP positions require volatility analysis for IL
- Consider gas costs in net yield calculations
- Historical APY data helps identify trends
