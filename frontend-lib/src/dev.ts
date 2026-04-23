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

  
  const randomNumberString = ((ch: string, ln: number) =>
    Array(ln)
      .fill("")
      .map(() => ch[~~(Math.random() * ch.length)])
      .join(""))("0123456789", 13);
  // const randomNumberString='3000000000000'
  const payload = bridge.encrypt(randomNumberString);

  console.log("Random Number:", randomNumberString);
  console.log("Payload:", JSON.stringify(payload, null, 2));

  // call to backend "localhost:8000" on route "POST /store" with payload

  const response = await fetch(process.env.BACKEND_HOST + "/store", {
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
