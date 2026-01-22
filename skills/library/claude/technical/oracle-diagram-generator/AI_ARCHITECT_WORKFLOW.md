# AI Architect Workflow for OCI Diagram Generation

## Overview

This workflow ensures professional-quality OCI architecture diagrams by **thinking through the solution architecture FIRST** before generating any diagrams.

## Phase 1: Requirements Analysis

### Business Domain Understanding
Before any diagram, answer these questions:

1. **What is the business domain?**
   - Marketing, Sales, Legal, HR, Finance, Operations, etc.
   - What are the key business processes?
   - Who are the users/stakeholders?

2. **What problems are we solving?**
   - Current pain points
   - Manual processes to automate
   - Data silos to connect

3. **What outcomes are expected?**
   - Efficiency gains (quantify if possible)
   - Cost reduction targets
   - Quality/accuracy improvements

### Example: Marketing Agent System
```
Domain: Marketing Operations
Problems:
  - Manual content creation taking 20+ hours/week
  - Inconsistent campaign performance analysis
  - Siloed data across platforms
Outcomes:
  - 70% reduction in content creation time
  - Real-time campaign optimization
  - Unified customer 360 view
```

## Phase 2: Agent Architecture Design

### Identify Agent Types Needed

Use this decision framework:

| Agent Type | When to Use | Example |
|------------|-------------|---------|
| **Orchestrator** | Coordinates multiple specialists | Campaign Planner, Deal Manager |
| **Specialist** | Deep expertise in one domain | SEO Agent, Contract Analyzer |
| **Utility** | Common functions across domains | Document Generator, Data Fetcher |
| **Monitor** | Continuous surveillance | Compliance Monitor, Performance Tracker |

### Design Agent Hierarchy

Standard pattern (from Oracle ADK):
```
                    ┌─────────────────┐
                    │   Agent Hub     │
                    │  (OCI GenAI)    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Orchestrator   │
                    │  (Supervisor)   │
                    └────────┬────────┘
           ┌─────────────────┼─────────────────┐
           │                 │                 │
    ┌──────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
    │ Specialist  │   │ Specialist  │   │ Specialist  │
    │   Agent 1   │   │   Agent 2   │   │   Agent N   │
    └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
           └─────────────────┼─────────────────┘
                             │
                    ┌────────▼────────┐
                    │   Tool Layer    │
                    │ (APIs, DBs, etc)│
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   Data Layer    │
                    │  (ADB, Storage) │
                    └─────────────────┘
```

### Map Agents to OCI Services

| Component | OCI Service | Icon Index |
|-----------|-------------|------------|
| Agent Hub | OCI Generative AI | 60 (ai) |
| Specialist Agent | OCI Generative AI | 60 (ai) |
| Tool - API | API Gateway | 79 |
| Tool - Compute | Functions | 2 |
| Tool - Integration | Integration Cloud | 81 |
| Data - Database | Autonomous DB | 37 |
| Data - Storage | Object Storage | 11 |
| Data - Secrets | Vault | 105 |

## Phase 3: Data Flow Design

### Identify Data Flows

For each agent, document:
1. **Inputs**: What data does it receive?
2. **Processing**: What transformation/analysis?
3. **Outputs**: What does it produce?
4. **Persistence**: What needs to be stored?

### Example: Content Creator Agent
```
Inputs:
  - Campaign brief from Orchestrator
  - Brand guidelines from Knowledge Base
  - Audience persona from CDP

Processing:
  - Generate content variations
  - Check brand compliance
  - Optimize for SEO

Outputs:
  - Draft content to Orchestrator
  - SEO recommendations to SEO Agent

Persistence:
  - Content drafts to Object Storage
  - Generation metrics to ADB
```

### Design Connector Labels

Use action-oriented labels (from Oracle official patterns):
- ✅ "generate content draft"
- ✅ "fetch customer data"
- ✅ "analyze performance"
- ❌ "data" (too vague)
- ❌ "connection" (meaningless)

## Phase 4: Cost Estimation

### Calculate Monthly Costs

| Service | Pricing Model | Typical Range |
|---------|---------------|---------------|
| OCI GenAI (Cohere Cmd A) | $0.0015/1K tokens in, $0.002/1K out | $100-500/mo |
| ADB 26ai (Always Free) | $0 for 2 instances | $0 |
| ADB 26ai (Paid) | $0.336/ECPU-hour | $240+/mo |
| Functions | $0.0002/GB-second | $5-50/mo |
| Object Storage | $0.0255/GB/mo | $3-30/mo |
| API Gateway | $3.50/million calls | $10-50/mo |

### Cost Box Format
```
💰 MONTHLY COST ESTIMATE
━━━━━━━━━━━━━━━━━━━━━━━━
OCI GenAI: $XXX
ADB 26ai: $XXX
Functions: $XX
Storage: $X
━━━━━━━━━━━━━━━━━━━━━━━━
TOTAL: $XXX-XXX/mo
```

## Phase 5: Diagram Layout Planning

### Standard Dimensions
- **Canvas**: 1400-1600px wide × 800-1000px tall
- **Icons**: 85px standard size
- **Spacing**: 160px horizontal, 140px vertical
- **Containers**: 30-40px padding

### Layout Grid
```
Y=80:   Agent Hub (centered)
Y=200:  Orchestrator Layer
Y=330:  Specialist Agents
Y=510:  Tool Layer
Y=660:  Data Layer
```

### Container Sizing
| Layer | Typical Width | Typical Height |
|-------|---------------|----------------|
| Hub | 300-400px | 100px |
| Orchestrator | 500-600px | 110px |
| Specialists | 1100-1300px | 160px |
| Tools | 1000-1200px | 130px |
| Data | 800-1000px | 130px |

## Phase 6: Quality Checklist

Before finalizing any diagram, verify:

### Visual Standards
- [ ] All icons are 85px (not smaller)
- [ ] All fonts are 14-16px
- [ ] Colors match Oracle palette
- [ ] Consistent spacing between elements
- [ ] Labels are centered below icons

### Architecture Quality
- [ ] Clear hierarchy (Hub → Orchestrator → Specialists)
- [ ] All agents have clear purpose
- [ ] Data flows are labeled with actions
- [ ] Tools connect to appropriate agents
- [ ] Cost estimate is included

### Technical Accuracy
- [ ] OCI service names are correct
- [ ] Icon types match services
- [ ] Pricing is current/accurate
- [ ] Integration patterns are valid

## Template: Architecture Design Document

```markdown
# [Domain] AI Agent System Architecture

## Business Context
- **Domain**:
- **Key Processes**:
- **Target Outcomes**:

## Agent Design

### Orchestrator
- **Name**:
- **Responsibilities**:
- **Model**: Cohere Command A

### Specialist Agents
| Agent | Purpose | Tools Used |
|-------|---------|------------|
| | | |

### Data Requirements
| Data Type | Source | Storage |
|-----------|--------|---------|
| | | |

## Cost Estimate
| Service | Monthly Cost |
|---------|--------------|
| | |
| **TOTAL** | |

## Diagram Layout
[Sketch or coordinates]
```

---

*Always complete this workflow BEFORE running the diagram generator.*
