
from transform import transform_posts


def make_post(
    post_id=1,
    user_id=1,
    title="Example title",
    body="Example body",
):
    """Create a sample post for testing."""

    return {
        "userId": user_id,
        "id": post_id,
        "title": title,
        "body": body,
    }


def test_valid_post_is_cleaned():
    post = make_post(
        title="  Example title  ",
        body="  Example body  ",
    )

    valid, rejected = transform_posts([post])

    assert len(valid) == 1
    assert len(rejected) == 0
    assert valid[0]["post_id"] == 1
    assert valid[0]["title"] == "Example title"
    assert valid[0]["body"] == "Example body"


def test_missing_required_field_is_rejected():
    post = make_post()
    del post["body"]

    valid, rejected = transform_posts([post])

    assert len(valid) == 0
    assert len(rejected) == 1


def test_invalid_id_is_rejected():
    post = make_post(post_id=-1)

    valid, rejected = transform_posts([post])

    assert len(valid) == 0
    assert len(rejected) == 1
    assert rejected[0]["reason"] == "Invalid ID values."
    


def test_blank_title_is_rejected():
    post = make_post(title="   ")

    valid, rejected = transform_posts([post])

    assert len(valid) == 0
    assert len(rejected) == 1
    assert rejected[0]["reason"] == (
    "Title and body must be non-empty strings."
)
    


def test_duplicate_post_id_is_rejected():
    first_post = make_post(
        post_id=1,
        title="First post",
    )

    second_post = make_post(
        post_id=1,
        title="Duplicate post",
    )

    valid, rejected = transform_posts(
        [first_post, second_post]
    )

    assert len(valid) == 1
    assert len(rejected) == 1
    assert valid[0]["title"] == "First post"
    assert rejected[0]["reason"] == "Duplicate ID found."


def test_empty_input_returns_empty_results():
    valid, rejected = transform_posts([])

    assert valid == []
    assert rejected == []