# Juice Shop Walkthrough

In this repository, I document my progress in penetration testing the OWASP Juice Shop application.

##

**Goal:** Execute a stored XSS in the "reviews" field.

**1.** Injection of the tag: "<script>alert(‘XSS’);</script>".
- result - failure.
- observation - the characters "<" and ">" are converted to HTML entities "\&lt;" and "\&gt;".

**2.** An attempt to use alternatives tag: "img", "onerror".
- result - failure.
- observation - the application consistently replaces the "<" and ">".

~~**Conclusions**
The review section includes input sanitization based on HTML Entity Encoding. This mechanism effectively neutralizes Stored XSS attacks by sanitizing HTML tags before they are rendered in the DOM.~~

**3.** Secondary context testing.
Future testing revealed that "reviews" field is processed differently during the "Request Data Export" functionality.
- result - JavaScript execution occurs when exporting user data.
- observation - stored payload embedded in a review is rendered unsafely during account data export.

**Conclusions**
The website properly sanitizies review content in the standard review display. This preventing XSS in the primary rendernig context. The "Request Data Export" functionality renders stored review content unsafely, introducing a Stored XSS vulnerability in a secondary rendering context.

##

**Goal:** Execute a stored XSS in the "username" field.

**1.** Injection "<script>alert(‘XSS’);</script>" into the field.
- result - partial failure / Self-DoS.
- observation - "User Profile" side uses a "blacklist" approach to security. It identifies the "<script>" tag and strips it out entirely instead of encoding it.

**2.** Secondary context testing injection.
- result - data integrity corruption.
- observation - the data export funcionality fails to generate. The "username" field is a stored as a broken "lert('XSS');".

**Conclusions**
"Username" fields implement input filtering via blacklisting rather than output encoding. This is an insecure as it can often be bypassed by alternative payloads.
The sanitization logic causes Self-DoS by stripping tags, the application corrupts the user's data, breaking the "User Profile" UI and the "Request Data Export" feature.

## 

**Goal:** Gain access to other users accounts using SQL Injection.

**1.** Injection "' OR 1=1--" into the "Email" and a random string in the "Password" field.
- resulst - logged in as the administrator.
- observation - website is vulnerable to a classic SQL Injection.

**Conclusions**
The login page has critical security vulnerability that allows us to bypass the authentication mechanism. This indicates that other database-driven functionalities might also be vulnerable to SQL Injections. This potentially leading to full database exfiltration.

##

**Goal:** Execute DOM XSS in the "search" field.

**1.** Injection "<iframe src="javascript:alert('xss')">" into the field.
- results - JavaScript execution (alert window appears).
- observation - application implements a weak blacklist filter. While it successfully block the <script> tag, it fails to sanitize other HTML elements like <iframe>.

**Conclusions**
The "search" field is vulnerable to DOM-based XSS. The security mechanism is incomplete, allowing us to execute arbitrary code by using alternative HTML tags.

##
