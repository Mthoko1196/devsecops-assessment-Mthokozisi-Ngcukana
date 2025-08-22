
# Incident Response Playbook  
**Scenario:** CI/CD Pipeline Compromise (GitHub Actions → AWS)

---

## 0. Scope and Assumptions
- Entry points: stolen GitHub token, tampered workflow, self-hosted runner compromise, malicious dependency, abused OIDC role, leaked AWS keys.  
- Blast radius: repo code, build secrets, artifacts, container images, deployed workloads, downstream data.  
- Goals: stop misuse, preserve evidence, restore clean pipelines, reduce re-occurrence.

---

## 1. Step-by-Step Response Procedures

### T0–30 min: Triage and Stabilize
- Declare incident and assign roles (IC, Ops, Comms).  
- Disable GitHub Actions on affected repos or restrict environments.  
- In AWS: deny OIDC role assumption or revoke CI keys.  
- Preserve logs: GitHub audit logs, workflow runs, AWS CloudTrail, GuardDuty, ECR/ECS logs.

### T30–120 min: Containment
- Rotate GitHub and AWS secrets.  
- Quarantine images/artifacts in ECR or S3.  
- Enforce branch protections and environment approvals.  
- Lock down Actions usage to vetted workflows and runners.

### 2–24 hours: Investigation and Eradication
- Trace entry and activity in GitHub (workflow changes, OIDC provider updates, runner registrations) and AWS (AssumeRole events, unexpected pushes).  
- Revert unauthorized workflow changes.  
- Remove rogue runners and IAM policies.  
- Rebuild images from clean sources and regenerate SBOMs.  
- Reimage self-hosted runners with golden images.

### Recovery and Validation
- Recreate OIDC role with strict conditions (repo, branch, environment).  
- Re-enable Actions with allow-listing.  
- Redeploy from clean commits to staging, then prod.  
- Verify integrity via signatures, SBOMs, IAM drift checks.

### Post-Incident
- Lessons learned documented within 5 days.  
- Remediation tasks assigned with owners and deadlines.  
- Monitoring rules updated and tested.

---

## 2. Detection and Containment Strategies

### GitHub Indicators
- Workflow edits on default branches.  
- Actions runs from unexpected branches/forks.  
- New self-hosted runner registrations.  
- Secrets accessed by unapproved jobs.

### AWS Indicators
- `AssumeRoleWithWebIdentity` from unknown repos/branches.  
- Unusual `ecr:PutImage`, `lambda:UpdateFunctionCode`, or EB updates.  
- Config changes by CI roles outside change windows.

### Quick Containment
- Disable Actions.  
- Deny OIDC role assumption.  
- Rotate all secrets.  
- Quarantine suspect artifacts.

---

## 3. Prevention and Monitoring Improvements

### Identity & Access
- Use OIDC with strict conditions (`repo`, `ref`, `environment`).  
- Short session durations and least privilege per repo.  

### Pipeline Hygiene
- Branch protections and signed commits.  
- Allow-list actions by SHA.  
- SBOM generation and artifact signing (e.g., Cosign).  

### Secrets
- Centralize in AWS Secrets Manager or Parameter Store.  
- Rotate regularly and on demand.  

### Build Security
- Mandatory SAST/SCA.  
- Container scanning at build and on push.  
- Admission controls for signed images only.  

### Monitoring
- GuardDuty + CloudTrail alerts on CI roles.  
- GitHub alerts on workflow edits and new runners.  
- Dashboards for CI role usage and image provenance.  

### Self-hosted Runners
- Ephemeral runners only.  
- Restrict egress to GitHub and registries.  

---

## 4. Communication Plan Outline

### Roles
- **Incident Commander:** decision-making, timeline.  
- **Technical Leads:** GitHub & AWS.  
- **Comms Lead:** internal/external updates.  
- **Legal/Privacy:** regulatory obligations.  
- **Business Owner:** customer impact.  

### Cadence
- Engineering: hourly until containment, then twice daily.  
- Execs: initial summary within 2 hours, then at milestones.  
- Customers/partners: only if impact confirmed, aligned with Legal.  
- Regulators: if data exposure triggers thresholds.  

### Update Template
- What happened  
- Impact/blast radius  
- Containment actions  
- Next steps  
- Ask from stakeholders  

---

## 5. Checklists

**Containment**
- [ ] Disable Actions on affected repos  
- [ ] Deny OIDC role assumption / revoke keys  
- [ ] Rotate secrets  
- [ ] Quarantine artifacts  
- [ ] Preserve logs  

**Eradication**
- [ ] Revert workflow changes  
- [ ] Remove rogue runners/tokens  
- [ ] Recreate IAM roles with strict conditions  
- [ ] Rebuild images, rescan, resign  

**Recovery**
- [ ] Re-enable pipelines with allow-lists  
- [ ] Redeploy to staging → prod  
- [ ] Verify integrity and runtime policies  

**Post-Incident**
- [ ] Root cause documented  
- [ ] Actions assigned with deadlines  
- [ ] Monitoring rules updated  

---
