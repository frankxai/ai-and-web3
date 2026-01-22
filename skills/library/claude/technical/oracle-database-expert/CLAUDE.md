# Oracle Database Expert

Oracle Database design, optimization, performance tuning, and best practices for enterprise data management.

## Quick Reference

**When to Use**: Database architecture, optimization, SQL tuning
**Key Services**: Autonomous Database (ATP/ADW), Base Database, Exadata
**Expertise**: SQL, PL/SQL, performance tuning, data modeling

## Core Competencies

### Autonomous Database (ADB)
- **ATP**: Transaction Processing (OLTP)
- **ADW**: Data Warehouse (analytics)
- **AJD**: JSON Document Store
- Self-driving, self-securing, self-repairing

### Performance Optimization
- SQL tuning and execution plans
- Index design and maintenance
- Partitioning strategies
- Memory and I/O optimization

### Data Modeling
- Normalized vs. denormalized design
- Star/snowflake schemas for DW
- JSON-relational hybrid models

## Key Patterns

```sql
-- Autonomous Database connection
-- Use wallet-based authentication

-- Performance tuning hint
SELECT /*+ INDEX(orders orders_date_idx) */
  order_id, customer_id, order_date
FROM orders
WHERE order_date > SYSDATE - 30;

-- JSON in Oracle 23ai
SELECT j.data.customer.name
FROM orders_json j
WHERE JSON_VALUE(j.data, '$.status') = 'active';
```

## Integration with AI

### Oracle 23ai Features
- **AI Vector Search**: Native vector similarity search
- **Select AI**: Natural language to SQL
- **JSON Relational Duality**: GraphQL-like views

### For AI Agents
```python
# ADK with ADB
from oci_adk.tools import SQLTool

db_tool = SQLTool(
    connection_string=adb_connection,
    allowed_tables=["customers", "orders"]
)
```

## Decision Guide

**Use Oracle DB when**:
- Enterprise-grade reliability required
- Complex transactions and ACID compliance
- Existing Oracle investment/licensing
- Need AI vector search with relational data

## Related Skills
- `oci-services-expert` - Cloud deployment
- `oracle-adk` - AI agent integration
- `oracle-agent-spec` - Agent definitions

---

*Comprehensive database expertise for enterprise Oracle workloads.*
