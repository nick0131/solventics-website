// netlify/functions/notices.js
//
// Reads the "Notice_Data" tab of the same Contact_Data spreadsheet and
// returns it as JSON so the homepage can show live notices instead of
// hardcoded ones. Expected columns (row 1 = header, skipped):
//   A: date       B: title_ko     C: title_en     D: tag_ko     E: tag_en
//
// Uses the same env vars as contact.js:
//   GOOGLE_SERVICE_ACCOUNT_EMAIL, GOOGLE_PRIVATE_KEY, GOOGLE_SHEET_ID

const { google } = require("googleapis");

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
};

exports.handler = async () => {
  try {
    const auth = new google.auth.JWT(
      process.env.GOOGLE_SERVICE_ACCOUNT_EMAIL,
      null,
      (process.env.GOOGLE_PRIVATE_KEY || "").replace(/\\n/g, "\n"),
      ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    );

    const sheets = google.sheets({ version: "v4", auth });

    const res = await sheets.spreadsheets.values.get({
      spreadsheetId: process.env.GOOGLE_SHEET_ID,
      range: "Notice_Data!A2:E", // row 1 is the header, so start at row 2
    });

    const rows = res.data.values || [];

    const notices = rows
      .filter((r) => r[0]) // drop blank rows
      .map((r) => ({
        date: r[0] || "",
        title_ko: r[1] || "",
        title_en: r[2] || "",
        tag_ko: r[3] || "",
        tag_en: r[4] || "",
      }))
      // newest first, assumes YYYY-MM-DD style dates so string sort works
      .sort((a, b) => (a.date < b.date ? 1 : -1));

    return {
      statusCode: 200,
      headers: {
        ...CORS_HEADERS,
        "Content-Type": "application/json",
        "Cache-Control": "public, max-age=300", // 5 min, matches the old Streamlit cache TTL
      },
      body: JSON.stringify({ notices }),
    };
  } catch (err) {
    console.error("notices.js error:", err.message);
    return {
      statusCode: 500,
      headers: CORS_HEADERS,
      body: JSON.stringify({ error: "Failed to load notices" }),
    };
  }
};
