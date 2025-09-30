import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ExternalLink, Clock } from 'lucide-react';

const NewsCard = ({ news }) => {
  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));

    if (diffInHours < 1) return 'Just now';
    if (diffInHours < 24) return `${diffInHours}h ago`;
    return date.toLocaleDateString();
  };

  // Get category-based image from Unsplash or use the provided image_url
  const getImageUrl = () => {
    if (news.image_url) return news.image_url;

    // Default images based on category from Unsplash
    const categoryImages = {
      technology: 'https://images.unsplash.com/photo-1518770660439-4636190af475?w=800&q=80',
      business: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80',
      sports: 'https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800&q=80',
      entertainment: 'https://images.unsplash.com/photo-1514525253161-7a46d19cd819?w=800&q=80',
      health: 'https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=800&q=80',
      science: 'https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=800&q=80',
      world: 'https://images.unsplash.com/photo-1526778548025-fa2f459cd5c1?w=800&q=80',
      general: 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800&q=80'
    };

    return categoryImages[news.category] || categoryImages.general;
  };

  return (
    <Card className="mb-4 overflow-hidden transition-all duration-300 hover:shadow-lg border-l-4 border-l-green-500 bg-white">
      {/* News Image */}
      <div className="w-full h-48 overflow-hidden bg-gray-100">
        <img
          src={getImageUrl()}
          alt={news.title}
          className="w-full h-full object-cover transition-transform duration-300 hover:scale-105"
          onError={(e) => {
            e.target.src = 'https://images.unsplash.com/photo-1504711434969-e33886168f5c?w=800&q=80';
          }}
        />
      </div>

      <CardContent className="p-6">
        <div className="flex justify-between items-start mb-3">
          <Badge
            variant="secondary"
            className="bg-green-100 text-green-800 hover:bg-green-200"
          >
            {news.category.replace('_', ' ').toUpperCase()}
          </Badge>
          <div className="flex items-center text-gray-500 text-sm">
            <Clock className="w-4 h-4 mr-1" />
            {formatTime(news.timestamp)}
          </div>
        </div>

        <h2 className="text-xl font-bold text-gray-900 mb-3 leading-tight">
          {news.title}
        </h2>

        <p className="text-gray-700 text-base leading-relaxed mb-4">
          {news.summary}
        </p>

        <div className="flex justify-between items-center pt-3 border-t border-gray-200">
          <span className="text-sm text-gray-600 font-medium">
            {news.source_name}
          </span>
          <a
            href={news.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center text-green-600 hover:text-green-700 font-medium text-sm transition-colors"
          >
            Read More
            <ExternalLink className="w-4 h-4 ml-1" />
          </a>
        </div>
      </CardContent>
    </Card>
  );
};

export default NewsCard;
