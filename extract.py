import requests

API_URL = "https://jsonplaceholder.typicode.com/posts"

def extract_posts():
    """Retrieve posts from the external API."""

    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()

    posts = response.json()

    print(f"Successfully retrieved {len(posts)} posts.")

    return posts

if __name__ == "__main__":
    posts = extract_posts()

    if posts:
        print("\nFirst record:")
        print(posts[0])