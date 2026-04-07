# Juice Shop Walkthrough

In this repository, I document my progress in penetration testing the OWASP Juice Shop application.

## 2026-04-07

**Goal:** Execute a stored XSS in the “reviews” field.

**1.** Injection of the tag: "<script>alert(‘XSS by cialoo’);</script>"
- result - failure
- observation - the characters "<" and ">" are converted to HTML entities "&lt;" and "&gt;".

**2.** An attempt to use alternatives tag: "<img>", "onerror"
- result - failure
- observation - the application consistently replaces the "<" and ">".

**Conclusions**
The review section includes input sanitization based on HTML Entity Encoding. This mechanism effectively neutralizes Stored XSS attacks by sanitizing HTML tags before they are rendered in the DOM.
