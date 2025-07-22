// src/api.js
const API_BASE_URL = 'http://localhost:5000'; // Change to your backend URL

export async function extractInsights(text) {
  const response = await fetch(`${API_BASE_URL}/extract-insights`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) {
    throw new Error('Failed to extract insights');
  }
  return response.json();
}