# Juice Shop Walkthrough

In this repository, I document my progress in penetration testing the OWASP Juice Shop application.

##

**Goal:** Execute a stored XSS in the "reviews" field.

**1.** Injection of the tag: "<script>alert(‘XSS by cialoo’);</script>".
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
The website properly sanitizies review content in the standard review display. This preventing XSS in the primary rendernig context.

The "Request Data Export" functionality renders stored review content unsafely, introducing a Stored XSS vulnerability in a secondary rendering context.

## 
