package terraform.security

deny[msg] {
  input.resource_type == "aws_s3_bucket_public_access_block"
  not input.config.block_public_acls
  msg := "S3 buckets must block public ACLs"
}

deny[msg] {
  input.resource_type == "aws_s3_bucket_public_access_block"
  not input.config.block_public_policy
  msg := "S3 buckets must block public policy"
}