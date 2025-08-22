.PHONY: scan-images lint-dockerfile scan-compose tf-init tf-plan tf-scan tf-policy

scan-images:
	trivy image --exit-code 0 --severity MEDIUM,LOW devsecops/react-app:local || true
	trivy image --exit-code 1 --severity CRITICAL,HIGH devsecops/react-app:local || true
