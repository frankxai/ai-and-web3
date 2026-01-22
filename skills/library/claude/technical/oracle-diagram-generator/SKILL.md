# Oracle Diagram Generator - Professional Architecture Diagrams

## Overview

Generate professional Oracle Cloud Infrastructure architecture diagrams following official Oracle Architecture Center patterns and standards.

## Quick Start

```bash
# Generate all enterprise agent diagrams
python scripts/generate-oci-diagram.py --type all

# Generate specific diagram
python scripts/generate-oci-diagram.py --type marketing-agents
python scripts/generate-oci-diagram.py --type sales-agents
python scripts/generate-oci-diagram.py --type legal-agents
```

## Generated Diagrams

| Diagram | File | Description |
|---------|------|-------------|
| **Marketing Agents** | `docs/diagrams/oci-enterprise-marketing-agents.drawio` | 7 specialist agents: Content, SEO, Social, Email, Ads, Analytics, Persona |
| **Sales Agents** | `docs/diagrams/oci-enterprise-sales-agents.drawio` | 7 specialist agents: Lead, Research, Outreach, Proposal, Negotiation, Forecast, Coach |
| **Legal Agents** | `docs/diagrams/oci-enterprise-legal-agents.drawio` | 7 specialist agents: Contract, Research, Compliance, Review, Draft, IP, eDiscovery |

## CRITICAL: AI Architect Workflow

**ALWAYS follow the AI Architect workflow BEFORE generating diagrams.**

See: `AI_ARCHITECT_WORKFLOW.md`

### Workflow Phases
1. **Requirements Analysis** - Understand business domain and problems
2. **Agent Architecture Design** - Design agent hierarchy and types
3. **Data Flow Design** - Map inputs, outputs, persistence
4. **Cost Estimation** - Calculate monthly OCI costs
5. **Diagram Layout Planning** - Plan positioning and spacing
6. **Quality Checklist** - Verify standards compliance

---

## Oracle Official Standards (CRITICAL)

### Icon Sizing
| Element | Size | Notes |
|---------|------|-------|
| Service Icons | **85px** | Never smaller! |
| Labels | Below icon | Centered, 140px width |

### Font Sizes (ONLY TWO)
| Element | Size |
|---------|------|
| Headers/Labels | **16px bold** |
| Icon Labels | **14px regular** |
| Sublabels | **14px italic** |

**Never use fonts smaller than 14px**

### Official Oracle Color Palette
| Color | Hex | Usage |
|-------|-----|-------|
| Text/Labels | `#312D2A` | All text |
| Borders | `#9E9892` | Connectors, containers |
| Region Background | `#F5F4F2` | OCI Region fill |
| Oracle Red | `#C74634` | Accent, hub background |
| White | `#FFFFFF` | Icon backgrounds |

### Layer Color Coding
| Layer | Background | Border |
|-------|------------|--------|
| Hub | `#C74634` | `#312D2A` |
| Orchestrator | `#FFF5F3` | `#C74634` |
| Specialists | `#E3F2FD` | `#1565C0` |
| Tools | `#E8F5E9` | `#2E7D32` |
| Data | `#FFF3E0` | `#E65100` |

### Spacing Standards
| Element | Spacing |
|---------|---------|
| Horizontal (icon to icon) | **160px** |
| Vertical (row to row) | **140px** |
| Icon to label | **10px** |
| Container padding | **30-40px** |

---

## Icon Library Reference

### OCI Library Location
```
docs/diagrams/templates/OCI Library.xml  # 224 icons
```

### Key Icon Indices
| Service | Index | Type |
|---------|-------|------|
| GenAI/AI | 60 | `ai` |
| Functions | 2 | `functions` |
| VM | 3 | `vm` |
| Autonomous DB | 37 | `adb` |
| Object Storage | 11 | `object_storage` |
| API Gateway | 79 | `api_gateway` |
| Streaming | 65 | `streaming` |
| Vault | 105 | `vault` |
| Integration | 81 | `integration` |
| Load Balancer | 18 | `load_balancer` |
| Data Integration | 63 | `data_integration` |
| Notifications | 82 | `notifications` |

---

## Standard Architecture Layout

### Y-Coordinate Grid
```
Y=80:   Agent Hub (centered, Oracle Red)
Y=200:  Orchestrator Layer
Y=330:  Specialist Agent Pool
Y=510:  Tool Layer
Y=660:  Data Layer
```

### Canvas Dimensions
- **Width**: 1400-1600px
- **Height**: 800-1000px

### Layer Structure
```
┌─────────────────────────────────────────────────────────┐
│  OCI Region (fillColor=#F5F4F2, stroke=#9E9892)        │
│                                                         │
│    ┌─────────────────────────────────────┐             │
│    │        AGENT HUB (Oracle Red)        │             │
│    │         OCI GenAI Hub Icon           │             │
│    └─────────────────────────────────────┘             │
│                        │                                │
│    ┌─────────────────────────────────────┐             │
│    │    ORCHESTRATOR (light pink)         │             │
│    │   [Planner]    [Analyzer]            │             │
│    └─────────────────────────────────────┘             │
│                        │                                │
│    ┌─────────────────────────────────────────────────┐ │
│    │       SPECIALIST AGENTS (light blue)             │ │
│    │  [Agent1] [Agent2] [Agent3] ... [AgentN]         │ │
│    └─────────────────────────────────────────────────┘ │
│                        │                                │
│    ┌─────────────────────────────────────────────────┐ │
│    │          TOOLS (light green)                     │ │
│    │  [CRM] [APIs] [Functions] [Integrations]         │ │
│    └─────────────────────────────────────────────────┘ │
│                        │                                │
│    ┌─────────────────────────────────────────────────┐ │
│    │          DATA (light orange)                     │ │
│    │    [ADB 26ai]  [Object Storage]  [Vault]         │ │
│    └─────────────────────────────────────────────────┘ │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Connector Standards

### Style
```xml
edgeStyle=orthogonalEdgeStyle;rounded=1;curved=1;strokeColor=#9E9892;strokeWidth=1.5;
```

### Labels
Use action-oriented descriptions:
- ✅ "generate content"
- ✅ "fetch customer data"
- ✅ "analyze performance"
- ❌ "data" (too vague)
- ❌ "connection" (meaningless)

---

## Python Generator Usage

### Adding New Diagram Types

```python
def create_my_agent_system() -> OCIDiagramGenerator:
    """My Custom Agent System"""
    gen = OCIDiagramGenerator("My Agent System Title", 1500, 900)

    # Add containers (layers)
    gen.add_container(Container('hub_layer', 580, 80, 340, 100, 'INTELLIGENCE HUB',
                                ORACLE_COLORS['oracle_red'], ORACLE_COLORS['text'], ORACLE_COLORS['white']))

    # Add icons
    gen.add_icon(Icon('hub', 'ai', 710, 100, 'OCI GenAI', 'Cohere Command A'))

    # Add more agents, tools, data...

    return gen
```

### Icon Types Available
```python
ICON_INDICES = {
    'ai': 60,           # For GenAI agents
    'functions': 2,     # Serverless compute
    'vm': 3,            # Virtual machines
    'adb': 37,          # Autonomous Database
    'object_storage': 11,
    'api_gateway': 79,
    'streaming': 65,
    'vault': 105,
    'integration': 81,
    'load_balancer': 18,
    'data_integration': 63,
    'notifications': 82,
}
```

---

## Quality Checklist

Before finalizing any diagram:

### Visual Standards
- [ ] All icons are 85px size
- [ ] All fonts are 14-16px
- [ ] Colors match Oracle palette exactly
- [ ] Consistent 160px horizontal spacing
- [ ] Labels centered below icons

### Architecture Quality
- [ ] Clear Hub → Orchestrator → Specialists hierarchy
- [ ] Each agent has distinct purpose
- [ ] Connector labels describe actions
- [ ] Cost estimate box included
- [ ] OCI Region container present

### Technical Accuracy
- [ ] OCI service names correct
- [ ] Icon types match services
- [ ] Pricing current (check docs.oracle.com)
- [ ] Integration patterns valid

---

## Official Oracle Resources

### Download Links
- **Draw.io Toolkit**: https://docs.oracle.com/iaas/Content/Resources/Assets/OCI-Style-Guide-for-Drawio.zip
- **Architecture Center**: https://docs.oracle.com/en/solutions/
- **RAG Reference**: https://docs.oracle.com/en/solutions/implement-rag-oci/

### Local Resources
```
docs/diagrams/
├── templates/
│   ├── OCI Architecture Diagram Toolkit v24.2.drawio
│   └── OCI Library.xml
├── oracle-reference/
│   ├── rag-oic-oracle/
│   └── rag-oic-aug-gen-oracle/
├── ORACLE_DIAGRAM_STANDARDS.md
└── [generated diagrams]
```

---

## Related Skills

- **oracle-ai-architect** - AI architecture patterns
- **oci-services-expert** - OCI service pricing and capabilities
- **oracle-adk** - Agent Development Kit patterns

---

*Always think architecture first, then generate diagrams.*
