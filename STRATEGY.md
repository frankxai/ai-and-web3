# Strategy: ai-and-web3

## Vision
Make ai-and-web3 the most trusted, practical, and reproducible home for AI agents that operate on-chain.

## Positioning
- The TypeScript-first, evaluation-driven repo for AI + Web3 agents.
- Focus on reproducible labs, measurable outcomes, and production safety.
- Clear gap: few repos combine agent frameworks with real on-chain tasks and evals.

## Target audiences
- Builders shipping Web3 agents and wallets
- Researchers comparing agent frameworks on real tasks
- Teams needing safe, repeatable automation on-chain

## Product pillars
1) Agents and labs
- Small, composable agents that do one thing well (wallet ops, indexing, swaps, governance)
- Day-by-day labs with acceptance criteria and reproducible scripts

2) Tooling and MCP layer
- A consistent tool registry for RPC, storage, governance, and observability
- First-class MCP specs and server implementations

3) Evaluation and benchmarks
- Standard eval harness for cost, latency, success, and safety
- Comparative matrix for frameworks across identical tasks

4) Safety and policy
- Spend limits, dry runs, simulation gates, and approval workflows
- Clear threat model and guardrail docs

5) Docs and playbooks
- Fast onboarding guides, diagrams, and recipes
- Production playbooks for common Web3 tasks

## Build plan (next 90 days)

### Phase 1: Foundation and visibility (Weeks 1-3)
- Refresh README with clear value prop, quickstart, and links to landscape and strategy
- Publish Landscape doc with top repos and gaps
- Add issue templates and a simple contribution workflow
- Establish a minimal eval harness and one published benchmark

### Phase 2: Core agents and labs (Weeks 4-7)
- Ship 3-5 runnable agents (wallet ops, on-chain data, DAO proposal, NFT mint)
- Add TypeScript-first CLIs with predictable inputs and outputs
- Expand labs with acceptance checklists and artifacts

### Phase 3: MCP and eval expansion (Weeks 8-12)
- Implement MCP servers for EVM, IPFS, The Graph, Dune (or wrappers)
- Publish cross-framework evals on identical tasks
- Add safety guardrails (spend limits, policy gating)

## Longer-term bets (Quarter+)
- Cross-chain agent flows (EVM + Solana) with shared patterns
- Intent routing and account abstraction playbooks
- Verifiable inference or audit trails for high-value actions

## Growth and distribution
- Monthly release notes and demo videos (short, task-focused)
- Quarterly landscape refresh and benchmark update
- Community pull requests with labeled issues and good first issues

## Success metrics
- Repo activity: stars, forks, contributors, and issue velocity
- Benchmarks: number of evaluated frameworks and published results
- Adoption: number of labs run (proxy: downloads, workflow usage)

## Governance
- Define maintainer roles and review process
- Protect main with required checks and release tagging
