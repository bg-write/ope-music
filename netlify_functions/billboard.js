const fs = require('fs');
const path = require('path');

exports.handler = async (event, context) => {
  // CORS headers for production
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Content-Type': 'application/json'
  };

  // Handle preflight OPTIONS request
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  // Only allow GET requests
  if (event.httpMethod !== 'GET') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    // In production, read from the deployed data file
    const dataPath = path.join(__dirname, '../data_output/billboard_chart_data.json');
    
    if (fs.existsSync(dataPath)) {
      const realData = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
      
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          data: realData,
          message: 'Billboard chart data loaded from production data file',
          source: 'netlify_function',
          deployed_at: new Date().toISOString()
        })
      };
    } else {
      // Fallback to mock data if file doesn't exist
      const mockData = {
        chart_date: new Date().toISOString().split('T')[0],
        total_entries: 100,
        chart_entries: [
          {
            rank: 1,
            title: "Golden",
            artist: "HUNTR/X: EJAE, Audrey Nuna & REI AMI",
            chart_date: new Date().toISOString().split('T')[0],
            scraped_at: new Date().toISOString()
          },
          {
            rank: 2,
            title: "Vampire",
            artist: "Olivia Rodrigo",
            chart_date: new Date().toISOString().split('T')[0],
            scraped_at: new Date().toISOString()
          }
        ],
        top_artists: [
          {
            artist: "HUNTR/X: EJAE, Audrey Nuna & REI AMI",
            total_score: 100,
            song_count: 1,
            positions: [1]
          },
          {
            artist: "Olivia Rodrigo",
            total_score: 99,
            song_count: 1,
            positions: [2]
          }
        ]
      };

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          data: mockData,
          message: 'Using mock data - production data file not found',
          source: 'mock_data',
          deployed_at: new Date().toISOString()
        })
      };
    }
  } catch (error) {
    console.error('Error in Billboard Netlify function:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: 'Internal server error',
        message: 'Failed to load Billboard data',
        source: 'error'
      })
    };
  }
};
