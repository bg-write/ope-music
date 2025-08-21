// Reviews data embedded directly in the function
const reviewsData = {
  "reviews": [
    {
      "song_artist": "Florence + The Machine",
      "song_title": "Everybody Scream",
      "song_release_date": "2025-08-20",
      "song_upload_date": "2025-08-20",
      "song_duration_sec": 339,
      "song_album": "Everybody Scream",
      "song_label": "Universal Music Operations Limited",
      "song_genre": "Pop",
      "song_mood": "Energetic, Dramatic",
      "song_instrumentation": "Drums, Guitar, Vocals, Strings",
      "song_language": "English",
      "song_audio_url": "https://youtu.be/03iBgkXb1EE?si=AEroczos9BZM7yVx",
      "review_date": "2025-08-20",
      "review_score": 1.0,
      "review_text": "The Spoon of theater kids but doomed to jazz hands. The pre-chorus drum fumble (\"breakdown\" is felony-level generous) is bad yet Florence can still out-sing the man yelling at pigeons behind the 7-Eleven.",
      "review_id": "florence-+-the-machine-everybody-scream-song-review"
    },
    {
      "song_artist": "Wednesday",
      "song_title": "Bitter Everyday",
      "song_release_date": "2025-08-19",
      "song_upload_date": "2025-08-19",
      "song_duration_sec": 202,
      "song_album": "Bleeds",
      "song_label": "Dead Oceans",
      "song_genre": "Shoegaze, Indie Rock",
      "song_mood": "Melancholic, Dreamy",
      "song_instrumentation": "Guitar, Drums, Bass, Vocals",
      "song_language": "English",
      "song_audio_url": "https://youtu.be/qGNRGk5TOLE?si=-9XE7b4vi1BZC-re",
      "review_date": "2025-08-19",
      "review_score": 0.5,
      "review_text": "I'd rather lick Kid Rock's dinghy than listen to any more 2020s shoegaze. Even mildew and regret got bored by this song.",
      "review_id": "wednesday-bitter-everyday-song-review"
    },
    {
      "song_artist": "Joyce Manor",
      "song_title": "All My Friends Are So Depressed",
      "song_release_date": "2025-08-18",
      "song_upload_date": "2025-08-18",
      "song_duration_sec": 166,
      "song_album": "Single",
      "song_label": "Epitaph Records",
      "song_genre": "Alternative Rock, Punk Rock, Emo",
      "song_mood": "Aggressive, Melancholic",
      "song_instrumentation": "Guitar, Drums, Bass, Vocals",
      "song_language": "English",
      "song_audio_url": "https://youtu.be/NDmJDdFl_jI?si=I99dZE6IilHRunLr",
      "review_date": "2025-08-18",
      "review_score": 1.0,
      "review_text": "Why is everyone trying to do alt-country poorly now. The Civil War reenactment of Old 97's no one asked for.",
      "review_id": "joyce-manor-all-my-friends-are-so-depressed-song-review"
    },
    {
      "song_artist": "Horses 4k",
      "song_title": "Barely a Horse, Mostly a Pony",
      "song_release_date": "2025-08-01",
      "song_upload_date": "2025-08-01",
      "song_duration_sec": 246,
      "song_album": "Nina",
      "song_label": "Independent",
      "song_genre": "Ambient, Ambient Country",
      "song_mood": "Contemplative, Melancholic",
      "song_instrumentation": "Guitar, Drums, Bass, Vocals",
      "song_language": "N/A",
      "song_audio_url": "https://horses4k.bandcamp.com/album/nina",
      "review_date": "2025-08-15",
      "review_score": 3.5,
      "review_text": "The sound of a horse staring at the sea, pondering frisbees and Tolstoy. Seagulls heckle. The wind; it smells like Elvis's hairspray. And zoomers — bless them — think they invented y'alternative just to ban it, like they're trying to outlaw sadness itself.",
      "review_id": "horses-4k-barely-a-horse-mostly-a-pony-song-review"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 4,
    "total": 4,
    "pages": 1
  }
};;;;;;

// Load reviews from embedded data
function loadReviews() {
  return reviewsData.reviews || [];
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
  const requestPath = event.path;
  const method = event.httpMethod;
  
  try {
    // API endpoints
    if (requestPath === '/.netlify/functions/reviews' || requestPath === '/api/reviews') {
      if (method === 'GET') {
        const reviews = loadReviews();
        return createResponse({
          reviews: reviews,
          pagination: {
            page: 1,
            per_page: reviews.length,
            total: reviews.length,
            pages: 1
          }
        });
      }
    }
    
    // Search endpoint
    if (requestPath === '/api/search') {
      if (method === 'GET') {
        const query = event.queryStringParameters?.q || '';
        if (!query) {
          return createResponse({ error: 'Search query required' }, 400);
        }
        
        const reviews = loadReviews();
        const results = [];
        const searchTerms = query.toLowerCase().split(' ');
        
        for (const review of reviews) {
          const searchableText = `${review.song_artist} ${review.song_title} ${review.review_text}`.toLowerCase();
          if (searchTerms.every(term => searchableText.includes(term))) {
            results.push(review);
          }
        }
        
        return createResponse({
          query: query,
          results: results,
          total_results: results.length
        });
      }
    }
    
    // Analytics endpoint
    if (requestPath === '/api/analytics') {
      if (method === 'GET') {
        const reviews = loadReviews();
        const ratingCounts = {};
        const artistCounts = {};
        
        for (const review of reviews) {
          ratingCounts[review.review_score] = (ratingCounts[review.review_score] || 0) + 1;
          artistCounts[review.song_artist] = (artistCounts[review.song_artist] || 0) + 1;
        }
        
        return createResponse({
          total_reviews: reviews.length,
          rating_distribution: ratingCounts,
          artist_counts: artistCounts
        });
      }
    }
    
    // Default response for unknown endpoints
    return createResponse({
      error: "Endpoint not found",
      available_endpoints: [
        "/api/reviews",
        "/api/search?q=<query>",
        "/api/analytics"
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
