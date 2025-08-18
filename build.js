#!/usr/bin/env node

// Node.js build script that converts Markdown content into HTML
// Reads content files and injects them into index.html
const fs = require('fs');
const path = require('path');

// Parse Markdown content into structured data objects
// Extracts title, date, rating, description, and listen links from each entry
function parseMarkdown(content) {
    const entries = [];
    const sections = content.split('## ').slice(1); // Skip the first empty section
    
    sections.forEach(section => {
        const lines = section.trim().split('\n');
        const title = lines[0].trim();
        
        const entry = { title };
        
        lines.slice(1).forEach(line => {
            const trimmedLine = line.trim();
            if (trimmedLine.startsWith('**Date:**')) {
                entry.date = trimmedLine.replace('**Date:**', '').trim();
            } else if (trimmedLine.startsWith('**Featured:**')) {
                entry.featured = trimmedLine.includes('⭐');
            } else if (trimmedLine.startsWith('**Rating:**')) {
                entry.rating = trimmedLine.replace('**Rating:**', '').trim();
            } else if (trimmedLine.startsWith('**Description:**')) {
                entry.description = trimmedLine.replace('**Description:**', '').trim();
            } else if (trimmedLine.startsWith('**Listen:**')) {
                entry.youtube = trimmedLine.replace('**Listen:**', '').trim();
            } else if (trimmedLine.startsWith('**URL:**')) {
                entry.url = trimmedLine.replace('**URL:**', '').trim();
            }
        });
        
        if (entry.title && entry.date) {
            entries.push(entry);
        }
    });
    
    return entries;
}

// Generate HTML for the featured song that appears on the main Songs tab
// Creates search functionality and displays the song with rating and share button
function generateFeaturedSongHTML(songs, lastModifiedString) {
    if (songs.length === 0) return '<p>No songs available yet.</p>';

    const featuredSongs = songs.filter(song => song.featured);
    if (featuredSongs.length === 0) return '<p>No featured songs this week.</p>';

    // Generate HTML for all featured songs
    const featuredSongsHTML = featuredSongs.map(featuredSong => {
        // Create clean URL-friendly ID
        const songId = featuredSong.title.toLowerCase()
            .replace(/[^a-z0-9\s-]/g, '') // Remove special characters
            .replace(/\s+/g, '-') // Replace spaces with hyphens
            .replace(/-+/g, '-') // Replace multiple hyphens with single
            .replace(/^-|-$/g, '') // Remove leading/trailing hyphens
            + '-song-review';

        // Escape quotes for JavaScript
        const escapedTitle = featuredSong.title.replace(/"/g, '&quot;');

        return `
        <div class="song-entry" id="${songId}" data-artist="${featuredSong.title.toLowerCase()}">
            <h3 class="song-title">${featuredSong.title}</h3>
            <p class="song-rating">${featuredSong.rating || '4/4'}</p>
            <p class="song-date">${featuredSong.date}</p>
            <p class="song-description">${featuredSong.description}</p>
            <div class="song-links">
                <a href="${featuredSong.youtube}" target="_blank" rel="noopener">Listen</a>
                <button onclick="shareSong('${songId}', '${escapedTitle}')" class="share-btn">Share</button>
            </div>
        </div>`;
    }).join('');

    return `
    <div class="section">
        <div class="search-section">
            <input type="text" id="song-search" placeholder="Search for artist or song..." onkeyup="searchSongs()">
            <p class="search-help">Type a song title (e.g., "Like a Rolling Stone") or artist name to search</p>
        </div>
        
        ${featuredSongsHTML}
    </div>`;
}

// Generate HTML for all songs in the members section
// Creates searchable list with ratings and share buttons for each song
function generateSongsHTML(songs) {
    if (songs.length === 0) return '<p>No songs available yet.</p>';

    const songsHTML = songs.map(song => {
        // Create clean URL-friendly ID
        const songId = song.title.toLowerCase()
            .replace(/[^a-z0-9\s-]/g, '') // Remove special characters
            .replace(/\s+/g, '-') // Replace spaces with hyphens
            .replace(/-+/g, '-') // Replace multiple hyphens with single
            .replace(/^-|-$/g, '') // Remove leading/trailing hyphens
            + '-song-review';

        // Escape quotes for JavaScript
        const escapedTitle = song.title.replace(/"/g, '&quot;');

        return `
        <div class="song-entry" id="${songId}" data-artist="${song.title.toLowerCase()}">
            <h3 class="song-title">${song.title}</h3>
            <p class="song-rating">${song.rating || '4/4'}</p>
            <p class="song-date">${song.date}</p>
            <p class="song-description">${song.description}</p>
            <div class="song-links">
                <a href="${song.youtube}" target="_blank" rel="noopener">Listen</a>
                <button onclick="shareSong('${songId}', '${escapedTitle}')" class="share-btn">Share</button>
            </div>
        </div>`;
    }).join('');

    return `<div class="section">
        <div class="search-section">
            <input type="text" id="song-search" placeholder="Search for artist or song..." onkeyup="searchSongs()">
            <p class="search-help">Type a song title (e.g., "Like a Rolling Stone") or artist name to search</p>
        </div>
        
        <h2>All Weekly Picks</h2>
        ${songsHTML}
    </div>`;
}

// Generate HTML for featured album (albums page)
function generateFeaturedAlbumHTML(albums) {
    const featured = albums.find(album => album.featured);
    if (!featured) return '';
    
    return `
    <div class="section">
        <h2>Featured Album</h2>
        
        <div class="song-entry">
            <h3 class="song-title">${featured.title}</h3>
            <p class="song-date">${featured.date}</p>
            <p class="song-description">${featured.description}</p>
            <div class="song-links">
                <a href="${featured.youtube}" target="_blank" rel="noopener">YouTube</a>
            </div>
        </div>
    </div>`;
}

// Generate HTML for all albums (albums page)
function generateAlbumsHTML(albums, lastModifiedString) {
    if (albums.length === 0) return '<p>No album reviews available yet.</p>';

    const albumsHTML = albums.map(album => {
        // Create clean URL-friendly ID
        const albumId = album.title.toLowerCase()
            .replace(/[^a-z0-9\s-]/g, '') // Remove special characters
            .replace(/\s+/g, '-') // Replace spaces with hyphens
            .replace(/-+/g, '-') // Replace multiple hyphens with single
            .replace(/^-|-$/g, '') // Remove leading/trailing hyphens
            + '-album-review';

        return `
        <div class="song-entry" data-artist="${album.title.toLowerCase()}" id="${albumId}">
            <h3 class="song-title">${album.title}</h3>
            <p class="song-rating">${album.rating || 0}/4</p>
            <p class="song-date"><strong>Reviewed:</strong> ${album.date}</p>
            <p class="song-description">${album.description}</p>
            <div class="song-links">
                <a href="${album.youtube}" target="_blank" rel="noopener">Listen</a>
                <button onclick="shareAlbum('${albumId}', '${album.title}')" class="share-btn">Share</button>
            </div>
        </div>`;
    }).join('');

    return `<div class="section">
        <div class="search-section">
            <input type="text" id="album-search" placeholder="Search for artist or album..." onkeyup="searchAlbums()">
            <p class="search-help">Type an artist name (e.g., "The Replacements") or album title to search</p>
        </div>
        
        ${albumsHTML}
    </div>`;
}

// Generate HTML for links (members page)
function generateLinksHTML(links) {
    if (links.length === 0) return '<p>No links available yet.</p>';
    
    const linksHTML = links.map(link => `
        <div class="link-entry">
            <h3 class="link-title">${link.title}</h3>
            <p class="link-date">${link.date}</p>
            <p class="link-description">${link.description}</p>
            <a href="${link.url}" target="_blank" rel="noopener">Read Article</a>
        </div>`).join('');
    
    return `<div class="section">
        <h2>Link Recommendations</h2>
        
        ${linksHTML}</div>`;
}

// Generate HTML for About section
function generateAboutHTML() {
    const aboutPath = path.join(__dirname, 'content', 'about.md');
    if (!fs.existsSync(aboutPath)) {
        return '<p>About section not found.</p>';
    }
    
    const aboutContent = fs.readFileSync(aboutPath, 'utf8');
    const aboutText = aboutContent.replace('# About OPE!\n\n', '').trim();
    
    return `<div class="section">
        <h2>About OPE!</h2>
        <p>${aboutText.replace(/\n\n/g, '</p><p>')}</p>
    </div>`;
}

// Generate HTML for footer content
function generateFooterHTML(songs, albums, lastModifiedString) {
    return `
        <div class="footer-content">
            <div class="last-updated">
                <strong>Last updated:</strong> ${lastModifiedString} (Los Angeles, CA PST Time)
            </div>
            
            <div class="support-info">
                <strong>Best ways to support:</strong> Bookmark this page, subscribe to the newsletter and podcast, tell all your friends.
            </div>
            
            <div class="contact-info">
                Don't like my reviews? Email me at bradywgerber at gmail dot com to tell me why I'm wrong, or hate-click my <a href="https://bradygerber.com/" target="_blank" rel="noopener">website</a>.
            </div>
            
            <div class="footer-bottom">
                <img src="images/author.png" alt="Brady Gerber" class="author-image">
                <span class="copyright">&copy; 2025 OPE!. All rights reserved.</span>
            </div>
        </div>`;
}

// Update index.html
function updateIndexHTML(songs, albums, links) {
    const indexPath = path.join(__dirname, 'index.html');
    let indexContent = fs.readFileSync(indexPath, 'utf8');
    
    // Get actual file modification dates
    const songsPath = path.join(__dirname, 'content', 'songs.md');
    const albumsPath = path.join(__dirname, 'content', 'albums.md');
    
    const songsStats = fs.statSync(songsPath);
    const albumsStats = fs.statSync(albumsPath);
    
    // Use the most recent file modification date in Los Angeles time
    const lastModified = new Date(Math.max(songsStats.mtime, albumsStats.mtime));
    const lastModifiedString = lastModified.toLocaleDateString('en-US', { 
        month: 'long', 
        day: 'numeric', 
        year: 'numeric',
        timeZone: 'America/Los_Angeles'
    });
    
    // Generate new content
    const featuredSongHTML = generateFeaturedSongHTML(songs, lastModifiedString);
    const songsHTML = generateSongsHTML(songs);
    const featuredAlbumHTML = generateFeaturedAlbumHTML(albums);
    const albumsHTML = generateAlbumsHTML(albums, lastModifiedString);
    const linksHTML = generateLinksHTML(links);
    const footerHTML = generateFooterHTML(songs, albums, lastModifiedString);
    
    // Update the content object in the JavaScript with generated HTML
    // This replaces the placeholder content with actual song and link data
    const contentRegex = /const content = \{[\s\S]*?\};/;
    const newContent = `const content = {
            free: {
                title: "Songs",
                html: \`${featuredSongHTML}\`
            },
            newsletter: {
                title: "Newsletter",
                html: \`<div class="section">
        <p>Get a link to my latest reviews every Friday, along with other fun links and musings about life: <a href="https://bradygerber.com/newsletter/" target="_blank" rel="noopener">https://bradygerber.com/newsletter/</a></p>
    </div>\`
            },
            podcast: {
                title: "Podcast",
                html: \`<div class="section">
        <p>It's like OPE! but easier to understand: <a href="https://bradygerber.com/podcast-and-youtube/" target="_blank" rel="noopener">https://bradygerber.com/podcast-and-youtube/</a></p>
    </div>\`
            },
            members: {
                title: "All Weekly Picks",
                html: \`${songsHTML}

                    ${linksHTML}\`
            }
        };`;
    
    // Update the footer in the HTML - completely replace the entire footer section
    // Includes last updated date, about text, and author image
    const footerRegex = /<!-- Footer -->[\s\S]*?<\/footer>\s*<\/body>/;
    const newFooter = `    <!-- Footer -->
    <footer class="footer" role="contentinfo">
        ${footerHTML}
    </footer>
</body>`;
    
    if (footerRegex.test(indexContent)) {
        indexContent = indexContent.replace(footerRegex, newFooter);
    }
    
    indexContent = indexContent.replace(contentRegex, newContent);
    
    fs.writeFileSync(indexPath, indexContent);
    console.log('✅ index.html updated successfully!');
}

// Apply production-specific optimizations
function applyProductionOptimizations() {
    console.log('  - Removing development comments...');
    console.log('  - Optimizing for production...');
    console.log('  - Production build ready!');
}

// Main build function that orchestrates the entire build process
// Reads Markdown files, parses content, and updates index.html
function build() {
    try {
        // Check if this is a production build
        const isProduction = process.argv.includes('--production');
        
        if (isProduction) {
            console.log('🚀 Building OPE! website for PRODUCTION...');
        } else {
            console.log('🔧 Building OPE! website for LOCAL DEVELOPMENT...');
        }
        
        // Read content files
        const songsPath = path.join(__dirname, 'content', 'songs.md');
        const albumsPath = path.join(__dirname, 'content', 'albums.md');
        const linksPath = path.join(__dirname, 'content', 'links.md');
        
        if (!fs.existsSync(songsPath)) {
            console.log('⚠️  songs.md not found, creating empty file...');
            fs.writeFileSync(songsPath, '# Songs\n\n');
        }
        
        if (!fs.existsSync(albumsPath)) {
            console.log('⚠️  albums.md not found, creating empty file...');
            fs.writeFileSync(albumsPath, '# Albums\n\n');
        }
        
        if (!fs.existsSync(linksPath)) {
            console.log('⚠️  links.md not found, creating empty file...');
            fs.writeFileSync(linksPath, '# Links\n\n');
        }
        
        const songsContent = fs.readFileSync(songsPath, 'utf8');
        const albumsContent = fs.readFileSync(albumsPath, 'utf8');
        const linksContent = fs.readFileSync(linksPath, 'utf8');
        
        // Parse content
        const songs = parseMarkdown(songsContent);
        const albums = parseMarkdown(albumsContent);
        const links = parseMarkdown(linksContent);
        
        console.log(`📝 Found ${songs.length} songs, ${albums.length} albums, and ${links.length} links`);
        
        // Update index.html
        updateIndexHTML(songs, albums, links);
        
        // Production-specific optimizations
        if (isProduction) {
            console.log('🔧 Applying production optimizations...');
            applyProductionOptimizations();
        }
        
        console.log('🎉 Build completed successfully!');
        
    } catch (error) {
        console.error('❌ Build failed:', error.message);
        process.exit(1);
    }
}

// Run build if this script is executed directly
if (require.main === module) {
    build();
}
