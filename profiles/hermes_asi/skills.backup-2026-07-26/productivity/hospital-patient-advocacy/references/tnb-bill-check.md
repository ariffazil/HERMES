# TNB Bill Check — Browser Automation Gotcha

Checking a Malaysian TNB electricity bill programmatically.

## Official Portal

**Express Payment (no login required):**
`https://myaccount.mytnb.com.my/Payment/QuickPay/`

## Browser Automation Pitfalls

### 1. Spinbutton inputs (not text inputs)
The account number field is 12 individual `<input type="number" role="spinbutton">` elements — one per digit. You cannot paste a 12-digit string. Each digit must be typed individually into its own spinbutton.

In Hermes browser tools, this means 12 separate `browser_type` calls (one per ref).

### 2. reCAPTCHA blocks submission
Even after entering all 12 digits and force-enabling the disabled Search button via JavaScript (`document.querySelector('button').disabled = false`), the page injects a reCAPTCHA iframe before processing. Programmatic access is blocked.

### 3. No API fallback
TNB does not expose a public API for bill checking. The only paths are:
- myTNB mobile app (Android/iOS)
- Web portal with CAPTCHA
- Phone: 1-300-88-5454 (CareLine)

## Verdict

**Don't attempt browser automation for TNB bills.** Tell the user to use the myTNB app or call CareLine. The spinbutton + CAPTCHA combo means it'll always fail from an agent context.

## Account Number Format

12 digits. Example: `210356986905`. Printed at the top of every TNB bill under the logo.

## Alternative: CareLine Phone

Call **1-300-88-5454** with the account number and registered address. Agent can read the current bill amount and due date over the phone. No CAPTCHA.

## Session Evidence

2026-07-21: Attempted to check account `210356986905` (Neu Suites unit) via browser. Spinbuttons entered successfully but reCAPTCHA blocked search. Failed after 12+ tool calls. User directed to myTNB app instead.
