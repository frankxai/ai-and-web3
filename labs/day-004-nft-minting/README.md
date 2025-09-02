# Day 004 — NFT Mint Pipeline

## Goals
- Create metadata, pin to IPFS, and mint an NFT on testnet
- Add agent steps for metadata validation and pinning

## Tasks
1) Generate image or reference asset
2) Create metadata JSON (name, description, image)
3) Pin to IPFS and record CID
4) Mint NFT referencing CID

## Acceptance criteria
- [ ] `runs/<timestamp>/ipfs.json` with CID
- [ ] `runs/<timestamp>/mint.json` receipt with tokenId
