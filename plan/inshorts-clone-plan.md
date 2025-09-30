# Inshorts Clone Implementation Plan

## Requirement ID: e55aa6da-dcc1-42d2-93c7-04ee6e2d9b0a

## Overview
Build a news summary website similar to Inshorts with:
- AI-generated concise news summaries
- Clean scrollable feed interface
- Green color theme
- Source links to original articles

## Technical Approach

### Backend APIs (FastAPI)
1. **POST /api/news/fetch** - Fetch and generate new news summaries
   - Use SearchAgent to search for latest news on various topics
   - Generate concise summaries using AI
   - Store in MongoDB with timestamp, title, summary, source URL, category
   - Return newly created summaries

2. **GET /api/news** - Get all news summaries
   - Fetch from MongoDB sorted by timestamp (newest first)
   - Optional pagination
   - Return list of news items

3. **GET /api/news/refresh** - Auto-refresh news feed
   - Background job to fetch new news periodically
   - Search for trending topics and latest news

### Frontend (React)
1. **Home Page** - Main news feed
   - Vertical scrollable feed
   - Card-based layout with green theme
   - Each card shows: title, summary, source, timestamp
   - "Read more" link to original article
   - Pull-to-refresh or auto-refresh button
   - Loading states with skeleton cards

2. **Design System**
   - Green primary color (#2ecc71 or similar)
   - Clean typography
   - Card shadows and hover effects
   - Responsive mobile-first design

### Database Schema
```
news_summaries collection:
{
  id: uuid,
  title: string,
  summary: string (60 words max),
  source_url: string,
  source_name: string,
  category: string,
  timestamp: datetime,
  created_at: datetime
}
```

## Implementation Steps

### Phase 1: Backend APIs
1. Create news models and schemas
2. Implement /api/news/fetch endpoint with SearchAgent integration
3. Implement /api/news GET endpoint
4. Test APIs thoroughly

### Phase 2: Frontend
1. Create NewsCard component
2. Build main feed page
3. Implement API integration
4. Add loading and error states
5. Style with green theme

### Phase 3: Testing & Polish
1. Test news fetching from various topics
2. Test frontend display and interactions
3. Verify responsive design
4. Build and deploy

## Acceptance Criteria
- ✅ User can see a feed of news summaries
- ✅ Each summary is concise (similar to Inshorts style)
- ✅ Green color theme throughout
- ✅ Click to read full article on source website
- ✅ Responsive design works on mobile and desktop
- ✅ News content is sourced via search and AI summarization
