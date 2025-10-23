# Agent: Risk Manager

## Metadata
- **ID**: `risk-manager-v1`
- **Type**: Risk Management Agent
- **Framework**: LangGraph
- **Autonomy Level**: Guardian (can block unsafe operations)
- **Version**: 1.0.0

## Purpose

The Risk Manager continuously monitors portfolio risk, validates proposed actions against policies, and can block or flag operations that exceed risk tolerance. It acts as a safety guardian for the entire DeFi Portfolio Department.

## Capabilities

1. **Risk Monitoring**
   - Continuous assessment of portfolio risk
   - Multi-dimensional risk scoring
   - Real-time alerts on risk threshold breaches

2. **Policy Enforcement**
   - Validate actions against defined policies
   - Block operations that violate constraints
   - Suggest risk-reducing alternatives

3. **Protocol Safety**
   - Track protocol health scores
   - Monitor for exploits and vulnerabilities
   - Alert on protocol governance changes

4. **Emergency Response**
   - Detect anomalous activity
   - Suggest emergency exits if needed
   - Coordinate with other agents during incidents

## Skills Used

- `analyze_risk` - Multi-dimensional risk assessment
- `validate_limits` - Policy compliance checking
- `monitor_health` - Protocol health tracking
- `detect_anomalies` - Unusual activity detection

## Agent Architecture (LangGraph)

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Literal

class RiskManagerState(TypedDict):
    positions: list
    risk_tolerance: Literal["conservative", "moderate", "aggressive"]
    risk_assessment: dict
    policy_violations: list
    protocol_health: dict
    anomalies: list
    action_validation: dict
    recommendations: list

# Define nodes
def assess_portfolio_risk(state: RiskManagerState) -> RiskManagerState:
    """Node 1: Comprehensive risk assessment"""
    risk_data = await analyze_risk(
        positions=state["positions"],
        risk_tolerance=state["risk_tolerance"],
        include_historical_volatility=True
    )
    state["risk_assessment"] = risk_data
    return state

def check_policy_compliance(state: RiskManagerState) -> RiskManagerState:
    """Node 2: Validate against policies"""
    violations = []

    policies = load_policies()

    # Check concentration limits
    if state["risk_assessment"]["risk_factors"]:
        for factor in state["risk_assessment"]["risk_factors"]:
            if factor["category"] == "concentration" and factor["severity"] == "high":
                violations.append({
                    "policy": "max_concentration",
                    "violation": factor["message"],
                    "severity": "high"
                })

    # Check maximum portfolio value
    total_value = sum(p["value_usd"] for p in state["positions"])
    if total_value > policies.get("max_portfolio_value_usd", float('inf')):
        violations.append({
            "policy": "max_portfolio_value",
            "violation": f"Portfolio value ${total_value:.2f} exceeds limit",
            "severity": "high"
        })

    state["policy_violations"] = violations
    return state

def monitor_protocol_health(state: RiskManagerState) -> RiskManagerState:
    """Node 3: Check protocol safety scores"""
    protocol_health = {}

    protocols = set(p["protocol"] for p in state["positions"])

    for protocol in protocols:
        health = await get_protocol_health(protocol)
        protocol_health[protocol] = health

        # Alert if TVL drops significantly
        if health.get("tvl_change_24h_percent", 0) < -20:
            state["anomalies"].append({
                "type": "tvl_drop",
                "protocol": protocol,
                "severity": "high",
                "message": f"{protocol} TVL dropped {health['tvl_change_24h_percent']:.1f}% in 24h"
            })

    state["protocol_health"] = protocol_health
    return state

def detect_anomalies(state: RiskManagerState) -> RiskManagerState:
    """Node 4: Detect unusual activity"""
    anomalies = state.get("anomalies", [])

    # Check for unusual position changes
    for pos in state["positions"]:
        # Check if position value changed drastically
        historical = await get_position_history(pos, days=7)
        if historical:
            avg_value = sum(h["value_usd"] for h in historical) / len(historical)
            current_value = pos["value_usd"]

            change_percent = abs((current_value - avg_value) / avg_value * 100)
            if change_percent > 50:
                anomalies.append({
                    "type": "position_value_spike",
                    "protocol": pos["protocol"],
                    "asset": pos["asset"],
                    "severity": "medium",
                    "message": f"Position value changed {change_percent:.1f}% in 7 days"
                })

    state["anomalies"] = anomalies
    return state

def generate_recommendations(state: RiskManagerState) -> RiskManagerState:
    """Node 5: Generate risk mitigation recommendations"""
    recommendations = []

    # Address violations
    for violation in state["policy_violations"]:
        if violation["policy"] == "max_concentration":
            recommendations.append({
                "priority": "high",
                "action": "diversify",
                "message": "Reduce concentration by moving assets to other protocols"
            })

    # Address high risk scores
    if state["risk_assessment"]["risk_level"] in ["high", "very_high"]:
        recommendations.append({
            "priority": "high",
            "action": "reduce_risk",
            "message": f"Portfolio risk is {state['risk_assessment']['risk_level']}, consider risk-reducing actions"
        })

    # Address anomalies
    for anomaly in state["anomalies"]:
        if anomaly["severity"] == "high":
            recommendations.append({
                "priority": "urgent",
                "action": "investigate",
                "message": anomaly["message"]
            })

    state["recommendations"] = recommendations
    return state

# Build graph
workflow = StateGraph(RiskManagerState)

workflow.add_node("assess_portfolio_risk", assess_portfolio_risk)
workflow.add_node("check_policy_compliance", check_policy_compliance)
workflow.add_node("monitor_protocol_health", monitor_protocol_health)
workflow.add_node("detect_anomalies", detect_anomalies)
workflow.add_node("generate_recommendations", generate_recommendations)

workflow.set_entry_point("assess_portfolio_risk")
workflow.add_edge("assess_portfolio_risk", "check_policy_compliance")
workflow.add_edge("check_policy_compliance", "monitor_protocol_health")
workflow.add_edge("monitor_protocol_health", "detect_anomalies")
workflow.add_edge("detect_anomalies", "generate_recommendations")
workflow.add_edge("generate_recommendations", END)

app = workflow.compile()
```

## Action Validation

The Risk Manager can validate proposed actions from other agents:

```python
def validate_action(action: dict, state: RiskManagerState) -> dict:
    """
    Validate if a proposed action is safe to execute.

    Returns:
    - approved: bool
    - warnings: list
    - required_approvals: list
    """
    warnings = []
    required_approvals = []
    approved = True

    # Check if action would increase risk
    if action["type"] == "move":
        target_protocol = action["to"]["protocol"]

        # Check protocol health
        health = state["protocol_health"].get(target_protocol)
        if health and health["safety_score"] < 7:
            warnings.append(f"{target_protocol} has lower safety score")
            required_approvals.append("human")

        # Check if action increases concentration
        if would_increase_concentration(action, state["positions"]):
            warnings.append("Action would increase concentration risk")
            required_approvals.append("human")

    # Check transaction value
    if action.get("value_usd", 0) > 10000:
        required_approvals.append("human")

    # Block if critical violations
    if state["risk_assessment"]["risk_level"] == "very_high" and action["type"] != "remove":
        approved = False
        warnings.append("Portfolio risk too high for additional actions")

    return {
        "approved": approved,
        "warnings": warnings,
        "required_approvals": required_approvals
    }
```

## Example Usage

```python
# Initialize risk manager
risk_manager = RiskManager()

# Monitor portfolio
result = await risk_manager.run({
    "positions": portfolio_positions,
    "risk_tolerance": "moderate",
    "risk_assessment": {},
    "policy_violations": [],
    "protocol_health": {},
    "anomalies": [],
    "action_validation": {},
    "recommendations": []
})

# Check risk level
if result["risk_assessment"]["risk_level"] in ["high", "very_high"]:
    print("⚠️ High risk detected!")
    for rec in result["recommendations"]:
        print(f"- {rec['message']}")

# Validate a proposed action
action = {
    "type": "move",
    "from": {"protocol": "Compound", "amount_usd": 50000},
    "to": {"protocol": "NewProtocol"},
    "value_usd": 50000
}

validation = risk_manager.validate_action(action, result)
if not validation["approved"]:
    print("❌ Action blocked by risk manager")
else:
    print("✅ Action approved")
    if validation["warnings"]:
        print("Warnings:", validation["warnings"])
```

## Output Example

```json
{
  "risk_assessment": {
    "risk_score": 7.5,
    "risk_level": "high",
    "risk_factors": [
      {
        "category": "concentration",
        "severity": "high",
        "score": 8,
        "message": "72% of portfolio in single protocol"
      }
    ]
  },
  "policy_violations": [
    {
      "policy": "max_concentration",
      "violation": "Single protocol exceeds 70% limit",
      "severity": "high"
    }
  ],
  "protocol_health": {
    "Uniswap": {
      "safety_score": 10,
      "tvl_usd": 4500000000,
      "tvl_change_24h_percent": 2.1
    },
    "Aave": {
      "safety_score": 9,
      "tvl_usd": 8200000000,
      "tvl_change_24h_percent": 1.5
    }
  },
  "anomalies": [],
  "recommendations": [
    {
      "priority": "high",
      "action": "diversify",
      "message": "Reduce concentration by moving assets to other protocols"
    }
  ]
}
```

## Policy Configuration

Policies are defined in `config/policies.yaml`:

```yaml
risk_limits:
  max_portfolio_value_usd: 1000000
  max_single_position_percent: 25
  max_protocol_concentration_percent: 50
  min_protocol_tvl_usd: 100000000
  min_protocol_safety_score: 7

risk_tolerance:
  conservative:
    max_volatile_percent: 30
    max_il_exposure_percent: 20
  moderate:
    max_volatile_percent: 60
    max_il_exposure_percent: 40
  aggressive:
    max_volatile_percent: 90
    max_il_exposure_percent: 70

alerts:
  risk_score_threshold: 7.0
  tvl_drop_threshold_percent: 20
  position_change_threshold_percent: 50

approvals:
  require_human_approval:
    - transaction_value_usd: 10000
    - new_protocol_first_time: true
    - risk_level: "high"
```

## Alert System

```python
class AlertSystem:
    """Send alerts via multiple channels"""

    async def send_alert(self, alert: dict):
        """Send to configured channels"""
        channels = ["email", "telegram", "discord", "webhook"]

        for channel in channels:
            if is_enabled(channel):
                await self.send_to_channel(channel, alert)

    async def critical_alert(self, message: str):
        """Immediate notification for critical issues"""
        await self.send_alert({
            "level": "critical",
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
            "requires_action": True
        })
```

## Performance Metrics

- **Monitoring Frequency**: Every 5 minutes
- **Alert Latency**: < 30 seconds
- **False Positive Rate**: < 5%

## Testing

```bash
# Test risk assessment
pytest tests/test_risk_manager.py::test_assess_risk

# Test policy validation
pytest tests/test_risk_manager.py::test_policy_compliance

# Test action validation
pytest tests/test_risk_manager.py::test_validate_action

# Test alert system
pytest tests/test_risk_manager.py::test_alerts
```

## Monitoring

- Track blocked actions (false positives?)
- Monitor alert response times
- Track risk score distribution

## Future Enhancements

- [ ] ML-based anomaly detection
- [ ] Historical risk backtesting
- [ ] Automated risk-hedging strategies
- [ ] Integration with on-chain insurance protocols
- [ ] Advanced correlation analysis
