from models.interests_model import (
    create_interest,
    list_interests,
    update_user_interests,
    get_interest_by_id,
    add_interests,
    remove_interests
)
from models.user_model import get_user_by_id
from typing import List, Dict
import logging
from models.database import Database

def get_all_interests() -> List[Dict]:
    return list_interests()

def add_new_interest(tag: str) -> Dict:
    return create_interest(validate_tags([tag])[0])

def add_multiple_interests(tags: List[str]) -> List[Dict]:
    return add_interests(validate_tags(tags))

def remove_interests_by_ids(interest_ids: List[int]) -> str:
    if not interest_ids:
        raise ValueError("No interest IDs provided.")
    return remove_interests(interest_ids)

def assign_interests_to_user(user_id: int, tags: List[str]) -> List[Dict]:
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found.")

    cleaned_tags = validate_tags(tags)
    interests = add_interests(cleaned_tags)

    query = '''
        INSERT INTO user_interests (user_id, interest_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    '''
    try:
        with Database.get_connection() as connection:
            with connection.cursor() as cursor:
                for interest in interests:
                    cursor.execute(query, (user_id, interest['id']))
                connection.commit()
        return interests
    except Exception as e:
        logging.error(f"Error assigning interests to user {user_id}: {e}")
        raise Exception("Error assigning interests") from e

def get_user_interests(user_id: int) -> List[Dict]:
    user = get_user_by_id(user_id)
    if not user:
        raise ValueError("User not found.")

    query = '''
        SELECT i.id, i.tag
        FROM user_interests ui
        INNER JOIN interests i ON ui.interest_id = i.id
        WHERE ui.user_id = %s
        ORDER BY i.tag ASC
    '''
    return execute_query(query, (user_id,), fetchone=False)

def validate_tags(tags: List[str]) -> List[str]:
    if not tags:
        raise ValueError("Tags cannot be empty.")
    cleaned_tags = [tag.strip() for tag in tags if tag.strip()]
    if not cleaned_tags:
        raise ValueError("No valid tags provided.")
    return cleaned_tags

