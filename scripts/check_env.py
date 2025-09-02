#!/usr/bin/env python3
import os

REQUIRED = [
    ("Day001", ["EVM_RPC_URL", "PRIVATE_KEY"]),
    ("Day003", ["EVM_RPC_URL", "PRIVATE_KEY", "COUNTER_ADDRESS"]),
    ("Day004", ["EVM_RPC_URL", "PRIVATE_KEY", "ERC721_ADDRESS", "TOKEN_URI"]),
]

missing = []
for name, keys in REQUIRED:
    for k in keys:
        if not os.environ.get(k):
            missing.append((name, k))

if missing:
    print("Missing env vars:")
    for name, k in missing:
        print(f"- {name}: {k}")
    raise SystemExit(1)
else:
    print("All required env vars present for Day001/3/4")

