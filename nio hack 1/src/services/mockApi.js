export const MOCK_HAZARDS = ['Pothole', 'Broken Streetlight', 'Waterlogging', 'Garbage Dumping', 'Damaged Infrastructure'];

// Simulates the AI pipeline
export const processReport = async (reportData) => {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 1500));

  // 1. Image Analysis Mock
  const hazardType = MOCK_HAZARDS[Math.floor(Math.random() * MOCK_HAZARDS.length)];
  const confidence = (Math.random() * 40 + 60).toFixed(1); // 60-100%

  // 2. Text Analysis Mock (NLP)
  const description = (reportData.description || '').toLowerCase();
  let textSeverity = 0;
  const urgencyKeywords = [];
  if (description.includes('accident') || description.includes('dangerous') || description.includes('huge') || description.includes('urgent')) {
    textSeverity += 30;
    if (description.includes('accident')) urgencyKeywords.push('accident');
    if (description.includes('dangerous')) urgencyKeywords.push('dangerous');
    if (description.includes('urgent')) urgencyKeywords.push('urgent');
  }

  // 3. Location Context Mock
  // Arbitrarily assign higher risk to certain random cases to simulate proximity to schools/hospitals
  const locationMultiplier = Math.random() > 0.7 ? 1.5 : 1.0; 
  const locationContext = locationMultiplier > 1.0 ? 'Near High-Traffic/School Zone' : 'Standard Location';

  // 4. Priority Scoring
  // Base risk 10-50 + text severity + location multiplier
  let baseScore = Math.floor(Math.random() * 40) + 10;
  let riskScore = Math.min(100, Math.floor((baseScore + textSeverity) * locationMultiplier));

  // 5. Deduplication Mock
  const isDuplicate = Math.random() > 0.8; // 20% chance it clusters with an existing issue
  const clusterId = isDuplicate ? `CLUSTER-${Math.floor(Math.random() * 1000)}` : null;

  return {
    ...reportData,
    id: `REP-${Math.floor(Math.random() * 10000)}`,
    timestamp: new Date().toISOString(),
    aiAnalysis: {
      hazardType,
      confidence,
      urgencyKeywords,
      locationContext,
      isDuplicate,
      clusterId,
      riskScore,
    }
  };
};
