from azure.cosmos import CosmosClient
import uuid

COSMOS_ENDPOINT = "https://photosapp.documents.azure.com:443/"
COSMOS_KEY = "PVHeA5AWQzZ8bwpOaOQjXpQKghM2Au8aOOONrHuCdntUJwWvPUZRnZqsDFoWcTW54DPpE00Ns6euACDbJMXirA=="

DATABASE_NAME = "photoapp"
PHOTOS_CONTAINER = "photos"
COMMENTS_CONTAINER = "comment"
RATINGS_CONTAINER = "rating"

client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
database = client.create_database_if_not_exists(id=DATABASE_NAME)

photos_container = database.create_container_if_not_exists(
    id=PHOTOS_CONTAINER,
    partition_key={"/path": "/photoId"}
)

comments_container = database.create_container_if_not_exists(
    id=COMMENTS_CONTAINER,
    partition_key={"/path": "/photoId"}
)

ratings_container = database.create_container_if_not_exists(
    id=RATINGS_CONTAINER,
    partition_key={"/path": "/photoId"}
)

def save_photo(data):
    data["photoId"] = str(uuid.uuid4())
    photos_container.create_item(body=data)
    return data


def get_photos():
    items = list(photos_container.read_all_items())
    return items


def get_photo(photo_id):
    query = "SELECT * FROM c WHERE c.photoId=@id"
    items = list(photos_container.query_items(
        query=query,
        parameters=[{"name": "@id", "value": photo_id}],
        enable_cross_partition_query=True
    ))
    return items


def search_photos(keyword):
    query = "SELECT * FROM c WHERE CONTAINS(c.title, @q)"
    items = list(photos_container.query_items(
        query=query,
        parameters=[{"name": "@q", "value": keyword}],
        enable_cross_partition_query=True
    ))
    return items


def add_comment(data):
    data["commentId"] = str(uuid.uuid4())
    comments_container.create_item(body=data)
    return data


def add_rating(data):
    data["ratingId"] = str(uuid.uuid4())
    ratings_container.create_item(body=data)
    return data