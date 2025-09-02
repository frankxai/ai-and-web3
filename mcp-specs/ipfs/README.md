# MCP IPFS (Draft Spec)

Tools
- ipfs_add(file|bytes, pin: bool) -> { cid }
- ipfs_get(cid) -> { bytes | filePath }
- ipfs_pin(cid) -> { pinned: bool }

Config
- Local or remote gateway, pinning service credentials optional
