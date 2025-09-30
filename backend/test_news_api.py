"""Test script for news API endpoints."""

import requests
import time

BASE_URL = "http://localhost:8001/api"

def test_fetch_news():
    """Test fetching news summaries."""
    print("\n=== Testing News Fetch API ===")

    payload = {
        "topics": ["technology", "business"],
        "count": 5
    }

    print(f"Fetching news for topics: {payload['topics']}")
    response = requests.post(f"{BASE_URL}/news/fetch", json=payload, timeout=60)

    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    print(f"Message: {data.get('message')}")
    print(f"News Items Count: {len(data.get('news_items', []))}")

    if data.get('news_items'):
        print("\nFirst News Item:")
        item = data['news_items'][0]
        print(f"  Title: {item.get('title')}")
        print(f"  Category: {item.get('category')}")
        print(f"  Summary (first 100 chars): {item.get('summary', '')[:100]}...")

    return data.get('success', False)


def test_get_news():
    """Test getting all news summaries."""
    print("\n=== Testing Get News API ===")

    response = requests.get(f"{BASE_URL}/news?limit=10", timeout=10)

    print(f"Status Code: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    print(f"News Count: {data.get('count')}")

    if data.get('news_items'):
        print(f"\nShowing {len(data['news_items'])} news items:")
        for idx, item in enumerate(data['news_items'][:3], 1):
            print(f"\n{idx}. {item.get('title')}")
            print(f"   Category: {item.get('category')}")
            print(f"   Source: {item.get('source_name')}")
            print(f"   Summary: {item.get('summary', '')[:80]}...")

    return data.get('success', False)


if __name__ == "__main__":
    print("Starting News API Tests...")
    print("=" * 50)

    # Test 1: Fetch news (this will take time as it uses AI)
    fetch_success = test_fetch_news()

    # Wait a bit for data to be stored
    time.sleep(2)

    # Test 2: Get news
    get_success = test_get_news()

    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"  Fetch News: {'✓ PASS' if fetch_success else '✗ FAIL'}")
    print(f"  Get News: {'✓ PASS' if get_success else '✗ FAIL'}")

    if fetch_success and get_success:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed")
