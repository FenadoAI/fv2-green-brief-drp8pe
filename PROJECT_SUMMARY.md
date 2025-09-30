# NewsShorts - Inshorts Clone

## Project Overview
A web-based news summary service inspired by Inshorts, featuring AI-generated concise news summaries with a distinctive green color theme.

**Requirement ID**: e55aa6da-dcc1-42d2-93c7-04ee6e2d9b0a

## Live Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001/api

## Key Features

### ✅ Implemented
1. **Clean News Feed Interface**
   - Scrollable card-based layout
   - Green color theme throughout (borders, badges, buttons)
   - Responsive design for mobile and desktop

2. **AI-Powered News Summaries**
   - Integration with SearchAgent for web search
   - Concise summaries (60-word format)
   - Source attribution with read more links

3. **User Experience**
   - Category badges (Technology, Business, Science)
   - Relative timestamps (e.g., "2h ago")
   - Loading states with skeleton components
   - Empty state handling
   - Refresh functionality

4. **Backend API**
   - `/api/news` - Get all news summaries
   - `/api/news/fetch` - Fetch new news with AI summarization
   - `/api/news/seed` - Load sample news for testing

## Technical Stack

### Backend
- **Framework**: FastAPI
- **Database**: MongoDB (news_summaries collection)
- **AI**: SearchAgent with LiteLLM integration
- **Language**: Python 3.11

### Frontend
- **Framework**: React 19
- **UI Components**: shadcn/ui
- **Styling**: Tailwind CSS (green theme)
- **Icons**: lucide-react
- **Routing**: React Router v7

## Database Schema

```javascript
news_summaries: {
  id: uuid,
  title: string,
  summary: string,
  source_url: string,
  source_name: string,
  category: string,
  timestamp: datetime,
  created_at: datetime
}
```

## How to Use

### 1. View News Feed
Simply navigate to http://localhost:3000 to see the news feed

### 2. Load Sample News
If the feed is empty, click "Load Sample News" button to populate with 5 sample articles

### 3. Refresh News
Click the "Refresh" button in the header to reload the news feed

### 4. Read Full Articles
Click "Read More" on any news card to visit the original source

## API Endpoints

### Get News
```bash
curl http://localhost:8001/api/news
```

### Seed Sample News
```bash
curl -X POST http://localhost:8001/api/news/seed
```

### Fetch AI-Generated News
```bash
curl -X POST http://localhost:8001/api/news/fetch \
  -H "Content-Type: application/json" \
  -d '{"topics": ["technology", "business"], "count": 5}'
```

## Design Highlights

### Color Palette
- **Primary Green**: #10b981 (green-500)
- **Background**: Gradient from green-50 to white
- **Accent**: Green-600 for header/footer
- **Text**: Gray-900 for headings, Gray-700 for body

### Components
- **NewsCard**: Individual news item with green left border
- **NewsFeed**: Main page with sticky header and scrollable content
- **UI Elements**: shadcn/ui components with green theme customization

## Success Metrics
- Clean, modern interface ✅
- Green color theme consistently applied ✅
- Fast loading with skeleton states ✅
- Responsive design ✅
- AI-powered content sourcing ✅
- Easy navigation and readability ✅

## Future Enhancements
- Real-time news fetching with scheduled jobs
- Category filtering
- Search functionality
- Dark mode support
- Share functionality
- Bookmark/save articles
- Pagination for better performance

## Development Commands

### Backend
```bash
cd backend
uvicorn server:app --reload
```

### Frontend
```bash
cd frontend
bun start
```

### Build Frontend
```bash
cd frontend
bun run build
```

## Files Created
- `backend/server.py` - Updated with news endpoints
- `frontend/src/components/NewsCard.jsx` - News card component
- `frontend/src/pages/NewsFeed.jsx` - Main news feed page
- `frontend/src/App.js` - Updated routing
- `plan/inshorts-clone-plan.md` - Implementation plan
- `backend/test_news_api.py` - API test script

## Acceptance Criteria Status
✅ User can see a feed of news summaries
✅ Each summary is concise (60-word format)
✅ Green color theme throughout the application
✅ Click to read full article on source website
✅ Responsive design works on mobile and desktop
✅ News content sourced via search and AI summarization

---

**Built with ❤️ on Fenado**
