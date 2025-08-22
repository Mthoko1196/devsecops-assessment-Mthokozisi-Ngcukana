output "bucket_name" { value = aws_s3_bucket.secure.bucket }
output "log_bucket_name" { value = aws_s3_bucket.logs.bucket }