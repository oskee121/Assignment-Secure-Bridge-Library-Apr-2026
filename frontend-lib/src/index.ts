import * as crypto from "crypto";

export interface EncryptedPayload {
    encrypted_data: string;
    encrypted_key: string;
    iv: string;
    tag: string;
    key_version: string;
}

export class SecureBridge {
    constructor(private publicKey: string) {}

    encrypt(payload: string): EncryptedPayload {
        console.log('Start encrypt');
        const aesKey = crypto.randomBytes(32);

        const iv = crypto.randomBytes(12);
        const cipher = crypto.createCipheriv("aes-256-gcm", aesKey, iv);

        let encrypted = cipher.update(payload, "utf8", "base64");
        encrypted += cipher.final("base64");

        const tag = cipher.getAuthTag();

        const encryptedKey = crypto.publicEncrypt(
            {
                key: this.publicKey,
                padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
                oaepHash: "sha256",
            },
            aesKey
        );

        return {
            encrypted_data: encrypted,
            encrypted_key: encryptedKey.toString("base64"),
            iv: iv.toString("base64"),
            tag: tag.toString("base64"),
            key_version: "v1",
        };
    }
}