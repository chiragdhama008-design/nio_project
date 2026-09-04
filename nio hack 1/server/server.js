require('dotenv').config();
const express = require('express');
const cors = require('cors');
const Groq = require('groq-sdk');

const app = express();
app.use(cors());
app.use(express.json());

const PORT = process.env.PORT || 3000;

// Initialize Groq API
const groq = new Groq({ apiKey: process.env.LLM_API_KEY });

app.post('/api/analyze', async (req, res) => {
  try {
    const { description, location } = req.body;

    if (!process.env.LLM_API_KEY || process.env.LLM_API_KEY === 'your_gemini_api_key_here') {
      console.warn("LLM_API_KEY is not set correctly. Returning fallback mock data.");
      return res.json({
        id: `REP-${Math.floor(Math.random() * 10000)}`,
        timestamp: new Date().toISOString(),
        aiAnalysis: {
          hazardType: 'Unknown (Key Missing)',
          confidence: '0.0',
          urgencyKeywords: ['API_KEY_MISSING'],
          locationContext: 'Standard Location',
          isDuplicate: false,
          clusterId: null,
          riskScore: 50,
        }
      });
    }

    const prompt = `
      You are an AI analyzing urban hazard reports for the CivicShield triage system.
      
      Report Details:
      Description: "${description}"
      Location: "${location}"

      Analyze the report and provide the following in valid JSON format:
      - hazardType (string): e.g., Pothole, Broken Streetlight, Waterlogging.
      - confidence (string): 0-100 percentage.
      - urgencyKeywords (array of strings): extracted urgent words from the description (e.g., accident, dangerous).
      - locationContext (string): assess risk based on location, e.g., "Near High-Traffic Zone" or "Standard Location".
      - isDuplicate (boolean): mostly false for this demo, unless the text explicitly says "duplicate".
      - clusterId (string or null): null if not a duplicate.
      - riskScore (number): 0 to 100, where 100 is most critical. Base it on hazard type, urgency keywords, and location.

      Respond ONLY with the raw JSON object, no markdown formatting.
    `;

    const chatCompletion = await groq.chat.completions.create({
      messages: [
        {
          role: "user",
          content: prompt,
        },
      ],
      model: "llama3-8b-8192", // Using a fast, standard model on Groq
      response_format: { type: "json_object" },
    });

    const responseContent = chatCompletion.choices[0]?.message?.content;
    const analysis = JSON.parse(responseContent);

    // Return combined result
    res.json({
      id: `REP-${Math.floor(Math.random() * 10000)}`,
      timestamp: new Date().toISOString(),
      aiAnalysis: analysis
    });

  } catch (error) {
    console.error('Error analyzing report:', error);
    res.status(500).json({ error: 'Failed to analyze report using LLM' });
  }
});

app.listen(PORT, () => {
  console.log(`CivicShield backend running on http://localhost:${PORT}`);
});
