#!/usr/bin/env node
import { getBalance, simulateTransfer, sendTransfer } from "@ai-web3/evm-tools";

function env(name: string) {
  const v = process.env[name];
  if (!v) throw new Error(`Missing env ${name}`);
  return v;
}

async function main() {
  const RPC_URL = env("RPC_URL");
  const PRIVATE_KEY = env("PRIVATE_KEY");
  const TO_ADDRESS = env("TO_ADDRESS") as `0x${string}`;
  const VALUE_WEI = BigInt(env("VALUE_WEI"));
  const MAX_VALUE_WEI = process.env["MAX_VALUE_WEI"] ? BigInt(env("MAX_VALUE_WEI")) : undefined;

  const FROM_ADDRESS = (await getBalance(RPC_URL, (env("FROM_ADDRESS") as `0x${string}`))).address;
  console.log("Plan: balance -> simulate -> send");

  const bal = await getBalance(RPC_URL, FROM_ADDRESS);
  console.log("Balance:", bal);

  const sim = await simulateTransfer(RPC_URL, PRIVATE_KEY as `0x${string}`, TO_ADDRESS, VALUE_WEI);
  if (!sim.ok) throw new Error("Simulation failed: " + sim.error);
  console.log("Simulation:", sim);

  const sent = await sendTransfer(RPC_URL, PRIVATE_KEY as `0x${string}`, TO_ADDRESS, VALUE_WEI, { maxValueWei: MAX_VALUE_WEI });
  console.log("Sent:", sent);
}

main().catch((e) => { console.error(e); process.exit(1); });

