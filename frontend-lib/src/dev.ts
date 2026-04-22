import { SecureBridge } from "./index";
import * as fs from "fs";
import "dotenv/config";

async function main() {
  if (!process.env.VERIFICATION_SERVICE_PUBLIC_KEY) {
    throw new Error("VERIFICATION_SERVICE_PUBLIC_KEY is not defined");
  }
  if (!process.env.BACKEND_HOST) {
    throw new Error("BACKEND_HOST is not defined");
  }
  const publicKeyContent = fs.readFileSync(
    process.cwd() + "/" + process.env.VERIFICATION_SERVICE_PUBLIC_KEY,
    "utf-8",
  );
  const bridge = new SecureBridge(publicKeyContent);

  const payload = bridge.encrypt("1234567890125");

  console.log("Payload:", JSON.stringify(payload, null, 2));

  // call to backend "localhost:8000" on route "POST /ingest" with payload

  const response = await fetch(process.env.BACKEND_HOST + "/ingest", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  const result = await response.json();

  console.log(result);
}

main();
