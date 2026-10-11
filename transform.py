REQUIRED_FIELDS = {"userId", "id", "title", "body"}

def transform_posts(posts):
    """Validate and clean extracted post records."""

    valid_posts =[]
    rejected_posts = []
    seen_ids = set()


    for post in posts:
        # 1. Check for required fields.
        if not isinstance(post, dict) or not REQUIRED_FIELDS.issubset(post):
            rejected_posts.append({
                "record": post,
                "reason": "Missing required fields or invalid record format."
            })
            continue

        #2. Check IDs.
        if(
            type(post["id"]) is not int
            or type(post["userId"]) is not int
            or post["id"] <= 0
            or post["userId"] <= 0
        ):
            rejected_posts.append({
                "record": post,
                "reason": "Invalid ID values."
            })
            continue

        # 3. Check text fields.
        if(
            not isinstance(post["title"], str)
            or not post["title"].strip()
            or not isinstance(post["body"], str)
            or not post["body"].strip()
        ):
            rejected_posts.append({
                "record": post,
                "reason": "Title and body must be non-empty strings."
            })
            continue

        # 4. Remove duplicates IDS.
        if post["id"] in seen_ids:
            rejected_posts.append({
                "record": post,
                "reason": "Duplicate ID found."
            })
            continue
        seen_ids.add(post["id"])

        # 5. Standardize the output fields.
        cleaned_post = {
            "post_id": post["id"],
            "user_id": post["userId"],
            "title": post["title"].strip(),
            "body": post["body"].strip()
        }
        valid_posts.append(cleaned_post)

    return valid_posts, rejected_posts