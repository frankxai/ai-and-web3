import { createPublicClient, createWalletClient, http, parseEther, formatEther } from "viem";
import { mainnet, sepolia } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

export type Chain = typeof mainnet | typeof sepolia;

export function getPublicClient(rpcUrl: string, chain: Chain = sepolia) {
  return createPublicClient({ chain, transport: http(rpcUrl) });
}

export function getWalletClient(pk: string, rpcUrl: string, chain: Chain = sepolia) {
  const account = privateKeyToAccount(pk as `0x${string}`);
  return createWalletClient({ account, chain, transport: http(rpcUrl) });
}

export async function getBalance(rpcUrl: string, address: `0x${string}`, chain: Chain = sepolia) {
  const pc = getPublicClient(rpcUrl, chain);
  const bal = await pc.getBalance({ address });
  return { address, wei: bal.toString(), ether: formatEther(bal) };
}

export async function simulateTransfer(
  rpcUrl: string,
  fromPk: `0x${string}`,
  to: `0x${string}`,
  valueWei: bigint,
  chain: Chain = sepolia
) {
  const pc = getPublicClient(rpcUrl, chain);
  const wc = getWalletClient(fromPk, rpcUrl, chain);
  try {
    const gas = await pc.estimateGas({ account: wc.account!, to, value: valueWei });
    return { ok: true, estimatedGas: gas.toString() };
  } catch (e: any) {
    return { ok: false, error: String(e) };
  }
}

export async function sendTransfer(
  rpcUrl: string,
  fromPk: `0x${string}`,
  to: `0x${string}`,
  valueWei: bigint,
  opts: { maxValueWei?: bigint } = {},
  chain: Chain = sepolia
) {
  if (opts.maxValueWei && valueWei > opts.maxValueWei) {
    throw new Error("Policy violation: exceeds maxValueWei");
  }
  const wc = getWalletClient(fromPk, rpcUrl, chain);
  const hash = await wc.sendTransaction({ to, value: valueWei });
  return { txHash: hash };
}

