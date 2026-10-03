# Local Knowledge Base

Place private/company knowledge sources here when running the agent locally.

Recommended structure:

knowledge/
  raw/
    Wendor_KB_Fixed/
    Adnan_Role_KRA_Operating_Manual_Updated.docx
  index/

These files are intentionally excluded from Git.

The agent should retrieve from the knowledge base using:
1. source-of-truth priority,
2. topic routing,
3. evidence/context retrieval,
4. action/owner/closure rules.

Do not commit employer/customer-confidential documents to this public repository.
