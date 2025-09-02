#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from agents.tools.evm import get_balance, simulate_transfer, send_transfer


app = FastAPI(title="EVM Tool Server", version="0.1.0")


class BalanceIn(BaseModel):
    address: str = Field(pattern=r"^0x[0-9a-fA-F]{40}$")


class SimIn(BaseModel):
    to: str = Field(pattern=r"^0x[0-9a-fA-F]{40}$")
    value_wei: int = Field(ge=0)


class SendIn(SimIn):
    max_value_wei: Optional[int] = Field(default=None, ge=0)


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/evm/get_balance")
def api_get_balance(inp: BalanceIn):
    try:
        return get_balance(inp.address)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/evm/simulate_transfer")
def api_simulate(inp: SimIn):
    try:
        return simulate_transfer(inp.to, inp.value_wei)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/evm/send_transfer")
def api_send(inp: SendIn):
    try:
        return send_transfer(inp.to, inp.value_wei, inp.max_value_wei)
    except SystemExit as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Run: uvicorn agents.servers.evm_server:app --reload

