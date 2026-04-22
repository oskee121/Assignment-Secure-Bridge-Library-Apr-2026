import { SecureBridge } from "./index";
import * as fs from "fs";

const publicKeyContent = fs.readFileSync("./keys/public.pem", "utf-8");
const bridge = new SecureBridge(publicKeyContent);

const result = bridge.encrypt("1234567890123");

console.log(result);
