### **UpPass Assignment: Secure Bridge Library & Python Backend**

**Role:** Technical Lead  
**Tech Stack:** TypeScript (Frontend), Python (Backend)  
**Context**  
At UpPass, trust is our currency. We are building a developer-friendly tool that allows our client's frontend applications to send sensitive Personally Identifiable Information (PII) to our servers securely. We require End-to-End (E2E) Encryption to ensure data is never exposed in transit, even to our internal load balancers.  
**Objective**

1. Develop a **Client-side TypeScript Library** to handle E2E encryption.  
2. Develop a **Python Backend** to receive, decrypt, and securely store data (with search capabilities).  
3. **Architectural Design:** Propose solutions for Key Lifecycle Management and Incident Response.

### ---

**Part 1: "UpPass Secure Bridge" (TypeScript Library)**

**Requirement:** Create a standalone TypeScript library (e.g., a class or module) that abstracts away the complexity of cryptography.

* **Core Logic (Hybrid Encryption):**  
  * The library must accept a Public Key (RSA/ECC) upon initialization.  
  * For every submission:  
    1. Generate a transient **Symmetric Key** (e.g., AES-256).  
    2. Encrypt the payload (National ID) with this Symmetric Key.  
    3. Encrypt the Symmetric Key itself using the Server's **Public Key**.  
    4. Return the packaged payload: { encrypted\_data: "...", encrypted\_key: "..." }.  
* **Deliverable:** A TypeScript file/module demonstrating this logic.

### **Part 2: The Python Verification Service (Backend)**

**Requirement:** Build a Python web service (FastAPI/Flask/Django) to handle the secure ingress.

* **Secure Ingress Endpoint:**  
  * Accept the encrypted payload from the library.  
  * **Decryption:** Use the Private Key to recover the Symmetric Key, then decrypt the data.  
* **Secure Storage (Blind Indexing):**  
  * **Column A (Storage):** Store the data using Randomized Encryption (different ciphertext every time).  
  * **Column B (Search Index):** Store the data using **HMAC-SHA256** (Deterministic) for exact matching.  
* **Search Endpoint:**  
  * Implement an API to search by National ID using the Blind Index approach (Exact match).

### **Part 3: System Design & Incident Response**

*Please provide a written document (Markdown) or a Diagram for the following scenarios:*

**Scenario A: Key Rotation Strategy**

"We need to rotate our Data Encryption Keys (DEK) annually for compliance. However, we have millions of encrypted records in the database."  
**Question:** Design a zero-downtime strategy to migrate these millions of records to the new key. How does the system know which key to use for decryption during the transition period? (Hint: Key Versioning).

**Scenario B: Data Leak Incident Response**

"A security audit reveals that a developer accidentally logged the 'Decrypted National ID' into our Cloud Logging system (e.g., CloudWatch/Stackdriver) for the past 24 hours."  
**Question:** As a Tech Lead, what are your immediate actions? How do you remediate the leak, and what technical controls would you implement to prevent this from happening again?

### ---

**Deliverables Checklist**

1. **Source Code:**  
   * /frontend-lib: TypeScript source code for the encryption library.  
   * /backend: Python service code (Dockerized).  
2. **Documentation (README.md):**  
   * Instructions to run the project.  
   * Deploy service on cloud service, e.g. Vercel  
   * Your answers/designs for **Scenario A (Key Rotation)** and **Scenario B (Data Leak)**.