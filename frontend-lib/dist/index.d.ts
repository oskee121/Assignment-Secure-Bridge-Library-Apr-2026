export interface EncryptedPayload {
    encrypted_data: string;
    encrypted_key: string;
    iv: string;
    tag: string;
    key_version: string;
}
export declare class SecureBridge {
    private publicKey;
    constructor(publicKey: string);
    encrypt(payload: string): EncryptedPayload;
}
