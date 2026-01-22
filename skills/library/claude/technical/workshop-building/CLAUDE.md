# Workshop Building Skill
**Version**: 1.0.0
**Category**: Technical + Education
**Agentic-Creator-OS Integration**: Full

---

## Purpose

Master skill for creating comprehensive, hands-on technical workshops that transform learners from beginners to practitioners. Designed for the FrankX Workshop System, integrating with GitHub repositories, frankx.ai/workshops, and the Agentic-Creator OS intelligence systems.

## Core Philosophy

> "The best workshop doesn't just teach—it transforms. Every participant leaves with working code, deep understanding, and the confidence to build on their own."

### The FrankX Workshop Methodology

```
┌──────────────────────────────────────────────────────────────┐
│                 WORKSHOP TRANSFORMATION LOOP                  │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│   DISCOVER ──────► UNDERSTAND ──────► BUILD ──────► MASTER   │
│       │                │                │              │      │
│   Curiosity         Concepts         Practice       Fluency  │
│   Sparked           Grasped          Applied        Achieved │
│                                                               │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  Quality Gates at Each Stage Ensure Progression     │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## Workshop Architecture

### Directory Structure

```
workshops/
├── README.md                    # Workshop catalog and navigation
├── _templates/                  # Reusable workshop templates
│   ├── module-template.md       # Standard module structure
│   ├── lab-template.md          # Hands-on lab structure
│   └── assessment-template.md   # Knowledge check templates
│
├── ai-coding-agents/            # Workshop: AI Coding Agents Mastery
│   ├── README.md                # Workshop overview
│   ├── 00-prerequisites/        # Setup requirements
│   ├── 01-foundations/          # Core concepts
│   ├── 02-setup-guides/         # Tool installation
│   ├── 03-first-agent/          # First project
│   ├── 04-advanced/             # Advanced patterns
│   ├── 05-evolution/            # skill.md → agent.md → orchestration
│   ├── labs/                    # Hands-on exercises
│   ├── projects/                # Capstone projects
│   └── resources/               # Additional materials
│
├── mcp-server-mastery/          # Workshop: MCP Server Architecture
├── oracle-genai-enterprise/     # Workshop: Oracle GenAI for Enterprise
├── agentic-creator-evolution/   # Workshop: From Beginner to Master
└── quality-gates/               # Shared quality assessment system
    ├── progress-tracker.md      # Track learner progress
    ├── skill-assessments/       # Test comprehension
    └── completion-criteria.md   # Graduation requirements
```

### Workshop Module Structure

Each module follows this pattern:

```markdown
# Module X: [Title]

## Learning Objectives
- [ ] Objective 1 (measurable)
- [ ] Objective 2 (actionable)
- [ ] Objective 3 (demonstrable)

## Prerequisites
- Previous module completion
- Required tools/access

## Concepts (UNDERSTAND)
[Theory and explanation - 20% of content]

## Demonstration (OBSERVE)
[Walkthrough with explanations - 30% of content]

## Lab Exercise (BUILD)
[Hands-on practice - 40% of content]

## Assessment (VERIFY)
[Knowledge check - 10% of content]

## Next Steps
[Pathway to next module]
```

---

## Workshop Types

### 1. Quick Start Labs (30 min - 2 hours)
- Single focused skill
- Immediate hands-on
- Clear outcome
- Example: "Set Up Claude Code in 30 Minutes"

### 2. Deep Dive Modules (2-4 hours)
- Comprehensive topic coverage
- Multiple exercises
- Builds on prerequisites
- Example: "MCP Server Architecture Deep Dive"

### 3. Full Workshops (1-3 days)
- Complete transformation journey
- Multiple modules
- Capstone project
- Example: "AI Coding Agents Mastery Workshop"

### 4. Evolution Pathways (Ongoing)
- Progressive skill building
- Milestone achievements
- Community progression
- Example: "Agentic Creator Evolution Path"

---

## Quality Gates System

### Per-Module Gates

```yaml
module_quality_gates:
  content:
    - concepts_clear: true
    - code_examples_working: true
    - labs_tested: true
    - assessments_validated: true

  experience:
    - estimated_time_accurate: true
    - difficulty_appropriate: true
    - prerequisites_documented: true

  outcomes:
    - learning_objectives_measurable: true
    - hands_on_percentage: ">= 40%"
    - real_world_applicability: true
```

### Workshop-Level Gates

```yaml
workshop_quality_gates:
  structure:
    - logical_progression: true
    - no_prerequisite_gaps: true
    - capstone_integrates_all: true

  accessibility:
    - beginner_friendly_entry: true
    - advanced_paths_available: true
    - multiple_learning_styles: true

  completeness:
    - all_tools_documented: true
    - troubleshooting_included: true
    - next_steps_clear: true
```

---

## Creating a New Workshop

### Step 1: Define the Transformation

```markdown
## Workshop Planning Template

### Target Audience
- Who is this for?
- Current skill level?
- Goals and motivations?

### Transformation Promise
- What can they do BEFORE?
- What can they do AFTER?
- How long does it take?

### Success Metrics
- Completion criteria
- Skill assessments
- Real-world application proof
```

### Step 2: Map the Learning Journey

```
DISCOVERY PHASE
├── Hook: Why this matters
├── Overview: What we'll build
└── Quick win: First 10 minutes

FOUNDATION PHASE
├── Core concepts
├── Mental models
└── Terminology

BUILD PHASE
├── Guided labs
├── Independent exercises
└── Troubleshooting

MASTERY PHASE
├── Capstone project
├── Real-world application
└── Community sharing
```

### Step 3: Create Content with Quality Gates

Each piece of content must pass:

1. **Clarity Check**: Can a beginner understand this?
2. **Accuracy Check**: Is the code/info correct and current?
3. **Completeness Check**: Are all steps documented?
4. **Testing Check**: Has someone successfully followed this?

---

## Integration Points

### GitHub Integration

Workshops live in `FrankX-Workshops` repository:
- Version controlled content
- Issue tracking for feedback
- PR workflow for updates
- Actions for validation

### FrankX.AI Integration

Workshops displayed at `frankx.ai/workshops`:
- Interactive progress tracking
- Community discussion
- Achievement system
- Certificate generation

### Agentic-Creator OS Integration

Workshop content feeds into:
- Skill development tracking
- Agent training data
- Knowledge base expansion
- Evolution pathway

### OpenCode ACOS Integration

Same skill available in:
- `.opencode/agents/workshop-builder.md`
- Cross-platform consistency
- Shared quality gates

---

## Workshop Content Guidelines

### Voice and Tone

- **Authoritative but approachable**: Expert guidance without intimidation
- **Action-oriented**: Focus on doing, not just reading
- **Encouraging**: Celebrate progress, normalize challenges
- **Practical**: Real-world applications, not academic exercises

### Code Standards

```markdown
## Code Block Requirements

1. **Complete and runnable**: No pseudo-code in labs
2. **Well-commented**: Explain the "why" not just "what"
3. **Tested**: All code verified working
4. **Copy-friendly**: Easy to copy and execute
```

### Visual Standards

- Architecture diagrams for complex concepts
- Progress indicators for multi-step processes
- Before/after comparisons for transformations
- Terminal screenshots for setup verification

---

## Workshop Templates

### Quick Start Template

```markdown
# Quick Start: [Topic]

**Time**: 30 minutes
**Level**: Beginner
**Outcome**: [What they'll have working]

## Prerequisites
- [Minimal requirements]

## Step 1: [Action] (5 min)
[Clear instructions]

## Step 2: [Action] (10 min)
[Clear instructions]

## Step 3: [Action] (10 min)
[Clear instructions]

## Verify It Works
[How to test success]

## Next Steps
[Where to go from here]
```

### Deep Dive Template

```markdown
# [Topic] Deep Dive

**Duration**: 3-4 hours
**Level**: Intermediate
**Prerequisites**: [List]

## Overview
[Why this matters, what you'll learn]

## Part 1: Concepts (45 min)
### 1.1 [Concept]
### 1.2 [Concept]
### 1.3 [Concept]

## Part 2: Hands-On (2 hours)
### Lab 1: [Title]
### Lab 2: [Title]
### Lab 3: [Title]

## Part 3: Real-World Application (45 min)
### Project: [Title]
### Best Practices
### Common Pitfalls

## Assessment
[Knowledge check]

## Resources
[Further learning]
```

---

## When to Use This Skill

- Creating new technical workshops
- Structuring educational content
- Building learning pathways
- Designing hands-on labs
- Integrating with FrankX workshop system

## Related Skills

- `mcp-architecture` - For MCP-focused workshops
- `claude-sdk` - For Agent SDK workshops
- `oracle-adk` - For Oracle ADK workshops
- `frankx-brand` - For voice and tone alignment
- `ui-ux-design-expert` - For workshop UI/UX

---

## Activation Commands

```bash
# Create new workshop
/workshop-building create [workshop-name]

# Generate module
/workshop-building module [workshop-name] [module-number]

# Validate workshop quality
/workshop-building validate [workshop-name]

# Generate workshop landing page
/workshop-building landing [workshop-name]
```

---

*This skill embodies the FrankX mission: transforming creators from tech-overwhelmed to AI-empowered through hands-on, soul-aligned learning experiences.*
