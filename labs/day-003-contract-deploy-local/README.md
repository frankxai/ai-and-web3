# Day 003 — Local Contract Deploy (Anvil)

## Goals
- Stand up Anvil and deploy a simple Solidity contract
- Interact with it via an agent step (read/write fn)

## Tasks
1) Launch `anvil`
2) Compile + deploy `Counter.sol` (or similar)
3) Call `increment()` and verify state
4) Capture artifacts (address, abi, receipt)

## Acceptance criteria
- [ ] `runs/<timestamp>/deploy.json` with address and bytecode hash
- [ ] `runs/<timestamp>/calls.json` with return values

## Foundry quickstart
- Install Foundry, then:
- `cd labs/day-003-contract-deploy-local`
- `forge build`
- `anvil` (in a new terminal)
- `forge script script/Deploy.s.sol:Deploy --rpc-url http://127.0.0.1:8545 --private-key <ANVIL_KEY> --broadcast`

Record the deployed address and interact via `cast call` or a small script.
