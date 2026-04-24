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

**2.** Injection "' OR 1=1 LIMIT 2,1 --" into the "Email" and a random string in the "Password" field.
- result - logged in as another user (bender).
- observation - query returns multiple users and LIMIT allows selecting a specific one.

~~**Conclusions**
The login page has critical security vulnerability that allows us to bypass the authentication mechanism. This indicates that other database-driven functionalities might also be vulnerable to SQL Injections. This could potentially lead to full database exfiltration.~~ 

**3.** Injection "jim@juice-sh.op'--" into the "Email" and a random string in the "Password" field.
- result - logged in as another user (jim) by type his adrress email which we allow to see in the reviews.
- observation - the SQL query is likely structured as: "SELECT * FROM users WHERE email='email_input' AND password='password_input'".

**Conclusions**
The login page has critical security vulnerability that allows access to arbitrary user accounts. We can bypass the authentication mechanism by manipulating the "LIMIT" clause or we can choose users by using a valid emial address which we allow to see in the reviews. This results in full account takeover.

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
The application is vulnerable to IDOR (Insecure Direct Object Reference). Obtaining "Order ID" give us access to information about expected delivery, items in the order, price, quantity, bonus points earned, e-mail address and date of order. 

##

**Goal:** Verification of password hashing mechanism.

**1.** Check password length using SQL Injection: "1@1.pl' AND LENGTH(password) = 32 --" in the username field.
- result - successful, password length is 32 characters.
- observation - MD5 hashes have the same length of 32 characters.

**2.** Convert known password "11111" to its MD5 hash "b0baee9d279d34fa1dfd71aadb908c3f" and attempt authentication using SQL Injection: "1@1.pl' AND password = 'b0baee9d279d34fa1dfd71aadb908c3f'--" in the username field.
- result - successful authentication.
- observation - the application compares the provided value directly with the stored MD5 hash.

**Conclusions**
The application uses unsalted MD5 hashing for password storage. This allows an attacker to verify password hashes via SQL Injection and potentially recover plaintext passwords of the users. This significantly increases the impact of the SQL Injection vulnerability.

##

**Goal.** Perform password extraction via Blind SQL Injection.

**1.** Test password values for the administrator account using: "admin@juice-sh.op' AND password LIKE 'n%' --", where "n" represents each possible MD5 character (0-9, a-f).
- result - after multiple attempts, successful login using the full 32-character pattern: "admin@juice-sh.op' AND password LIKE '0192023a7bbd73250516f069df18b500%' --".
- observation - the login page can be use as a boolean oracle (True/False) to verify correct password characters.

**2.** Decode the extracted MD5 hash "0192023a7bbd73250516f069df18b500" and attempt authentication.
- result - decoded password is "admin123", successful login.
- observation - user passwords can be recovered from their hashes.

**Conclusions**
The SQL Injection vulnerability in the login page allows full password extraction using blind techniques. Combined with weak password hashing (unsalted MD5), an attacker can recover plaintext passwords of users. This can lead to credential reuse attacks on other services (e.g., email accounts), significantly increasing the overall impact of the vulnerability.

##
















