# Skill: Query Positions

## Metadata
- **ID**: `defi.query_positions`
- **Version**: 1.0.0
- **Category**: Data Retrieval
- **Risk Level**: Low (Read-only)
- **Required MCP**: ethereum, thegraph

## Description

Queries all DeFi positions for a given wallet address across supported protocols. Returns structured data about holdings, liquidity positions, lending/borrowing positions, and staking.

## Supported Protocols

- **Uniswap V3**: Liquidity positions (NFTs)
- **Aave V3**: Lending and borrowing positions
- **Compound V3**: Supply and borrow positions
- **Lido**: Staked ETH (stETH)
- **Curve**: Liquidity pool positions
- **Balancer**: Weighted pool positions

## Input Schema

```json
{
  "type": "object",
  "properties": {
    "address": {
      "type": "string",
      "pattern": "^0x[a-fA-F0-9]{40}$",
      "description": "Ethereum address to query"
    },
    "protocols": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["uniswap", "aave", "compound", "lido", "curve", "balancer"]
      },
      "description": "Specific protocols to query (default: all)",
      "default": ["uniswap", "aave", "compound", "lido"]
    },
    "include_history": {
      "type": "boolean",
      "description": "Include historical position changes",
      "default": false
    }
  },
  "required": ["address"]
}
```

## Output Schema

```json
{
  "type": "object",
  "properties": {
    "address": {
      "type": "string",
      "description": "Queried address"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Query execution time"
    },
    "positions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "protocol": {
            "type": "string",
            "description": "Protocol name"
          },
          "type": {
            "type": "string",
            "enum": ["liquidity", "lending", "borrowing", "staking"],
            "description": "Position type"
          },
          "asset": {
            "type": "string",
            "description": "Primary asset symbol"
          },
          "amount": {
            "type": "number",
            "description": "Amount in native units"
          },
          "details": {
            "type": "object",
            "description": "Protocol-specific details"
          }
        }
      }
    },
    "total_positions": {
      "type": "integer",
      "description": "Total number of positions"
    }
  }
}
```

## Implementation

### Data Sources

1. **On-chain (via ethereum MCP)**:
   - Direct contract calls for token balances
   - Uniswap V3 NFT positions
   - Aave data provider contract

2. **The Graph (via thegraph MCP)**:
   - Historical position data
   - Detailed transaction history
   - Aggregated statistics

3. **Protocol APIs**:
   - Aave: `https://aave-api-v3.aave.com/data/`
   - Compound: Direct contract queries
   - Lido: `https://stake.lido.fi/api/`

### Query Strategy

```python
async def query_positions(address: str, protocols: list) -> dict:
    """
    Query all positions for an address across protocols.

    Strategy:
    1. Parallel queries to all protocols
    2. Aggregate results
    3. Normalize data structure
    4. Cache for 5 minutes
    """
    tasks = []

    if "uniswap" in protocols:
        tasks.append(query_uniswap_positions(address))
    if "aave" in protocols:
        tasks.append(query_aave_positions(address))
    if "compound" in protocols:
        tasks.append(query_compound_positions(address))
    if "lido" in protocols:
        tasks.append(query_lido_positions(address))

    results = await asyncio.gather(*tasks, return_exceptions=True)

    positions = []
    for result in results:
        if not isinstance(result, Exception):
            positions.extend(result)

    return {
        "address": address,
        "timestamp": datetime.utcnow().isoformat(),
        "positions": positions,
        "total_positions": len(positions)
    }
```

## Example Usage

### Basic Query

**Input**:
```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
}
```

**Output**:
```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  "timestamp": "2025-01-15T10:30:00Z",
  "positions": [
    {
      "protocol": "Uniswap V3",
      "type": "liquidity",
      "asset": "USDC/ETH",
      "amount": 2,
      "details": {
        "token_ids": [123456, 123457],
        "pool": "0x88e6A0c2dDD26FEEb64F039a2c41296FcB3f5640",
        "fee_tier": "0.3%",
        "price_range": {
          "lower": 1800,
          "upper": 2200
        },
        "liquidity": "1234567890",
        "fees_earned": {
          "usdc": 45.32,
          "eth": 0.024
        }
      }
    },
    {
      "protocol": "Aave V3",
      "type": "lending",
      "asset": "USDC",
      "amount": 50000,
      "details": {
        "aToken_balance": 50123.45,
        "supply_apy": 4.5,
        "collateral_enabled": true,
        "health_factor": null
      }
    },
    {
      "protocol": "Lido",
      "type": "staking",
      "asset": "stETH",
      "amount": 10.5,
      "details": {
        "original_eth": 10.0,
        "rewards_earned": 0.5,
        "current_apy": 3.8,
        "validator_count": 2
      }
    }
  ],
  "total_positions": 3
}
```

## Error Handling

### Common Errors

1. **Invalid Address**:
```json
{
  "error": "invalid_address",
  "message": "Address must be valid Ethereum address",
  "code": 400
}
```

2. **RPC Failure**:
```json
{
  "error": "rpc_error",
  "message": "Failed to connect to Ethereum RPC",
  "code": 503,
  "retry_after": 30
}
```

3. **Rate Limited**:
```json
{
  "error": "rate_limited",
  "message": "Too many requests",
  "code": 429,
  "retry_after": 60
}
```

## Performance

- **Target Latency**: < 3 seconds
- **Cache Duration**: 5 minutes
- **Parallel Queries**: Up to 6 protocols simultaneously
- **Timeout**: 10 seconds per protocol

## Testing

```python
# Test fixtures
TEST_ADDRESS = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"

async def test_query_positions():
    result = await query_positions(TEST_ADDRESS, ["uniswap", "aave"])
    assert result["address"] == TEST_ADDRESS
    assert "positions" in result
    assert isinstance(result["positions"], list)

async def test_invalid_address():
    with pytest.raises(ValueError):
        await query_positions("invalid", ["uniswap"])

async def test_no_positions():
    # Address with no DeFi positions
    result = await query_positions("0x0000...0001", ["uniswap"])
    assert result["total_positions"] == 0
```

## Dependencies

- `web3.py` >= 6.0.0
- `aiohttp` >= 3.8.0
- `gql` >= 3.4.0 (for The Graph queries)

## Rate Limits

- Ethereum RPC: Depends on provider (typically 100-300 req/sec)
- The Graph: 1000 queries/day (free tier)
- Protocol APIs: Varies (typically 100 req/min)

## Notes

- Always validate addresses before querying
- Use multicall patterns to reduce RPC calls
- Cache aggressively for read-only data
- Handle partial failures gracefully (some protocols may be down)
- Log all queries for debugging and optimization
