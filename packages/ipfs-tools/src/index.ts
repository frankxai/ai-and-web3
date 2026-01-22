import { create, type IPFSHTTPClient } from "ipfs-http-client";

export function getIpfsClient(url: string): IPFSHTTPClient {
  return create({ url });
}

export async function addJson(url: string, data: any) {
  const client = getIpfsClient(url);
  const { cid } = await client.add(JSON.stringify(data));
  return { cid: cid.toString() };
}
