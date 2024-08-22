from mongomock import MongoClient


def mongomock_client():
    client = MongoClient()
    braks = client.db.braks
    users = client.db.users
    user_data = [
        dict(id=1, first_name="test", last_name="1", username="test1", language_code="ru", is_admin=False),
        dict(id=2, first_name="test", last_name="2", username="test2", language_code="ru", is_admin=False),
        dict(id=3, first_name="test", last_name="3", username="test3", language_code="ru", is_admin=False),
        dict(id=4, first_name="test", last_name="4", username="test4", language_code="ru", is_admin=False),
        dict(id=5, first_name="test", last_name="5", username="test5", language_code="ru", is_admin=False),
        dict(id=6, first_name="test", last_name="6", username="test6", language_code="ru", is_admin=False),
        dict(id=7, first_name="test", last_name="7", username="test7", language_code="ru", is_admin=False),
        dict(id=8, first_name="test", last_name="8", username="test8", language_code="ru", is_admin=False)
    ]
    brak_data = [
        dict(first_user_id=1, second_user_id=2, create_date="2023-07-04T18:57:56.122Z", baby_user_id=3,
             baby_create_date="2023-07-04T18:57:56.122Z", score=0, last_casino_play="2024-08-21T21:46:41.863Z",
             last_grow_kid="2024-08-21T21:46:43.929Z", last_hamster_update="2024-08-22T18:23:32.120Z", tap_count=0,
             chat_id=-1001527296273),
        dict(first_user_id=3, second_user_id=4, create_date="2023-07-04T18:57:56.122Z", baby_user_id=5,
             baby_create_date="2023-07-04T18:57:56.122Z", score=0, last_casino_play="2024-08-21T21:46:41.863Z",
             last_grow_kid="2024-08-21T21:46:43.929Z", last_hamster_update="2024-08-22T18:23:32.120Z", tap_count=0,
             chat_id=-1001527296273),
        dict(first_user_id=5, second_user_id=6, create_date="2023-07-04T18:57:56.122Z", baby_user_id=7,
             baby_create_date="2023-07-04T18:57:56.122Z", score=0, last_casino_play="2024-08-21T21:46:41.863Z",
             last_grow_kid="2024-08-21T21:46:43.929Z", last_hamster_update="2024-08-22T18:23:32.120Z", tap_count=0,
             chat_id=-1001527296273),
        dict(first_user_id=7, second_user_id=8, create_date="2023-07-04T18:57:56.122Z", baby_user_id=5,
             baby_create_date="2023-07-04T18:57:56.122Z", score=0, last_casino_play="2024-08-21T21:46:41.863Z",
             last_grow_kid="2024-08-21T21:46:43.929Z", last_hamster_update="2024-08-22T18:23:32.120Z", tap_count=0,
             chat_id=-1001527296273)
    ]
    for user in user_data:
        user['_id'] = users.insert_one(user).inserted_id
    for brak in brak_data:
        brak['_id'] = braks.insert_one(brak).inserted_id
    return client