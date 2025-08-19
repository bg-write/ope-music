const fs = require('fs');
const path = require('path');

// Load reviews from JSON file
function loadReviews() {
  try {
    const dataFile = path.join(__dirname, 'reviews.json');
    const data = JSON.parse(fs.readFileSync(dataFile, 'utf8'));
    return data.reviews || [];
  } catch (error) {
    console.error('Error loading reviews:', error);
    return [];
  }
}

// Create response with CORS headers
function createResponse(body, statusCode = 200, headers = {}) {
  const responseHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Content-Type': 'application/json',
    ...headers
  };

  return {
    statusCode,
    headers: responseHeaders,
    body: JSON.stringify(body)
  };
}

// Handle CORS preflight
function handleCORS() {
  return {
    statusCode: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    },
    body: ''
  };
}

// Main handler
exports.handler = async function(event, context) {
  
  // Handle CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return handleCORS();
  }
  
  // Get the path and method
  const path = event.path;
  const method = event.httpMethod;
  
  try {
    // Simple test endpoint
    if (path === '/.netlify/functions/reviews') {
      if (method === 'GET') {
        const reviews = loadReviews();
        return createResponse({
          message: "OPE! Music Reviews API is working!",
          total_reviews: reviews.length,
          sample_review: reviews[0] || null
        });
      }
    }
    
    // Default response
    return createResponse({
      message: "OPE! Music Reviews API",
      status: "Function is running",
      path: path,
      method: method
    });
    
  } catch (error) {
    console.error('Function error:', error);
    return createResponse({
      error: 'Internal server error',
      message: error.message
    }, 500);
  }
};
