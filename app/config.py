# ORACLE FIXTURE — exactly THREE hardcoded secrets are planted in this file.
# All three are published dummy/example values, safe to commit to a test repo.
# Count: 3. Any secret-detection leaf must report 3, not 2 and not 4.

AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"                              # secret 1 (AWS docs example)
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"      # secret 2 (AWS docs example)
GENERIC_API_TOKEN = "api_key_0123456789abcdef0123456789abcdef"          # secret 3

DATABASE_HOST = "localhost"
DATABASE_PORT = 5432
