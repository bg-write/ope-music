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
    // In production, read from the data file in root directory
    const dataPath = path.join(__dirname, '..', 'billboard_chart_data.json');
    
    console.log('Looking for data file at:', dataPath);
    console.log('File exists:', fs.existsSync(dataPath));
    
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
      // Fallback to embedded data if file doesn't exist
      const billboardData = {
      "chart_date": "2025-08-31",
      "total_entries": 100,
      "chart_entries": [
        {
          "rank": 1,
          "title": "Golden",
          "artist": "HUNTR/X: EJAE, Audrey Nuna & REI AMI",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.431125"
        },
        {
          "rank": 2,
          "title": "Ordinary",
          "artist": "Alex Warren",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.434176"
        },
        {
          "rank": 3,
          "title": "What I Want",
          "artist": "Morgan Wallen Featuring Tate McRae",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.436750"
        },
        {
          "rank": 4,
          "title": "Your Idol",
          "artist": "Saja Boys: Andrew Choi, Neckwav, Danny Chung, Kevin Woo & samUIL Lee",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.439654"
        },
        {
          "rank": 5,
          "title": "Soda Pop",
          "artist": "Saja Boys: Andrew Choi, Neckwav, Danny Chung, Kevin Woo & samUIL Lee",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.443099"
        },
        {
          "rank": 6,
          "title": "Love Me Not",
          "artist": "Ravyn Lenae",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.448876"
        },
        {
          "rank": 7,
          "title": "Lose Control",
          "artist": "Teddy Swims",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.462473"
        },
        {
          "rank": 8,
          "title": "Daisies",
          "artist": "Justin Bieber",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.472606"
        },
        {
          "rank": 9,
          "title": "Just In Case",
          "artist": "Morgan Wallen",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.494105"
        },
        {
          "rank": 10,
          "title": "How It's Done",
          "artist": "HUNTR/X: EJAE, Audrey Nuna & REI AMI",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.505697"
        },
        {
          "rank": 11,
          "title": "Die With A Smile",
          "artist": "Lady Gaga & Bruno Mars",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.512376"
        },
        {
          "rank": 12,
          "title": "Good News",
          "artist": "Shaboozey",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.523730"
        },
        {
          "rank": 13,
          "title": "A Bar Song (Tipsy)",
          "artist": "Shaboozey",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.533132"
        },
        {
          "rank": 14,
          "title": "Manchild",
          "artist": "Sabrina Carpenter",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.550313"
        },
        {
          "rank": 15,
          "title": "Mutt",
          "artist": "Leon Thomas",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.558940"
        },
        {
          "rank": 16,
          "title": "I'm The Problem",
          "artist": "Morgan Wallen",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.566279"
        },
        {
          "rank": 17,
          "title": "Beautiful Things",
          "artist": "Benson Boone",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.575526"
        },
        {
          "rank": 18,
          "title": "Pink Pony Club",
          "artist": "Chappell Roan",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.587357"
        },
        {
          "rank": 19,
          "title": "I Got Better",
          "artist": "Morgan Wallen",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.594145"
        },
        {
          "rank": 20,
          "title": "What It Sounds Like",
          "artist": "HUNTR/X: EJAE, Audrey Nuna & REI AMI",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.601543"
        },
        {
          "rank": 21,
          "title": "Luther",
          "artist": "Kendrick Lamar & SZA",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.607761"
        },
        {
          "rank": 22,
          "title": "Birds Of A Feather",
          "artist": "Billie Eilish",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.614812"
        },
        {
          "rank": 23,
          "title": "Free",
          "artist": "Rumi, JINU, EJAE & Andrew Choi",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.623432"
        },
        {
          "rank": 24,
          "title": "I Had Some Help",
          "artist": "Post Malone Featuring Morgan Wallen",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.639127"
        },
        {
          "rank": 25,
          "title": "Takedown",
          "artist": "HUNTR/X: EJAE, Audrey Nuna & REI AMI",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.647515"
        },
        {
          "rank": 26,
          "title": "Sorry I'm Here For Someone Else",
          "artist": "Benson Boone",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.651129"
        },
        {
          "rank": 27,
          "title": "Undressed",
          "artist": "sombr",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.654768"
        },
        {
          "rank": 28,
          "title": "The Subway",
          "artist": "Chappell Roan",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.657777"
        },
        {
          "rank": 29,
          "title": "Yukon",
          "artist": "Justin Bieber",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.661793"
        },
        {
          "rank": 30,
          "title": "Mystical Magical",
          "artist": "Benson Boone",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.665003"
        },
        {
          "rank": 31,
          "title": "Back To Friends",
          "artist": "sombr",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.667951"
        },
        {
          "rank": 32,
          "title": "It Depends",
          "artist": "Chris Brown Featuring Bryson Tiller",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.671091"
        },
        {
          "rank": 33,
          "title": "All The Way",
          "artist": "BigXthaPlug Featuring Bailey Zimmerman",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.674059"
        },
        {
          "rank": 34,
          "title": "Backup Plan",
          "artist": "Bailey Zimmerman & Luke Combs",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.677572"
        },
        {
          "rank": 35,
          "title": "Folded",
          "artist": "Kehlani",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.680892"
        },
        {
          "rank": 36,
          "title": "Burning Blue",
          "artist": "Mariah The Scientist",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.684312"
        },
        {
          "rank": 37,
          "title": "Blue Strips",
          "artist": "Jessie Murph",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.687472"
        },
        {
          "rank": 38,
          "title": "30 For 30",
          "artist": "SZA With Kendrick Lamar",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.690130"
        },
        {
          "rank": 39,
          "title": "After All The Bars Are Closed",
          "artist": "Thomas Rhett",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.693574"
        },
        {
          "rank": 40,
          "title": "Happen To Me",
          "artist": "Russell Dickerson",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.696839"
        },
        {
          "rank": 41,
          "title": "Worst Way",
          "artist": "Riley Green",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.699880"
        },
        {
          "rank": 42,
          "title": "APT.",
          "artist": "ROSE & Bruno Mars",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.702583"
        },
        {
          "rank": 43,
          "title": "Bar None",
          "artist": "Jordan Davis",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.705942"
        },
        {
          "rank": 44,
          "title": "Love Somebody",
          "artist": "Morgan Wallen",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.708916"
        },
        {
          "rank": 45,
          "title": "What Did I Miss?",
          "artist": "Drake",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.712333"
        },
        {
          "rank": 46,
          "title": "Nokia",
          "artist": "Drake",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.715560"
        },
        {
          "rank": 47,
          "title": "Back In The Saddle",
          "artist": "Luke Combs",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.718728"
        },
        {
          "rank": 48,
          "title": "Bottle Rockets",
          "artist": "Scotty McCreery & Hootie & The Blowfish",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.722215"
        },
        {
          "rank": 49,
          "title": "Sugar On My Tongue",
          "artist": "Tyler, The Creator",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.726924"
        },
        {
          "rank": 50,
          "title": "No Broke Boys",
          "artist": "Disco Lines & Tinashe",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.731973"
        },
        {
          "rank": 51,
          "title": "6 Months Later",
          "artist": "Megan Moroney",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.737952"
        },
        {
          "rank": 52,
          "title": "Miami",
          "artist": "Morgan Wallen Featuring Lil Wayne & Rick Ross",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.741276"
        },
        {
          "rank": 53,
          "title": "Takedown",
          "artist": "JEONGYEON, JIHYO & CHAEYOUNG Of TWICE",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.747651"
        },
        {
          "rank": 54,
          "title": "Somewhere Over Laredo",
          "artist": "Lainey Wilson",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.751942"
        },
        {
          "rank": 55,
          "title": "20 Cigarettes",
          "artist": "Morgan Wallen",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.755924"
        },
        {
          "rank": 56,
          "title": "House Again",
          "artist": "Hudson Westbrook",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.759163"
        },
        {
          "rank": 57,
          "title": "Strategy",
          "artist": "TWICE",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.763463"
        },
        {
          "rank": 58,
          "title": "Amen",
          "artist": "Shaboozey & Jelly Roll",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.766290"
        },
        {
          "rank": 59,
          "title": "Wildflower",
          "artist": "Billie Eilish",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.769475"
        },
        {
          "rank": 60,
          "title": "Outside",
          "artist": "Cardi B",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.772405"
        },
        {
          "rank": 61,
          "title": "Hell At Night",
          "artist": "BigXthaPlug & Ella Langley",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.775016"
        },
        {
          "rank": 62,
          "title": "Your Way's Better",
          "artist": "Forrest Frank",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.778989"
        },
        {
          "rank": 63,
          "title": "Just Keep Watching",
          "artist": "Tate McRae",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.782144"
        },
        {
          "rank": 64,
          "title": "So Far So Fake",
          "artist": "Pierce The Veil",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.785280"
        },
        {
          "rank": 65,
          "title": "Shake It To The Max (Fly)",
          "artist": "MOLIY, Silent Addy, Skillibeng & Shenseea",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.787891"
        },
        {
          "rank": 66,
          "title": "Eternity",
          "artist": "Alex Warren",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.790871"
        },
        {
          "rank": 67,
          "title": "I Ain't Coming Back",
          "artist": "Morgan Wallen Featuring Post Malone",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.794862"
        },
        {
          "rank": 68,
          "title": "Better Me For You (Brown Eyes)",
          "artist": "Max McNown",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.797577"
        },
        {
          "rank": 69,
          "title": "Marlboro Rojo",
          "artist": "Fuerza Regida",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.800926"
        },
        {
          "rank": 70,
          "title": "Imaginary Playerz",
          "artist": "Cardi B",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.804130"
        },
        {
          "rank": 71,
          "title": "Party 4 U",
          "artist": "Charli xcx",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.807546"
        },
        {
          "rank": 72,
          "title": "Gabriela",
          "artist": "KATSEYE",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.811271"
        },
        {
          "rank": 73,
          "title": "Which One",
          "artist": "Drake & Central Cee",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.814130"
        },
        {
          "rank": 74,
          "title": "Jump",
          "artist": "BLACKPINK",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.816897"
        },
        {
          "rank": 75,
          "title": "Superman",
          "artist": "Morgan Wallen",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.819737"
        },
        {
          "rank": 76,
          "title": "Rather Lie",
          "artist": "Playboi Carti & The Weeknd",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.822647"
        },
        {
          "rank": 77,
          "title": "Last One To Know",
          "artist": "Gavin Adcock",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.825585"
        },
        {
          "rank": 78,
          "title": "Don't Mind If I Do",
          "artist": "Riley Green Featuring Ella Langley",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.830565"
        },
        {
          "rank": 79,
          "title": "Revolving Door",
          "artist": "Tate McRae",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.834845"
        },
        {
          "rank": 80,
          "title": "Nice To Meet You",
          "artist": "Myles Smith",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.839691"
        },
        {
          "rank": 81,
          "title": "Sparks",
          "artist": "Coldplay",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.844265"
        },
        {
          "rank": 82,
          "title": "Went Legit",
          "artist": "G Herbo",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.848687"
        },
        {
          "rank": 83,
          "title": "Frecuencia",
          "artist": "Dareyes de La Sierra",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.851415"
        },
        {
          "rank": 84,
          "title": "Hard Fought Hallelujah",
          "artist": "Brandon Lake X Jelly Roll",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.854481"
        },
        {
          "rank": 85,
          "title": "Ring Ring Ring",
          "artist": "Tyler, The Creator",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.857550"
        },
        {
          "rank": 86,
          "title": "Heart Of Stone",
          "artist": "Jelly Roll",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.861782"
        },
        {
          "rank": 87,
          "title": "TN",
          "artist": "Morgan Wallen",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.865567"
        },
        {
          "rank": 88,
          "title": "Typa",
          "artist": "GloRilla",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.868946"
        },
        {
          "rank": 89,
          "title": "Just Say Dat",
          "artist": "Gunna",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.872031"
        },
        {
          "rank": 90,
          "title": "Cliche",
          "artist": "mgk",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.875049"
        },
        {
          "rank": 91,
          "title": "Let Down",
          "artist": "Radiohead",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.879440"
        },
        {
          "rank": 92,
          "title": "Tu Sancho",
          "artist": "Fuerza Regida",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.882664"
        },
        {
          "rank": 93,
          "title": "wgft",
          "artist": "Gunna Featuring Burna Boy",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.885549"
        },
        {
          "rank": 94,
          "title": "Bloodline",
          "artist": "Alex Warren With Jelly Roll",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.888440"
        },
        {
          "rank": 95,
          "title": "Is It A Crime",
          "artist": "Mariah The Scientist & Kali Uchis",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.891311"
        },
        {
          "rank": 96,
          "title": "Forever Be Mine",
          "artist": "Gunna Featuring Wizkid",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.895347"
        },
        {
          "rank": 97,
          "title": "Somebody",
          "artist": "Latto",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.898566"
        },
        {
          "rank": 98,
          "title": "What Kinda Man",
          "artist": "Parker McCollum",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.901663"
        },
        {
          "rank": 99,
          "title": "Country Song Came On",
          "artist": "Luke Bryan",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.904652"
        },
        {
          "rank": 100,
          "title": "Napoleon",
          "artist": "$uicideboy$",
          "chart_date": "2025-08-31",
          "scraped_at": "2025-08-31T15:15:28.908151"
        }
      ],
      "top_artists": [
        {
          "rank": 1,
          "artist": "Morgan Wallen",
          "total_score": 402,
          "chart_positions": [
            9,
            16,
            19,
            44,
            55,
            75,
            87
          ],
          "songs_count": 7
        },
        {
          "rank": 2,
          "artist": "HUNTR/X: EJAE, Audrey Nuna & REI AMI",
          "total_score": 348,
          "chart_positions": [
            1,
            10,
            20,
            25
          ],
          "songs_count": 4
        },
        {
          "rank": 3,
          "artist": "Benson Boone",
          "total_score": 230,
          "chart_positions": [
            17,
            26,
            30
          ],
          "songs_count": 3
        },
        {
          "rank": 4,
          "artist": "Saja Boys: Andrew Choi, Neckwav, Danny Chung, Kevin Woo & samUIL Lee",
          "total_score": 193,
          "chart_positions": [
            4,
            5
          ],
          "songs_count": 2
        },
        {
          "rank": 5,
          "artist": "Shaboozey",
          "total_score": 177,
          "chart_positions": [
            12,
            13
          ],
          "songs_count": 2
        },
        {
          "rank": 6,
          "artist": "Justin Bieber",
          "total_score": 165,
          "chart_positions": [
            8,
            29
          ],
          "songs_count": 2
        },
        {
          "rank": 7,
          "artist": "Chappell Roan",
          "total_score": 156,
          "chart_positions": [
            18,
            28
          ],
          "songs_count": 2
        },
        {
          "rank": 8,
          "artist": "sombr",
          "total_score": 144,
          "chart_positions": [
            27,
            31
          ],
          "songs_count": 2
        },
        {
          "rank": 9,
          "artist": "Alex Warren",
          "total_score": 134,
          "chart_positions": [
            2,
            66
          ],
          "songs_count": 2
        },
        {
          "rank": 10,
          "artist": "Billie Eilish",
          "total_score": 121,
          "chart_positions": [
            22,
            59
          ],
          "songs_count": 2
        }
      ]
    };

      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          data: billboardData,
          message: "Billboard Hot 100 data retrieved successfully (fallback)",
          source: "fallback_data",
          deployed_at: new Date().toISOString()
        })
      };
    }

  } catch (error) {
    console.error('Error in Billboard function:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: 'Internal server error',
        message: error.message
      })
    };
  }
};
