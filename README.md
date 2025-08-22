# DevSecOps Assessment — Blocks 1B, 3, 4 (Terraform), 5

This repo contains..

- **Block 1 (Option B)**: Custom secret detection engine (language-agnostic)
- **Block 3**: Container security for a React app (Node build -> NGINX runtime, non-root)
- **Block 4**: IaC security with Terraform + policy validation (OPA/Rego)
- **Block 5**: Incident Response plan for a CI/CD pipeline compromise
## Approach Summary
I focused on four blocks that demonstrate practical DevSecOps skills:

- **Block 1 (Option B — Secret Detection Engine):**  
  Implemented a custom CLI to detect secrets using regex + entropy. Supports a baseline allowlist and JSON output for CI/CD. Exits non-zero on Medium+ findings, ensuring secret leakage breaks the build.

- **Block 3 (Container Security):**  
  Hardened Dockerfile for the provided React app. Since the app bundle was already supplied, I simplified the build to a single NGINX stage running as non-root on port 8080. Added security headers, read-only root filesystem, capability drops, and healthchecks. Integrated Trivy and Hadolint into CI.

- **Block 4 (Terraform + Policy as Code):**  
  Provisioned a minimal but secure S3 baseline with logging, versioning, and server-side encryption. Applied static analysis (tfsec, Checkov) and OPA policy validation with Conftest to enforce “no public buckets” as code.

- **Block 5 (Incident Response — CI/CD Compromise):**  
  Authored a step-by-step IR plan (detection, containment, eradication, recovery, and comms). Hardened the GitHub Actions workflow by pinning actions to SHAs, applying least-privilege permissions, and splitting policy validation into a separate job.

**Tool choices:**  
- *Custom scanner* for secrets (Python)  
- *Trivy, Hadolint, Grype* for containers  
- *tfsec, Checkov, OPA (Conftest)* for Terraform  
- *GitHub Actions* for CI/CD with pinned SHAs  
- *NGINX* as minimal runtime for static React app  

---

## Time Breakdown
- Block 1 (Secret detection): **40 minutes**  
- Block 3 (Container security): **45 minutes**  
- Block 4 (Terraform + policy): **35 minutes**  
- Block 5 (IR plan + CI hardening): **25 minutes**  
- Documentation and cleanup: **15 minutes**  

**Total ≈ 2h40** (within the 3-hour guideline).

---

## Assumptions Made
- The React app was already provided as a pre-built bundle. No Node.js build stage was required; Dockerfile just serves static assets via NGINX.  
- AWS credentials are not needed for `terraform plan`; if apply was required, credentials would be injected as repo secrets.  
- Security gates:  
  - Fail pipeline on CRITICAL/HIGH container vulns  
  - Fail pipeline on Medium+ secret findings  
  - IaC scans (`tfsec`, `checkov`) produce reports but OPA policy is the hard enforcement step.  
- Latest stable releases of security tools are acceptable in CI runners for the assessment context.
### Personal Note
DevSecOps as a discipline is new to me, but I have solid foundations in GitHub workflows, AWS services, and CI/CD. I approached this assessment by leveraging those fundamentals and layering in security tooling and practices where they fit naturally:
- Security gates in GitHub Actions (Trivy, Hadolint, secret scan, IaC scans)
- AWS IaC with encryption, logging, and policy validation
- Clear documentation of assumptions, risks, and mitigations

This demonstrates my ability to take my current strengths and extend them into security-focused DevOps practices.

---

## Challenges & Solutions
- **False positives in secret scanning:**  
  Some benign tokens looked like keys. Solved with an entropy threshold and baseline allowlist to filter expected strings.  

- **React build uncertainty (dist vs build):**  
  Confirmed the provided app was already built. Simplified Dockerfile to serve static bundle directly from NGINX. Documented how to switch copy path if needed.  

- **Tool availability on GitHub runners:**  
  Default runners don’t include Trivy/tfsec/Conftest/Hadolint. Added explicit install steps in the workflow before running scans.  

- **Balance between depth and breadth:**  
  Instead of trying to cover every Terraform resource, I focused on one (S3) that demonstrates encryption, logging, and access control. This allowed me to integrate both scanning and policy validation in the timebox.

---

## AI/LLM Usage
- **Tool used:** ChatGPT (to speed up drafting configs, scripts, and documentation).  
- **Prompts used (examples):**  
  - “Write a Python CLI that scans a repo for secrets using regex and entropy, with baseline allowlist and JSON output.”  
  - “Generate a hardened Dockerfile for a React app served with NGINX as non-root.”  
  - “Provide a Terraform config for a secure S3 bucket with versioning, SSE, and logging, plus an OPA policy to block public access.”  
  - “Harden a GitHub Actions workflow: pin SHAs, least-privilege permissions, install Trivy/tfsec/Checkov/Conftest/Hadolint.”  

- **Outputs received:** Initial drafts of Dockerfile, secret scanner skeleton, Terraform S3 config, OPA policy, and workflow YAML.  
- **Modifications made:** Tightened regexes and entropy handling in scanner, simplified Dockerfile to skip Node build, split IR workflow into two jobs, and added explicit tool installation to CI. Also edited docs to reflect the provided app context and assessment requirements.

## Secrets Management Note

As part of Block 1 (Secret Detection Engine) I deliberately tested with a dummy AWS key to validate that both GitHub’s built-in secret scanning and my custom scanner would flag it.  
The secret was **not valid** and posed no real risk, but it demonstrated that the detection mechanisms work as intended.

Key practices I would follow in production:
- Never commit real secrets to source control.
- Use GitHub Actions secrets or AWS OIDC roles for authentication.
- Revoke and rotate any credential that is accidentally committed.
- Clean the commit history if an actual secret leak occurred.

<img width="1885" height="817" alt="image" src="https://github.com/user-attachments/assets/e19295d5-bae9-40e4-8b15-6e4890570971" />

This test highlights the importance of automated secret detection in CI/CD pipelines and shows how I would handle real secrets safely.
