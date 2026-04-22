import { SecureBridge } from "./index";
import * as fs from "fs";

async function main() {
  const publicKeyContent = fs.readFileSync("./keys/public.pem", "utf-8");
  const bridge = new SecureBridge(publicKeyContent);

  const payload = bridge.encrypt("1234567890123");

  console.log("Payload:", JSON.stringify(payload, null, 2));

  // call to backend "localhost:8000" on route "POST /ingest" with payload

  const response = await fetch("http://localhost:8000/ingest", {
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
