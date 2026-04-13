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
- result - logged in as the administrator.
- observation - website is vulnerable to a classic SQL Injection.

**Conclusions**
The login page has critical security vulnerability that allows us to bypass the authentication mechanism. This indicates that other database-driven functionalities might also be vulnerable to SQL Injections. This potentially leading to full database exfiltration.

##

**Goal:** Execute DOM XSS in the "search" field.

**1.** Injection "<iframe src="javascript:alert('xss')">" into the field.
- result - JavaScript execution (alert window appears).
- observation - application implements a weak blacklist filter. While it successfully block the <script> tag, it fails to sanitize other HTML elements like <iframe>.

**2.** Impact of injection "<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>"
- results - website renders a functional music player.
- observation - the appliaction allow to use <iframe> and the same time allow for content fabrication. 

**Conclusions**
The "search" field is vulnerable to DOM-based XSS. The security mechanism is incomplete, allowing us to execute arbitrary code by using alternative HTML tags.

##

**Goal:** Access unauthorized customer order data (IDOR).

**1.** URL manipulation  "http://localhost:3000/#/track-result?id=5267-6f0cf09311268121".
- result - unauthorized access to the "Track Order" page.
- observation - appliaction does not verify if the order belongs to the logged-in user. Knowing the ID is enough to view the data.

**2.** Direct file access by change id for specific one:"http://localhost:3000/ftp/order_5267-6f0cf09311268121.pdf".
- result - access to "Order Confirmation" document.
- observation - appliaciotn give access to files without any access control checks.

**Conclusions**
The appliacation is vulnerable to IDOR (Insecure Direct Object Reference). Obtaining "Order ID" give us access to information about expected delivery, items in the order, price, quantity, bonus points earned, e-mail address and date of order. 

##
