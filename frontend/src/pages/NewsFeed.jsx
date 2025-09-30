import React, { useState, useEffect } from 'react';
import axios from 'axios';
import NewsCard from '../components/NewsCard';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { Badge } from '@/components/ui/badge';
import { RefreshCw, AlertCircle, Newspaper } from 'lucide-react';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8001';
const API = `${API_BASE}/api`;

const CATEGORIES = [
  { id: 'all', label: 'All', icon: '📰' },
  { id: 'technology', label: 'Technology', icon: '💻' },
  { id: 'business', label: 'Business', icon: '💼' },
  { id: 'science', label: 'Science', icon: '🔬' },
  { id: 'health', label: 'Health', icon: '🏥' },
  { id: 'sports', label: 'Sports', icon: '⚽' },
  { id: 'entertainment', label: 'Entertainment', icon: '🎬' },
  { id: 'world', label: 'World', icon: '🌍' },
  { id: 'general', label: 'General', icon: '📄' },
];

const NewsFeed = () => {
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);
  const [selectedCategory, setSelectedCategory] = useState('all');

  const fetchNews = async (isRefresh = false, category = selectedCategory) => {
    try {
      if (isRefresh) setRefreshing(true);
      else setLoading(true);

      setError(null);
      const categoryParam = category !== 'all' ? `&category=${category}` : '';
      const response = await axios.get(`${API}/news?limit=50${categoryParam}`);

      if (response.data.success) {
        setNews(response.data.news_items);
      } else {
        setError('Failed to load news');
      }
    } catch (err) {
      console.error('Error fetching news:', err);
      setError('Unable to fetch news. Please try again later.');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const handleCategoryChange = (categoryId) => {
    setSelectedCategory(categoryId);
    setLoading(true);
    fetchNews(false, categoryId);
  };

  const seedNews = async () => {
    try {
      setRefreshing(true);
      await axios.post(`${API}/news/seed`);
      await fetchNews();
    } catch (err) {
      console.error('Error seeding news:', err);
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchNews();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-green-50 to-white">
        <div className="max-w-2xl mx-auto px-4 py-8">
          <div className="mb-8">
            <Skeleton className="h-12 w-48 mb-4" />
            <Skeleton className="h-6 w-full mb-2" />
          </div>
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="mb-4">
              <Skeleton className="h-48 w-full" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-green-50 to-white">
      {/* Header */}
      <header className="bg-green-600 shadow-md sticky top-0 z-10">
        <div className="max-w-2xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center">
            <Newspaper className="w-8 h-8 text-white mr-3" />
            <h1 className="text-2xl font-bold text-white">NewsShorts</h1>
          </div>
          <Button
            onClick={() => fetchNews(true)}
            disabled={refreshing}
            variant="secondary"
            size="sm"
            className="bg-white text-green-600 hover:bg-green-50"
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
            Refresh
          </Button>
        </div>
      </header>

      {/* Category Filter */}
      <div className="bg-white border-b border-gray-200 sticky top-[72px] z-10 shadow-sm">
        <div className="max-w-2xl mx-auto px-4 py-4">
          <div className="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-hide">
            {CATEGORIES.map((category) => (
              <Badge
                key={category.id}
                onClick={() => handleCategoryChange(category.id)}
                className={`cursor-pointer whitespace-nowrap transition-all duration-200 px-4 py-2 text-sm font-medium ${
                  selectedCategory === category.id
                    ? 'bg-green-600 text-white hover:bg-green-700'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                <span className="mr-2">{category.icon}</span>
                {category.label}
              </Badge>
            ))}
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-2xl mx-auto px-4 py-8">
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center">
            <AlertCircle className="w-5 h-5 text-red-600 mr-3" />
            <span className="text-red-800">{error}</span>
          </div>
        )}

        {news.length === 0 && !error && (
          <div className="text-center py-12">
            <Newspaper className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h2 className="text-xl font-semibold text-gray-700 mb-2">No News Available</h2>
            <p className="text-gray-600 mb-4">Get started by loading some sample news</p>
            <Button
              onClick={seedNews}
              disabled={refreshing}
              className="bg-green-600 hover:bg-green-700 text-white"
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
              Load Sample News
            </Button>
          </div>
        )}

        {news.length > 0 && (
          <div className="space-y-0">
            {news.map((item) => (
              <NewsCard key={item.id} news={item} />
            ))}
          </div>
        )}

        {news.length > 0 && (
          <div className="text-center py-8">
            <p className="text-gray-500">You've reached the end</p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-green-600 mt-12 py-6">
        <div className="max-w-2xl mx-auto px-4 text-center text-white">
          <p className="text-sm">NewsShorts - Your concise news companion</p>
          <p className="text-xs mt-2 opacity-80">Built with ❤️ on Fenado</p>
        </div>
      </footer>
    </div>
  );
};

export default NewsFeed;
