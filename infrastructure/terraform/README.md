# Terraform — Secure S3 baseline

This module creates two buckets: a **logs** bucket and a **secure** bucket with:
- Versioning
- SSE (AES256)
- Public access blocked
- Access logging to the logs bucket

## Commands
```
terraform init
terraform plan -out=tfplan
terraform show -json tfplan > plan.json
checkov -d .
tfsec .
conftest test plan.json
```

## Secrets
Do not commit plaintext secrets. If required, reference AWS Secrets Manager via variables and resolve at application runtime. Avoid printing secrets in outputs.
```

---