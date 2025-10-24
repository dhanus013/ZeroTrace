// Server.js
const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
const twilio = require("twilio");

dotenv.config();
const app = express();

// ✅ Middlewares
app.use(cors());
app.use(express.json());

// ✅ Check for environment variables
const twilioSid = process.env.TWILIO_SID;
const twilioAuthToken = process.env.TWILIO_AUTH_TOKEN;
const twilioPhone = process.env.TWILIO_PHONE;

if (!twilioSid || !twilioAuthToken || !twilioPhone) {
  console.error("ERROR: Missing Twilio credentials in .env file.");
  console.error("Ensure TWILIO_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE are set.");
  process.exit(1); // Exit if credentials are not found
}

const client = twilio(twilioSid, twilioAuthToken);

// ✅ Test Route
app.get("/", (req, res) => {
  res.send("🌍 Emission Tracker Backend Running...");
});

// ✅ SMS Route (Used by Emission.jsx)
app.post("/send-sms", async (req, res) => {
  try {
    const { phone, message } = req.body;

    if (!phone || !message) {
      return res.status(400).json({ success: false, error: "Phone and message are required" });
    }

    console.log("📩 Incoming SMS request:", phone, message);

    const sms = await client.messages.create({
      body: message,
      from: twilioPhone, // Use the variable from .env
      to: phone,
    });

    console.log("SMS sent successfully:", sms.sid);
    res.json({ success: true, sid: sms.sid });
  } catch (error) {
    console.error("❌ SMS Error:", error.message);
    res.status(500).json({ success: false, error: error.message });
  }
});

// ✅ Start Server (Running on PORT 5000)
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
}); 