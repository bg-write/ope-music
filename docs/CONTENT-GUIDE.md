# OPE! Content Management Guide

## 🚀 **Status: Ready for Launch!**

Your OPE! website is fully functional and ready to go live. This guide shows you how to manage content using simple Markdown files.

## 📝 **Content Files Overview**

All your content lives in the `content/` folder as simple Markdown (`.md`) files:

- **`songs.md`** - Weekly song picks (one featured with ⭐)
- **`albums.md`** - Album reviews with ratings
- **`links.md`** - Link recommendations (optional)
- **`about.md`** - About section text

## 🎵 **Managing Songs (`content/songs.md`)**

### **Format for Each Song:**
```markdown
## Artist Name - "Song Title"
**Date:** January 15, 2025
**Featured:** ⭐  (only one song should have this)
**Description:** Your thoughts about why you picked this song...
**Listen:** https://youtube.com/watch?v=... (or Bandcamp, Spotify, etc.)
```

### **Example:**
```markdown
## Horses 4k - "Barely a Horse, Mostly a Pony"
**Date:** August 15, 2025
**Featured:** ⭐
**Description:** The sound of a horse looking out longingly at sea...
**Listen:** https://horses4k.bandcamp.com/album/nina
```

### **Important Notes:**
- **Only one song** should have `**Featured:** ⭐` - this becomes your "Song of the Week"
- **Date format:** Use consistent date formatting
- **Listen links:** Can be YouTube, Bandcamp, Spotify, or any music platform
- **Description:** Write whatever you want - be yourself!

## 🎼 **Managing Album Reviews (`content/albums.md`)**

### **Format for Each Album:**
```markdown
## Album Title - Artist Name (Year)
**Date:** January 15, 2025
**Rating:** 3 (1-4 scale)
**Description:** Your review and thoughts about the album...
**Listen:** https://youtube.com/watch?v=... (or any music platform)
```

### **Example:**
```markdown
## Currents - Tame Impala (2015)
**Date:** August 10, 2025
**Rating:** 2
**Description:** This album created a new type of guy and I hate it.
**Listen:** https://www.youtube.com/watch?v=wycjnCCgUes
```

### **Rating System:**
- **1/4** - Didn't like it
- **2/4** - Meh, not great
- **3/4** - Pretty good
- **4/4** - Loved it

## 🔗 **Managing Links (`content/links.md`)**

### **Format for Each Link:**
```markdown
## Article Title
**Date:** January 15, 2025
**Description:** Brief description of why this link is worth sharing...
**URL:** https://example.com/article
```

## ℹ️ **Managing About Section (`content/about.md`)**

Keep it simple:
```markdown
# About OPE!

OPE! is a music "blog." Leave me alone.
```

## 🛠 **Workflow: Adding New Content**

### **1. Edit the Markdown File**
Open the appropriate `.md` file in any text editor and add your new entry at the top.

### **2. Build the Website**
Run this command in your terminal:
```bash
npm run build
```

### **3. Preview Changes**
Open `index.html` in your browser to see the updates.

### **4. Deploy (when ready)**
Upload the updated files to your hosting platform.

## 📱 **Content Tips**

### **For Songs:**
- Keep descriptions personal and authentic
- Use the ⭐ feature for your current favorite
- Include diverse genres and time periods
- Add context about why you chose it

### **For Album Reviews:**
- Be honest with ratings
- Include release years
- Write what you actually think
- Keep descriptions concise but meaningful

### **General:**
- **Be consistent** with date formatting
- **Test your links** before publishing
- **Keep it simple** - the content speaks for itself
- **Update regularly** - even weekly is fine

## 🔄 **Auto-Watch Mode (Optional)**

If you want the site to automatically rebuild when you save changes:
```bash
npm run watch
```

This will watch your content files and rebuild automatically.

## 🚀 **Ready to Launch!**

Your OPE! website is **production-ready** with:
- ✅ **Working search** for songs and albums
- ✅ **Mobile-responsive design**
- ✅ **Easy content updates** via Markdown
- ✅ **Professional appearance**
- ✅ **Shareable individual links**

**Next step:** Add some real content and launch! 🎵

---

**Need help?** Check the main README.md or deployment-guide.md for more details.
