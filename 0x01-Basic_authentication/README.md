## Authentication and Authorization in Web Applications

### Table of Contents:
1. [What is Authentication?](#what-authentication-means)
2. [What is Base64?](#what-base64-is)
    - [How to Encode a String in Base64](#how-to-encode-a-string-in-base64)
3. [What is Basic Authentication?](#what-basic-authentication-means)
4. [How to Send the Authorization Header](#how-to-send-the-authorization-header)

---

### What Authentication Means
**Authentication** is the process of verifying the identity of a user or system. In web applications, this typically involves the user providing credentials, such as a username and password, which are then validated by the server. If the credentials are correct, the user is authenticated and can access protected resources. There are many authentication mechanisms, such as:

- **Username and Password**: The most common method where a user provides a username and password.
- **OAuth**: A token-based authentication protocol often used in APIs.
- **JWT (JSON Web Token)**: A compact, URL-safe token that is used for authentication and data exchange.
- **Two-factor Authentication (2FA)**: Adds an additional layer of security by requiring a second form of identification.

---

### What Base64 Is
**Base64** is an encoding scheme used to represent binary data in an ASCII string format. It takes binary data and encodes it into a string of 64 characters consisting of uppercase and lowercase letters, digits, `+`, and `/`, with `=` used for padding. Base64 encoding is commonly used in contexts where binary data needs to be transmitted or stored in text form, such as email attachments, image encoding, and web data transfer.

#### How to Encode a String in Base64
To encode a string in Base64, you need to convert the string into binary data and then apply the Base64 encoding algorithm.

##### Example in Python:
```python
import base64

# Original string
original_string = "Hello World!"

# Encoding the string to Base64
encoded_string = base64.b64encode(original_string.encode())

# Decoded back from Base64
decoded_string = base64.b64decode(encoded_string).decode()

print(f"Encoded: {encoded_string}")
print(f"Decoded: {decoded_string}")
```

##### Example in JavaScript:
```javascript
const originalString = "Hello World!";

// Encoding the string to Base64
const encodedString = btoa(originalString);

// Decoding back from Base64
const decodedString = atob(encodedString);

console.log("Encoded:", encodedString);
console.log("Decoded:", decodedString);
```

---

### What Basic Authentication Means
**Basic Authentication** is a simple authentication method where the client's credentials (username and password) are sent as a Base64-encoded string in an HTTP header. When using Basic Authentication, the client must include an `Authorization` header in each request to the server that contains the username and password.

The format of the `Authorization` header in Basic Authentication is:
```
Authorization: Basic <Base64_encoded_username:password>
```

#### Example:
If the username is `user` and the password is `pass`, the Base64 encoding of `user:pass` would be:

```plaintext
user:pass → dXNlcjpwYXNz
```

The Authorization header would then be:
```
Authorization: Basic dXNlcjpwYXNz
```

---

### How to Send the Authorization Header

To send the Authorization header in an HTTP request, you can use various tools or programming languages.

#### Using `curl`:
You can use `curl` to send an HTTP request with Basic Authentication:
```bash
curl -u user:pass https://api.example.com/resource
```
This command automatically encodes `user:pass` to Base64 and sends it in the `Authorization` header.

#### Using Python and `requests`:
```python
import requests

# Send an HTTP GET request with Basic Authentication
response = requests.get('https://api.example.com/resource', auth=('user', 'pass'))

# Print the response
print(response.text)
```

#### Using JavaScript with `fetch`:
```javascript
const username = 'user';
const password = 'pass';
const headers = new Headers();
headers.set('Authorization', 'Basic ' + btoa(username + ":" + password));

fetch('https://api.example.com/resource', { method: 'GET', headers: headers })
  .then(response => response.json())
  .then(data => console.log(data));
```

---

### Conclusion
- **Authentication** is the process of verifying a user's identity, while **Base64** is an encoding scheme used to convert binary data into a text format.
- **Basic Authentication** uses a Base64-encoded username and password, and the credentials are sent via the `Authorization` header.
- The `Authorization` header is a key part of making secure requests to APIs and protected resources, and can be easily constructed and sent using various tools and programming languages.
