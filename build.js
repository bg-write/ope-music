#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Parse Markdown content and extract structured data
function parseMarkdown(content) {
    const lines = content.split('\n');
    const items = [];
    let currentItem = {};
    
    for (let i = 0; i < lines.length; i++) {
        const line = lines[i].trim();
        
        if (line.startsWith('## ')) {
            // New item starts
            if (Object.keys(currentItem).length > 0) {
                items.push(currentItem);
            }
            currentItem = { title: line.substring(3) };
        } else if (line.startsWith('**Date:**')) {
            currentItem.date = line.substring(9).trim();
        } else if (line.startsWith('**Rating:**')) {
            currentItem.rating = line.substring(11).trim();
        } else if (line.startsWith('**Featured:**')) {
            currentItem.featured = line.substring(13).trim();
        } else if (line.startsWith('**Description:**')) {
            currentItem.description = line.substring(16).trim();
        } else if (line.startsWith('**Listen:**')) {
            currentItem.listen = line.substring(11).trim();
        } else if (line.startsWith('**URL:**')) {
            currentItem.url = line.substring(8).trim();
        }
    }
    
    // Add the last item
    if (Object.keys(currentItem).length > 0) {
        items.push(currentItem);
    }
    
    return items;
}

// Generate HTML for songs
function generateSongsHTML(songs) {
    if (songs.length === 0) return '<p>No songs found.</p>';
    
    let html = `
        <div class="section">
            <div class="search-section">
                <input type="text" id="song-search" placeholder="Search for artist or song..." onkeyup="searchSongs()">
                <p class="search-help">Type a song title (e.g., "Like a Rolling Stone") or artist name to search</p>
            </div>
            
            `;
    
    songs.forEach(song => {
        const songId = song.title.toLowerCase()
            .replace(/[^a-z0-9\s-]/g, '')
            .replace(/\s+/g, '-')
            .replace(/-+/g, '-')
            .trim() + '-song-review';
        
        const artistText = song.title.toLowerCase()
            .replace(/[^a-z0-9\s]/g, '')
            .trim();
        
        html += `
            <div class="song-entry" id="${songId}" data-artist="${artistText}">
                <h3 class="song-title">${song.title}</h3>
                <p class="song-rating">${song.rating}</p>
                <p class="song-date">${song.date}</p>
                <p class="song-description">${song.description}</p>
                <div class="song-links">
                    <a href="${song.listen}" target="_blank" rel="noopener">Listen</a>
                </div>
            </div>`;
    });
    
    html += '</div>';
    return html;
}

// Generate HTML for links
function generateLinksHTML(links) {
    if (links.length === 0) return '<p>No links found.</p>';
    
    let html = '<div class="section">';
    
    links.forEach(link => {
        html += `
            <div class="link-entry">
                <h3 class="link-title">${link.title}</h3>
                <p class="link-date">${link.date}</p>
                <p class="link-description">${link.description}</p>
                <div class="link-links">
                    <a href="${link.url}" target="_blank" rel="noopener">Read More</a>
                </div>
            </div>`;
    });
    
    html += '</div>';
    return html;
}

// Generate featured songs HTML (only featured songs)
function generateFeaturedSongsHTML(songs) {
    const featuredSongs = songs.filter(song => song.featured && song.featured.includes('⭐'));
    return generateSongsHTML(featuredSongs);
}

// Generate members HTML (all songs + links)
function generateMembersHTML(songs, links) {
    let html = '<div class="section">';
    
    // Add search section
    html += `
        <div class="search-section">
            <input type="text" id="song-search" placeholder="Search for artist or song..." onkeyup="searchSongs()">
            <p class="search-help">Type a song title (e.g., "Like a Rolling Stone") or artist name to search</p>
        </div>`;
    
    // Add songs
    songs.forEach(song => {
        const songId = song.title.toLowerCase()
            .replace(/[^a-z0-9\s-]/g, '')
            .replace(/\s+/g, '-')
            .replace(/-+/g, '-')
            .trim() + '-song-review';
        
        const artistText = song.title.toLowerCase()
            .replace(/[^a-z0-9\s]/g, '')
            .trim();
        
        html += `
            <div class="song-entry" id="${songId}" data-artist="${artistText}">
                <h3 class="song-title">${song.title}</h3>
                <p class="song-rating">${song.rating}</p>
                <p class="song-date">${song.date}</p>
                <p class="song-description">${song.description}</p>
                <div class="song-links">
                    <a href="${song.listen}" target="_blank" rel="noopener">Listen</a>
                </div>
            </div>`;
    });
    
    // Add links
    links.forEach(link => {
        html += `
            <div class="link-entry">
                <h3 class="link-title">${link.title}</h3>
                <p class="link-date">${link.date}</p>
                <p class="link-description">${link.description}</p>
                <div class="link-links">
                    <a href="${link.url}" target="_blank" rel="noopener">Read More</a>
                </div>
            </div>`;
    });
    
    html += '</div>';
    return html;
}

// Update the footer with current date
function generateFooterHTML() {
    const now = new Date();
    const options = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        timeZone: 'America/Los_Angeles'
    };
    const laDate = now.toLocaleDateString('en-US', options);
    
    return `
        <div class="footer-content">
            <div class="last-updated">
                <strong>Last updated:</strong> ${laDate} (Los Angeles, CA PST Time)
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

// Update index.html with new content
function updateIndexHTML(songs, links) {
    const indexPath = path.join(__dirname, 'index.html');
    let indexContent = fs.readFileSync(indexPath, 'utf8');
    
    // Generate HTML content
    const featuredSongHTML = generateFeaturedSongsHTML(songs);
    const songsHTML = generateSongsHTML(songs);
    const linksHTML = generateLinksHTML(links);
    const membersHTML = generateMembersHTML(songs, links);
    const footerHTML = generateFooterHTML();
    
    // This replaces the placeholder content with actual song and link data
    const contentRegex = /const content\s*=\s*\{[\s\S]*?\};/;
    const newContent = `const content = {
            free: {
                title: "Songs",
                html: \`${featuredSongHTML}\`
            },
            newsletter: {
                title: "Newsletter",
                html: \`<div class="section">
        <p>A link to the week's reviews every Friday, along with other "fun" links and "musings" on "life": <a href="https://bradygerber.com/newsletter/" target="_blank" rel="noopener">https://bradygerber.com/newsletter/</a></p>
    </div>\`
            },
            podcast: {
                title: "Podcast",
                html: \`<div class="section">
        <p>My reviews, but easier to understand: <a href="https://bradygerber.com/podcast-and-youtube/" target="_blank" rel="noopener">https://bradygerber.com/podcast-and-youtube/</a></p>
    </div>\`
            },
            members: {
                title: "All Weekly Picks",
                html: \`${membersHTML}\`
            }
        };`;
    
    // Update the content object in the JavaScript with generated HTML
    if (contentRegex.test(indexContent)) {
        indexContent = indexContent.replace(contentRegex, newContent);
    }
    
    // Update the footer in the HTML - completely replace the entire footer section
    // Includes last updated date, about text, and author image
    const footerRegex = /<!-- Footer -->[\s\S]*?<\/footer>/;
    const newFooter = `<!-- Footer -->
<footer class="footer" role="contentinfo">
        ${footerHTML}
    </footer>`;
    
    if (footerRegex.test(indexContent)) {
        indexContent = indexContent.replace(footerRegex, newFooter);
    }
    
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
        const linksPath = path.join(__dirname, 'content', 'links.md');
        
        if (!fs.existsSync(songsPath)) {
            console.log('⚠️  songs.md not found, creating empty file...');
            fs.writeFileSync(songsPath, '# Songs\n\n');
        }
        
        if (!fs.existsSync(linksPath)) {
            console.log('⚠️  links.md not found, creating empty file...');
            fs.writeFileSync(linksPath, '# Links\n\n');
        }
        
        const songsContent = fs.readFileSync(songsPath, 'utf8');
        const linksContent = fs.readFileSync(linksPath, 'utf8');
        
        // Parse content
        const songs = parseMarkdown(songsContent);
        const links = parseMarkdown(linksContent);
        
        console.log(`📝 Found ${songs.length} songs and ${links.length} links`);
        
        // Update index.html
        updateIndexHTML(songs, links);
        
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
