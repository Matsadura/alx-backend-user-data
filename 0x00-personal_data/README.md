# Personal data

## Table of Contents

1. [Introduction](#introduction)
2. [Personally Identifiable Information (PII)](#personally-identifiable-information-pii)
3. [Log Filtering for PII](#log-filtering-for-pii)
4. [Password Encryption and Validation](#password-encryption-and-validation)
5. [Secure Database Authentication](#secure-database-authentication)

## Introduction

In today's digital landscape, protecting personal data is crucial. Educating developers on key aspects of personal data security and provide practical implementations of security measures is a must.

## Personally Identifiable Information (PII)

PII refers to any data that could potentially identify a specific individual. Examples include:

- Full name
- Social Security number
- Driver's license number
- Passport number
- Email address
- Phone number
- Home address
- Date of birth
- Credit card numbers
- Biometric data (e.g., fingerprints, retinal scans)

It's essential to handle this information with care and implement appropriate security measures.

## Log Filtering for PII

Implementing a log filter to obfuscate PII fields is crucial for preventing accidental exposure of sensitive information in log files.

Key features of an effective PII log filter:

- Regex-based pattern matching for common PII formats
- Customizable obfuscation techniques (e.g., partial masking, full redaction)
- Easy integration with popular logging frameworks

Example implementation:

```python
import re

class PIILogFilter(logging.Filter):
    def __init__(self):
        self.patterns = [
            (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', 'email'),
            (r'\b\d{3}-\d{2}-\d{4}\b', 'SSN'),
            # Add more patterns as needed
        ]

    def filter(self, record):
        message = record.getMessage()
        for pattern, pii_type in self.patterns:
            message = re.sub(pattern, f'[REDACTED {pii_type}]', message)
        record.msg = message
        return True

# Usage
logger = logging.getLogger()
logger.addFilter(PIILogFilter())
```

## Password Encryption and Validation

Secure password handling is essential for protecting user accounts. This section demonstrates how to encrypt passwords and validate them securely.

Key concepts:

1. Password hashing using a strong algorithm (e.g., bcrypt)
2. Salting to prevent rainbow table attacks
3. Secure comparison for password validation

Example implementation:

```python
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def check_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)

# Usage
password = "mySecurePassword123"
hashed_password = hash_password(password)
is_valid = check_password("mySecurePassword123", hashed_password)  # Returns True
is_valid = check_password("wrongPassword", hashed_password)  # Returns False
```

## Secure Database Authentication

Authenticating to a database securely is crucial for protecting sensitive data. Using environment variables keeps credentials out of your codebase.

Key concepts:

1. Storing database credentials in environment variables
2. Using a library like python-dotenv to load environment variables
3. Constructing a secure connection string

Example implementation:

```python
import os
from dotenv import load_dotenv
import psycopg2

# Load environment variables
load_dotenv()

def connect_to_database():
    try:
        connection = psycopg2.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME")
        )
        return connection
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
        return None

# Usage
db_connection = connect_to_database()
if db_connection:
    # Perform database operations
    db_connection.close()
```

This implementation assumes you have a `.env` file in your project root with the necessary database credentials:

```
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=your_host
DB_NAME=your_database_name
```

This can significantly enhance the security of personal data in software applications.
