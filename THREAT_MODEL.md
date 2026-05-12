# Threat Model

## Assets
- Research Dataset (CSV/SQL)
- Processing Scripts (Python)
- Metadata (JSON/YAML)

## Threats
- Unauthorized modification of data.
- Exposure of de-identified participants (re-identification).
- Malicious code injection in ETL scripts.

## Mitigations
- Use of cryptographic checksums.
- Rigid de-identification protocols.
- Automated CI/CD validation.
