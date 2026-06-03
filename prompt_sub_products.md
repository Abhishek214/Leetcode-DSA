# PROMPT: INTERNET / ELECTRONIC BANKING — SUB-PRODUCT EXTRACTION

## OBJECTIVE
Extract structured Sub-Product information (electronic/digital banking powers and their associated signing rules) from Board Resolution (BR) and Minutes of Meeting (MoM) documents related to internet and electronic banking, with 100% accuracy and zero hallucination. Output must strictly follow the JSON structure defined at the end of this prompt.

---

## CRITICAL INSTRUCTIONS — READ CAREFULLY

---

### 1. SCOPE, SOURCE VALIDATION & ANTI-HALLUCINATION

ONLY extract information from the Board Resolution or Minutes of Meeting sections (including their Annexes, Schedules, or Cover Letters). NEVER infer, assume, or generate information not explicitly stated in the document.

**ANTI-HALLUCINATION RULE:** NEVER copy text from the examples or instructions within this prompt (e.g., "Authorise third parties...", "Reset of login PIN", "Any 1 Officer Signatory") and present it as extracted data. All extracted text MUST originate exclusively from the physical document.

If information is absent or unclear, return `"N/A"`. DO NOT create placeholder data or fictional entries.

---

### 2. PRODUCT TYPE IDENTIFICATION (STRICT ABORT CONDITION)

Identify the product type by detecting keywords in the actual document text. For now only one product type is supported:

**"Internet / Electronic Banking"** — identified by the literal presence of any of the following keywords in the document:
- `appointed System Administrators`, `make changes to the online banking profile`, `subscribe for electronic banking`
- `electronic banking services`, `internet banking services`, `electronic banking`, `electronic platforms`
- `E-banking`, `HSBCnet`, `H2H`, `API's`, `channels`

If these keywords are found, set: `"product_type": "Internet / Electronic Banking"`

> **CRITICAL ABORT RULE:** If none of these specific keywords are physically present in the document text, the document is a general banking document. You MUST NOT extract any sub-products. Return EXACTLY:
> ```json
> {"Accounts": []}
> ```
> and **STOP processing immediately.**

---

### 3. PRODUCT CATEGORY IDENTIFICATION (AP ONLY)

For Internet / Electronic Banking, only the **AP (Authorised Person)** category is applicable.

A person is identified as AP if the document describes them as having general authority to represent the customer, open accounts, sign terms, and make mandate changes.

Keywords identifying AP powers:
- Subscribe for electronic banking channels or platforms
- Authorise third parties to manage the Channels
- Appoint administrators and manage authorisation levels, delegate authority
- signs contracts, legally possible to resolve, again, delegate, acting on behalf, represent, negotiate, draft and sign documents, appoint/revoke, open and manage, close.

**RULE:** Always set `"product_category": "AP"` for all extracted entries.

---

### 4. ACCOUNT NUMBER EXTRACTION RULES (MAPPED VS UNMAPPED LOGIC)

Look for global or general "Signatory Lists", "Annexes", "Schedules", or Cover Letters located elsewhere in the document that list the company's account numbers. Extract specific account numbers that follow standard banking account number formats (e.g., `21345060`, `21345052`, `7891-2345-6789`, `808-772438-001`).

**PRODUCT EXCLUSION RULE:** Do NOT extract account numbers that are explicitly and exclusively designated for non-electronic banking products (e.g., "Payroll", "Opex", "Cheques", "Corporate Cards").

**MAPPING LOGIC:**

**SCENARIO A (MAPPED/CORRESPONDING):** If the document explicitly maps specific lists of authorised persons to particular account numbers (e.g., a table where each column is a different account number with its own specific signatories), you MUST create a distinct and separate object in the `"Accounts"` array for EACH individual account number. `"Account Number"` will be an array containing just that one account number (e.g., `["21345060"]`).

**SCENARIO B (UNMAPPED/GLOBAL):** If multiple account numbers are listed (e.g., in a cover letter or header) and a single global resolution or sub-product list applies to all of them, you MUST group all of these account numbers into ONE SINGLE JSON object. Place all account numbers into a list/array within the `"Account Number"` field (e.g., `["808-772420-001", "808-772430-292", "808-772438-001", "808-772438-292"]`). DO NOT create multiple duplicate JSON objects with the identical sub-product information.

- If the document explicitly mentions "All Accounts" or "All Bank Accounts" in relation to internet banking, set `"Account Number": ["All Accounts"]`.
- If absolutely no specific account number or "All Accounts" is mentioned anywhere in the document, or if the only accounts mentioned fall under the Product Exclusion Rule, set `"Account Number": ["N/A"]`.

---

### 5. SUB-PRODUCT IDENTIFICATION & POPULATION RULES

**SCANNING RULE — SEARCH THE ENTIRE DOCUMENT:**
Scan every individual clause, sub-clause, and bullet point across the entire document. When a section contains a numbered or lettered list, YOU MUST evaluate EACH lettered/numbered item SEPARATELY. NEVER reject an entire list block because some items are general banking powers.

A clause is ONLY extracted as a Sub-Product if it passes **BOTH** gates:

**GATE 1 — The clause itself MUST explicitly contain at least one of these terms:**
- `internet banking` / `internet banking facilities`
- `electronic banking` / `electronic banking facilities`
- `electronic banking platforms` / `electronic platforms`
- `electronic banking systems` / `connectivity channels`
- `System Administrator(s)`
- `online banking profile`
- `E-banking` / `HSBCnet` / `H2H` / `API's`
- `Channels` / `E-channels` (in a digital context)
- `authorisation levels` (on a digital platform)
- `user access` (in context of banking platforms)
- `login PIN` / `token administration`

**GATE 2 — Ask: "Would this power exist even without internet/electronic banking?"**
- If **YES** = **REJECT**
- If **NO** = **ACCEPT**

**Step 1** — Link qualifying sub-products to each Account Number object determined in Section 4.
**Step 2** — Each qualifying sub-product gets its own object in the `"Sub-Products"` array with its own `"Signing Rule"` array.

If no clauses pass both gates, set `"Sub-Products": []`.

---

### 6. SIGNING RULE EXTRACTION

- **`"Signing Limit"`** — Capture the exact text outlining constraints, limits, or amounts. If left blank or marked with a dash (`"–"`) → use `"N/A"`.
- **`"Signing Rule"`** — Capture the exact signing pattern or authorised persons assigned to the power.

**Rules:** Capture exact limits and persons — NEVER round, infer, or modify.

---

### 7. PROCESSING WORKFLOW — FOLLOW THIS ORDER

1. Detect product type using keywords → if NO explicit keywords found in the document, return `{"Accounts": []}` and **STOP**.
2. Scan the entire document for Account Numbers. Apply the Product Exclusion Rule.
3. Apply Mapping Logic:
   - **Scenario A:** Create a distinct JSON object for EACH explicitly mapped account number.
   - **Scenario B:** Create ONE SINGLE JSON object and include ALL account numbers in a list/array.
4. Scan every individual clause against the **GATE 1** and **GATE 2** filtering rules.
5. ONLY extract qualifying electronic/digital banking clauses as Sub-Products.
6. Extract Signing Limits and Signing Rules per Sub-Product.
7. Validate against the Quality Assurance Checklist below.

---

## OUTPUT JSON STRUCTURE (GENERALIZED EXAMPLE)

```json
{
  "Accounts": [
    {
      "product_type": "Internet / Electronic Banking",
      "product_category": "AP",
      "Account Number": ["12345678", "87654321"],
      "Sub-Products": [
        {
          "Sub-Product (Signing Power)": "<Exact clause text from document>",
          "Signing Rule": [
            {
              "Signing Limit": "<Exact limit text, or N/A>",
              "Signing Rule": "<Exact signing pattern from document>"
            },
            {
              "Signing Limit": "<Exact limit text, or N/A>",
              "Signing Rule": "<Exact signing pattern from document>"
            }
          ]
        }
      ]
    }
  ]
}
```

---

## QUALITY ASSURANCE CHECKLIST

Before submitting output, verify:

- [ ] **ANTI-HALLUCINATION CHECK:** Are all sub-products and signing rules verbatim from the document? If they look identical to the prompt's examples, delete them.
- [ ] **PRODUCT TYPE CHECK:** Were the electronic banking keywords explicitly found? If not, output must be `{"Accounts": []}`.
- [ ] **PRODUCT EXCLUSION CHECK:** No account numbers were extracted from tables explicitly labeled for non-electronic products like "Payroll" or "Opex".
- [ ] **MAPPED VS UNMAPPED CHECK:** Account numbers sharing the same sub-product list MUST be combined into a single object's `"Account Number"` array. No duplicate objects were created.
- [ ] **SUB-PRODUCT GATE CHECK:** Every extracted sub-product contains a GATE 1 keyword AND fails the GATE 2 test.
- [ ] **SIGNING RULE CHECK:** Signing limits and rules are exact verbatim extractions — nothing rounded, inferred, or modified.

---

## ERROR PREVENTION RULES

**NEVER:**
- Copy text from the prompt's examples and output it as extracted data.
- Create separate, identical JSON objects for multiple account numbers unless the document explicitly maps them to different signatory lists.
- Extract sub-products that do not explicitly contain a GATE 1 keyword.
- Include a `"List of Authorised Person"` field in this output.
- Round, infer, or modify signing limits or signing rules.

**ALWAYS:**
- Return `{"Accounts": []}` if electronic banking keywords (`"electronic banking"`, `"internet banking"`, `"channels"`, `"HSBCnet"`, etc.) are not explicitly found in the document.
- Group account numbers into a list/array within ONE single object if they share the same global sub-product resolution.
- Strictly bound Sub-Product extraction to clauses directly modifying electronic Channels or digital platforms.
- Extract exact text as written for powers and limits.
