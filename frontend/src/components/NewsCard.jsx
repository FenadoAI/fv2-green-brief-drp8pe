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

  return (
    <Card className="mb-4 overflow-hidden transition-all duration-300 hover:shadow-lg border-l-4 border-l-green-500 bg-white">
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
