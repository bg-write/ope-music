const fs = require('fs');
const path = require('path');

// Load reviews from JSON file
function loadReviews() {
  try {
    const dataFile = path.join(__dirname, '../../python_backend/data/reviews.json');
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

// Get all reviews with pagination
function getReviews(event) {
  const reviews = loadReviews();
  
  // Get query parameters
  const queryParams = event.queryStringParameters || {};
  const page = parseInt(queryParams.page) || 1;
  const perPage = parseInt(queryParams.per_page) || 10;
  
  // Calculate pagination
  const startIdx = (page - 1) * perPage;
  const endIdx = startIdx + perPage;
  const paginatedReviews = reviews.slice(startIdx, endIdx);
  
  return createResponse({
    reviews: paginatedReviews,
    pagination: {
      page,
      per_page: perPage,
      total: reviews.length,
      pages: Math.ceil(reviews.length / perPage)
    }
  });
}

// Get specific review by ID
function getReview(event) {
  const reviews = loadReviews();
  
  // Extract review_id from path
  const pathParts = event.path.split('/');
  const reviewId = pathParts[pathParts.length - 1];
  
  if (!reviewId) {
    return createResponse({ error: 'Review ID required' }, 400);
  }
  
  // Find review by ID
  const review = reviews.find(r => r.review_id === reviewId);
  
  if (review) {
    return createResponse(review);
  } else {
    return createResponse({ error: 'Review not found' }, 404);
  }
}

// Search reviews
function searchReviews(event) {
  const query = (event.queryStringParameters?.q || '').toLowerCase();
  
  if (!query) {
    return createResponse({ error: 'Search query required' }, 400);
  }
  
  const reviews = loadReviews();
  const results = [];
  
  // Split search into individual terms
  const searchTerms = query.split(' ');
  
  for (const review of reviews) {
    // Create searchable text
    const searchableText = `${review.song_artist} ${review.song_title} ${review.review_text}`.toLowerCase();
    
    // Check if ALL terms appear somewhere
    if (searchTerms.every(term => searchableText.includes(term))) {
      results.push(review);
    }
  }
  
  return createResponse({
    query,
    results,
    total_results: results.length
  });
}

// Get analytics
function getAnalytics() {
  const reviews = loadReviews();
  
  if (reviews.length === 0) {
    return createResponse({ error: 'No reviews found' }, 404);
  }
  
  // Calculate analytics
  const totalReviews = reviews.length;
  
  // Rating distribution
  const ratingCounts = {};
  for (const review of reviews) {
    const score = review.review_score;
    ratingCounts[score] = (ratingCounts[score] || 0) + 1;
  }
  
  // Artist counts
  const artistCounts = {};
  for (const review of reviews) {
    const artist = review.song_artist;
    artistCounts[artist] = (artistCounts[artist] || 0) + 1;
  }
  
  // Most reviewed artist
  const mostReviewedArtist = Object.entries(artistCounts)
    .sort(([,a], [,b]) => b - a)[0];
  
  return createResponse({
    total_reviews: totalReviews,
    rating_distribution: ratingCounts,
    artist_counts: artistCounts,
    most_reviewed_artist: mostReviewedArtist,
    average_rating: 'N/A' // We'll implement this later
  });
}

// Export to CSV
function exportCSV() {
  const reviews = loadReviews();
  
  if (reviews.length === 0) {
    return createResponse({ error: 'No reviews found' }, 404);
  }
  
  // Create CSV content
  const csvLines = [];
  
  // Header
  const headers = ['review_id', 'song_title', 'song_artist', 'review_date', 'review_score', 'review_text', 'song_url'];
  csvLines.push(headers.join(','));
  
  // Data rows
  for (const review of reviews) {
    const row = [
      review.review_id,
      `"${review.song_title.replace(/"/g, '""')}"`,
      `"${review.song_artist.replace(/"/g, '""')}"`,
      `"${review.review_date.replace(/"/g, '""')}"`,
      review.review_score,
      `"${review.review_text.replace(/"/g, '""').replace(/,/g, ';')}"`,
      review.song_url
    ];
    csvLines.push(row.join(','));
  }
  
  const csvContent = csvLines.join('\n');
  
  return {
    statusCode: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'text/csv',
      'Content-Disposition': 'attachment; filename=ope_reviews.csv'
    },
    body: csvContent
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
    // Route to appropriate handler based on path
    if (path === '/.netlify/functions/api/reviews') {
      if (method === 'GET') {
        return getReviews(event);
      }
    }
    
    else if (path.startsWith('/.netlify/functions/api/reviews/') && path.split('/').length > 4) {
      if (method === 'GET') {
        return getReview(event);
      }
    }
    
    else if (path === '/.netlify/functions/api/search') {
      if (method === 'GET') {
        return searchReviews(event);
      }
    }
    
    else if (path === '/.netlify/functions/api/analytics') {
      if (method === 'GET') {
        return getAnalytics();
      }
    }
    
    else if (path === '/.netlify/functions/api/export/csv') {
      if (method === 'GET') {
        return exportCSV();
      }
    }
    
    // Default response for unknown endpoints
    return createResponse({
      error: 'Endpoint not found',
      available_endpoints: [
        '/api/reviews',
        '/api/reviews/<review_id>',
        '/api/search?q=<query>',
        '/api/analytics',
        '/api/export/csv'
      ]
    }, 404);
    
  } catch (error) {
    console.error('Function error:', error);
    return createResponse({
      error: 'Internal server error',
      message: error.message
    }, 500);
  }
};
