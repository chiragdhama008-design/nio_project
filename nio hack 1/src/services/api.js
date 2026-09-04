// Calls the Express backend which in turn calls the LLM
export const processReport = async (reportData) => {
  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        description: reportData.description,
        location: reportData.location
      })
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    const data = await response.json();
    return {
      ...reportData,
      id: data.id,
      timestamp: data.timestamp,
      aiAnalysis: data.aiAnalysis
    };
  } catch (error) {
    console.error("Failed to process report:", error);
    alert("Failed to connect to the backend AI service. Check console for details.");
    throw error;
  }
};
