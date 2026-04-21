import crypto from "crypto";

export class SecureBridge {
    private publicKey: string;

    constructor(publicKey: string) {
        this.publicKey = publicKey;
    }

    encrypt(payload: string) {
        // 1. Generate AES key
        const aesKey = crypto.randomBytes(32); // AES-256

        // 2. Encrypt data with AES-GCM
        const iv = crypto.randomBytes(12);
        const cipher = crypto.createCipheriv("aes-256-gcm", aesKey, iv);

        let encrypted = cipher.update(payload, "utf8", "base64");
        encrypted += cipher.final("base64");

        const tag = cipher.getAuthTag();

        // 3. Encrypt AES key with RSA
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
            key_version: "v1"
        };
    }
}