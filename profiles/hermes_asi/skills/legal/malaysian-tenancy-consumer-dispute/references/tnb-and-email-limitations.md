# TNB Bill Check & Email from VPS — Limitations

## TNB Bill by Account Number (Without Login)

**Reality:** Cannot programmatically access. TNB QuickPay portal at https://myaccount.mytnb.com.my/Payment/QuickPay/ requires reCAPTCHA solve. Direct MX delivery (sending email from VPS to Yahoo/Gmail) is unreliable:

- **Gmail rejects unauthenticated senders** (DMARC strict: "5.7.26 Unauthenticated email from yahoo.com is not accepted")
- **Direct MX delivery to Yahoo** may succeed but messages get spam-filtered
- **No SMTP credentials** on VPS = no reliable outbound mail

## What Works

| Method | Detail |
|---|---|
| myTNB App | User must download, login, add account number |
| TNB CareLine | Call 1-300-88-5454, provide account number + address |
| User's own email | User copy-pastes draft and sends manually |

## TNB for Rental Disputes

- Tip: Don't transfer TNB into tenant's name until landlord settles all obligations
- In tenancy context, TNB account is typically in landlord's name
- If landlord owes utility deposit, tenant should NOT register TNB under own name
