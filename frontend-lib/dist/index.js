"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.SecureBridge = void 0;
const crypto_1 = require("crypto");
class SecureBridge {
    constructor(publicKey) {
        this.publicKey = publicKey;
    }
    encrypt(payload) {
        const aesKey = crypto_1.default.randomBytes(32);
        const iv = crypto_1.default.randomBytes(12);
        const cipher = crypto_1.default.createCipheriv("aes-256-gcm", aesKey, iv);
        let encrypted = cipher.update(payload, "utf8", "base64");
        encrypted += cipher.final("base64");
        const tag = cipher.getAuthTag();
        const encryptedKey = crypto_1.default.publicEncrypt({
            key: this.publicKey,
            padding: crypto_1.default.constants.RSA_PKCS1_OAEP_PADDING,
            oaepHash: "sha256",
        }, aesKey);
        return {
            encrypted_data: encrypted,
            encrypted_key: encryptedKey.toString("base64"),
            iv: iv.toString("base64"),
            tag: tag.toString("base64"),
            key_version: "v1",
        };
    }
}
exports.SecureBridge = SecureBridge;
