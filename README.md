# ProfileSynchronizationService

Phase 1 starter, not production-ready. Python 3.12 recommended. No live database writes or AI network calls are wired. Public liveness only; import inspection fails closed until Newsletter authentication is integrated.

## Windows / VS Code
```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
python -m pytest -q
python -m uvicorn profile_sync.main:app --host 127.0.0.1 --port 8000 --reload
```
Visit http://127.0.0.1:8000/health/live. Select .venv interpreter in VS Code.

## Design
Domain is independent of frameworks. Application ports define external contracts. Infrastructure contains parsers, SQL repositories and normalization. Presentation exposes API. Configuration is uppercase snake case. Existing Profiles is owned by C# migrations. ORM models for new tables are proposals; no migration is applied or provided until existing HeaderMappingRecord and schema ownership are verified. SQL inspection is read-only; candidate index is commented.

## Required before enabling production
- Obtain Newsletter authentication contract, issuer/audience, token transport and permission claims. Add verified authentication and per-job authorization; no bypass.
- Obtain C# contact normalization/hash/encryption implementation and synthetic interoperability vectors. Raw, encrypted and hashed contacts must be written atomically; no fake emails. Resolve existing unique empty email constraints before phone-only creation.
- Inspect existing HeaderMappings and database schema; coordinate migrations. Require TLS certificate verification in production PostgreSQL connection settings and least privilege.
- Implement metadata sanitization and explicit approval before AI; agents are ports only. Never send participant values. Implement tag approval and profile updates preserving suppression and consent.
- Implement durable encrypted staging, Azure private Blob/queue integration, job orchestration, idempotent transactions, audit, retry, and final approval. Do not use this starter for real participant uploads yet. File limits must also be enforced at ingress before multipart parsing.
- Parser currently supports one worksheet, UTF-8 CSV, first-row headers, no formulas; numeric ZIP/phone cells may lose leading zeros in Excel. Require text formatting or review. Contact aliases are detected, but value validation/column selection and row-level matching are not wired to API.
- Pin dependencies with pip-compile and audit before deployment. Container/CI examples are not tested in Azure. Production readiness endpoint and secure deployment configuration remain pending.
