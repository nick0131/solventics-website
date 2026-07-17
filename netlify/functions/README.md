# Contact form & notices — Netlify Functions setup

This adds two things to the homepage, both reading/writing the same
`Contact_Data` spreadsheet used by the old Streamlit app:

- **`contact.js`** — writes new contact-form submissions to the
  `Contact_Data` tab (columns: timestamp, name, email, message).
- **`notices.js`** — reads the `Notice_Data` tab and serves it as JSON so
  the homepage's news/notice sections stay live instead of hardcoded.
  Expected columns, with a header row in row 1:
  `date | title_ko | title_en | tag_ko | tag_en`

## 1. Share the sheet with your service account (skip if already done)
Open the spreadsheet → Share → add the service account's `client_email`
(e.g. `streamlit-bot@....iam.gserviceaccount.com`) as an **Editor**.

## 2. Get the three values Netlify needs
From your service account JSON key file:
- `client_email` → this becomes `GOOGLE_SERVICE_ACCOUNT_EMAIL`
- `private_key` → this becomes `GOOGLE_PRIVATE_KEY`

From the spreadsheet's URL:
```
https://docs.google.com/spreadsheets/d/THIS_PART_IS_THE_ID/edit
```
→ this becomes `GOOGLE_SHEET_ID`

## 3. Add them in Netlify
Site settings → Environment variables → Add a variable, three times:

| Key | Value |
|---|---|
| `GOOGLE_SERVICE_ACCOUNT_EMAIL` | the `client_email` value |
| `GOOGLE_PRIVATE_KEY` | the full `private_key` value, **including** `-----BEGIN PRIVATE KEY-----` and `-----END PRIVATE KEY-----` |
| `GOOGLE_SHEET_ID` | the spreadsheet ID |

Paste the private key exactly as it appears in the JSON file (with the
`\n` characters). The function already handles converting `\n` into real
line breaks, so you don't need to reformat it by hand.

## 4. Redeploy
Environment variable changes only take effect on the next deploy —
trigger one from the Netlify dashboard (Deploys → Trigger deploy) after
adding the variables.

## 5. Test
Submit the contact form on the live site once deployed. A new row should
appear in `Contact_Data` within a few seconds. If it doesn't, check
Netlify → Functions → contact → real-time logs for the error message.
