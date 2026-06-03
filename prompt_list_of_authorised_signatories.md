# PROMPT: INTERNET / ELECTRONIC BANKING — LIST OF AUTHORISED SIGNATORIES EXTRACTION

## OBJECTIVE
Extract structured List of Authorised Person (signatory) information from Board Resolution (BR) and Minutes of Meeting (MoM) documents related to internet and electronic banking, with 100% accuracy and zero hallucination. Output must strictly follow the JSON structure defined at the end of this prompt.

---

## CRITICAL INSTRUCTIONS — READ CAREFULLY

---

### 1. SCOPE, SOURCE VALIDATION & ANTI-HALLUCINATION

ONLY extract information from the Board Resolution or Minutes of Meeting sections (including their Annexes, Schedules, or Cover Letters). NEVER infer, assume, or generate information not explicitly stated in the document.

**ANTI-HALLUCINATION RULE:** NEVER copy text from the examples or instructions within this prompt and present it as extracted data. All extracted text MUST originate exclusively from the physical document.

If information is absent or unclear, return `"N/A"`. DO NOT create placeholder data or fictional entries.

---

### 2. PRODUCT TYPE IDENTIFICATION (STRICT ABORT CONDITION)

Identify the product type by detecting keywords in the actual document text. For now only one product type is supported:

**"Internet / Electronic Banking"** — identified by the literal presence of any of the following keywords in the document:
- `appointed System Administrators`, `make changes to the online banking profile`, `subscribe for electronic banking`
- `electronic banking services`, `internet banking services`, `electronic banking`, `electronic platforms`
- `E-banking`, `HSBCnet`, `H2H`, `API's`, `channels`

If these keywords are found, set: `"product_type": "Internet / Electronic Banking"`

> **CRITICAL ABORT RULE:** If none of these specific keywords are physically present in the document text, the document is a general banking document. You MUST NOT extract any signatory information. Return EXACTLY:
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

**SCENARIO B (UNMAPPED/GLOBAL):** If multiple account numbers are listed (e.g., in a cover letter or header) and a single global resolution or signatory list applies to all of them, you MUST group all of these account numbers into ONE SINGLE JSON object. Place all account numbers into a list/array within the `"Account Number"` field (e.g., `["808-772420-001", "808-772430-292", "808-772438-001", "808-772438-292"]`). DO NOT create multiple duplicate JSON objects with the identical signatory information.

- If the document explicitly mentions "All Accounts" or "All Bank Accounts" in relation to internet banking, set `"Account Number": ["All Accounts"]`.
- If absolutely no specific account number or "All Accounts" is mentioned anywhere in the document, or if the only accounts mentioned fall under the Product Exclusion Rule, set `"Account Number": ["N/A"]`.

---

### 5. LIST OF AUTHORISED PERSON (AP)

**Field Name:** `"List of Authorised Person"`

**CRITICAL INHERITANCE:** You MUST extract the comprehensive list of personnel from the document's main "Signatory List" or Annex. DO NOT limit this list to only the specific individuals named in the Electronic Banking section.

**PRODUCT EXCLUSION RULE:** Do NOT extract personnel from lists or tables that are explicitly designated for non-electronic banking products (e.g., "Payroll", "Opex"). If the only signatory lists available are explicitly for excluded products, return a single entry with `"Name": "N/A"` and all other fields as `"N/A"`.

#### Fields to Extract Per Person

| Field | Description |
|---|---|
| **Name** | Full human name. EXCLUDE salutations and titles (e.g. remove "Mr.", "Mrs.", "Ms.", "Dr.", "Prof.") |
| **Action** | Normalized action — see Action Normalization Rules below |
| **ID Number** | Government ID if present, otherwise `'N/A'` |
| **Designation** | Position/Role/Title (e.g., CFO, Director) — see Designation Rules below |
| **Group** | Group designation or category (e.g., "Group A"). Extract overarching headings from lists/tables. |
| **Specific Effective Date** | Date in DD-MMM-YYYY format — see Effective Date Rules below |

#### Designation Rules

**CRITICAL OVERRIDE RULE:** You MUST first scan the preamble, introductory paragraphs, and meeting headers (e.g., clauses starting with "THE UNDERSIGNED"). If the document collectively defines the capacity of the individuals in this opening text (e.g., stating they are the "managing directors of the Company and together constituting the entire board"), you MUST extract this collective definition as the Designation.

**NEGATIVE CONSTRAINT:** Do NOT extract generic titles found immediately below signature lines or in isolated table cells (such as "Director – Legal Representative", "Authorized Signatory", etc.) if a more descriptive collective title exists in the document's preamble. Only fallback to the text immediately next to/below their name if the preamble completely fails to define their capacity. NEVER use structural headings (like "Officer Signatories" or "Group A") as a Designation.

---

### ACTION NORMALIZATION RULES

Only include a person if an explicit action word is present. Normalize as follows:

| Source Keywords | Normalized Output |
|---|---|
| `'appoint'` / `'add'` / `'accede'` | `"Add"` |
| `'revoke'` / `'terminate'` / `'dismiss'` / `'withdraw'` / `'cancel'` / `'remove'` / `'removed'` / `'resign'` / `'delete'` | `"Delete"` |
| `'replace'` / `'substitute'` / `'supersede'` / `'rescind'` | `"Replace"` |
| `'amend'` / `'update'` / `'rectify'` / `'modify'` | `"Amend"` |

**GLOBAL ACTION INHERITANCE (CONDITIONAL):** Scan the document for global resolution clauses (e.g., "the above authorisations hereby supersede"). ONLY IF `"supersede"`, `"replace"`, or `"rescind"` is found globally in a whole-document context, set `"Action"` to `"Replace"` for ALL individuals. DO NOT default to `"Replace"` if these keywords are missing. IF NO action is explicitly stated AND no global override exists → `"N/A"`. NEVER infer any action from context alone.

**ACTION ORDERING RULE** — Apply this order in the output:
1. All `"Add"` actions first
2. All `"Delete"` actions second
3. All `"Replace"` actions third
4. All `"Amend"` actions fourth
5. All `"N/A"` actions last

---

### SPECIFIC EFFECTIVE DATE RULES

Use the stated effective date, or fallback to the meeting/resolution adoption date found in the main body of the document (e.g., header, preamble, or title). Apply this as the global effective date for all persons (e.g., `27-SEP-2025`).

**CRITICAL INSTRUCTION:** Do NOT extract dates from digital signature audit trails, "Final Audit Report" pages, "Created" dates, or signature histories.

If a specific effective date is mentioned for an individual person → populate only for that person.

Always convert to **DD-MMM-YYYY** format (e.g., `27-SEP-2025`).

---

### 6. PROCESSING WORKFLOW — FOLLOW THIS ORDER

1. Detect product type using keywords → if NO explicit keywords found in the document, return `{"Accounts": []}` and **STOP**.
2. Scan document headers for meeting dates to set the global **Specific Effective Date**.
3. Scan the document for whole-document supersede/replace context.
4. Scan the entire document for Account Numbers. Apply the Product Exclusion Rule.
5. Apply Mapping Logic:
   - **Scenario A:** Create a distinct JSON object for EACH explicitly mapped account number.
   - **Scenario B:** Create ONE SINGLE JSON object and include ALL account numbers in a list/array.
6. Populate `"List of Authorised Person"` for the respective account object(s). Apply the Product Exclusion Rule.
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
      "List of Authorised Person": [
        {
          "Group": "Group A",
          "Name": "John Smith",
          "Action": "Add",
          "ID Number": "P1234567",
          "Designation": "Director",
          "Specific Effective Date": "15-MAR-2024"
        },
        {
          "Group": "Group A",
          "Name": "Sarah Johnson",
          "Action": "Add",
          "ID Number": "N/A",
          "Designation": "Treasurer",
          "Specific Effective Date": "15-MAR-2024"
        },
        {
          "Group": "Group B",
          "Name": "Michael Chen",
          "Action": "Delete",
          "ID Number": "N/A",
          "Designation": "CFO",
          "Specific Effective Date": "N/A"
        },
        {
          "Group": "Group B",
          "Name": "David Wong",
          "Action": "Replace",
          "ID Number": "N/A",
          "Designation": "N/A",
          "Specific Effective Date": "N/A"
        },
        {
          "Group": "Group A",
          "Name": "Peter Lam",
          "Action": "N/A",
          "ID Number": "N/A",
          "Designation": "N/A",
          "Specific Effective Date": "N/A"
        }
      ]
    }
  ]
}
```

---

## QUALITY ASSURANCE CHECKLIST

Before submitting output, verify:

- [ ] **ANTI-HALLUCINATION CHECK:** Are all names, designations, IDs, groups, and dates verbatim from the document? If they look identical to the prompt's examples, delete them.
- [ ] **PRODUCT TYPE CHECK:** Were the electronic banking keywords explicitly found? If not, output must be `{"Accounts": []}`.
- [ ] **PRODUCT EXCLUSION CHECK:** No account numbers or signatories were extracted from tables explicitly labeled for non-electronic products like "Payroll" or "Opex".
- [ ] **MAPPED VS UNMAPPED CHECK:** Account numbers sharing the same signatory list MUST be combined into a single object's `"Account Number"` array. No duplicate objects were created.
- [ ] **FULL SIGNATORY LIST CHECK:** The complete global signatory list was extracted from the Annex/Signatory List — not limited to only those named in the Electronic Banking section.
- [ ] **DESIGNATION CHECK:** Structural headings are mapped to the `Group` field, NOT `Designation`.
- [ ] **GLOBAL ACTION CHECK:** `"Replace"` is ONLY applied globally if `"supersede"`, `"replace"`, or `"rescind"` is present in a whole-document context.
- [ ] **EFFECTIVE DATE CHECK:** Document meeting dates were scanned and applied globally to all persons.
- [ ] **NAME FORMATTING CHECK:** All salutations and titles (Mr., Mrs., Ms., Dr., Prof.) were stripped from all Names.

---

## ERROR PREVENTION RULES

**NEVER:**
- Copy text from the prompt's examples and output it as extracted data.
- Create separate, identical JSON objects for multiple account numbers unless the document explicitly maps them to different signatory lists.
- Put structural headings (like "Officer Signatories") into the `Designation` field.
- Default the `"Action"` to `"Replace"` UNLESS explicit trigger words are located in the document.
- Extract account numbers or signatory lists explicitly labeled for non-electronic products like "Payroll".
- Include a `Specimen` field in output.
- Retain salutations or titles (Mr., Mrs., Ms., Dr., etc.) in extracted Names.
- Include `Sub-Products` in this output.

**ALWAYS:**
- Return `{"Accounts": []}` if electronic banking keywords (`"electronic banking"`, `"internet banking"`, `"channels"`, `"HSBCnet"`, etc.) are not explicitly found in the document.
- Group account numbers into a list/array within ONE single object if they share the exact same global signatory list.
- Extract exact text as written for names, designations, and IDs.
- Apply the Action Ordering Rule: **Add → Delete → Replace → Amend → N/A**.
