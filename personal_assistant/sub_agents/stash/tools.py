# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tools for the Stash agent to interact with the database."""

import uuid
import sqlalchemy
from google.adk.tools import ToolContext
from personal_assistant import database

def stash_url(user_id: str, url: str, summary: str, tags: str, tool_context: ToolContext) -> dict:
    """
    Adds a new URL to the user's stash.

    Args:
        user_id: The ID of the user.
        url: The URL to stash.
        summary: A summary of the URL's content.
        tags: Comma-separated tags for the URL.
        tool_context: The tool context.

    Returns:
        A dictionary with the status of the operation.
    """
    engine = database.connect_with_connector()
    url_id = str(uuid.uuid4())

    with engine.connect() as conn:
        conn.execute(
            database.stashed_urls.insert().values(
                url_id=url_id,
                user_id=user_id,
                url=url,
                summary=summary,
                tags=tags,
            )
        )
        conn.commit()

    return {"status": "success", "url_id": url_id}


def get_stashed_urls(user_id: str, tool_context: ToolContext) -> dict:
    """
    Retrieves the stashed URLs for a user.

    Args:
        user_id: The ID of the user.
        tool_context: The tool context.

    Returns:
        A dictionary with the stashed URLs.
    """
    engine = database.connect_with_connector()

    with engine.connect() as conn:
        select_urls = sqlalchemy.select(database.stashed_urls).where(
            database.stashed_urls.c.user_id == user_id
        )
        urls = conn.execute(select_urls).fetchall()
        
        result = [
            {
                "url": u.url,
                "summary": u.summary,
                "tags": u.tags,
            }
            for u in urls
        ]

    return {"stashed_urls": result}

def ask_for_confirmation(question: str, tool_context: ToolContext) -> dict:
    """
    Asks the user for confirmation before performing an action.

    Args:
        question: The question to ask the user.
        tool_context: The tool context.

    Returns:
        A dictionary with the user's response.
    """
    return {"question": question}

def add_user(user_name: str, tool_context: ToolContext) -> dict:
    """
    Adds a new user.

    Args:
        user_name: The name of the user.
        tool_context: The tool context.

    Returns:
        A dictionary with the status of the operation.
    """
    engine = database.connect_with_connector()
    user_id = str(uuid.uuid4())

    with engine.connect() as conn:
        conn.execute(
            database.users.insert().values(user_id=user_id, user_name=user_name)
        )
        conn.commit()

    return {"status": "success", "user_id": user_id}

def get_user_by_name(user_name: str, tool_context: ToolContext) -> dict:
    """
    Retrieves a user's ID by their name.

    Args:
        user_name: The name of the user.
        tool_context: The tool context.

    Returns:
        A dictionary containing the user's ID if found, otherwise an empty dictionary.
    """
    engine = database.connect_with_connector()
    with engine.connect() as conn:
        select_user = sqlalchemy.select(database.users).where(
            database.users.c.user_name == user_name
        )
        user = conn.execute(select_user).fetchone()
    if user:
        return {"user_id": user.user_id}
    return {}


def update_stashed_url(
    url_id: str,
    new_url: str,
    new_summary: str,
    new_tags: str,
    tool_context: ToolContext,
) -> dict:
    """
    Updates a stashed URL.

    Args:
        url_id: The ID of the URL to update.
        new_url: The new URL.
        new_summary: The new summary.
        new_tags: The new tags.
        tool_context: The tool context.

    Returns:
        A dictionary with the status of the operation.
    """
    engine = database.connect_with_connector()
    values = {}
    if new_url:
        values["url"] = new_url
    if new_summary:
        values["summary"] = new_summary
    if new_tags:
        values["tags"] = new_tags

    with engine.connect() as conn:
        update_stmt = (
            sqlalchemy.update(database.stashed_urls)
            .where(database.stashed_urls.c.url_id == url_id)
            .values(**values)
        )
        conn.execute(update_stmt)
        conn.commit()

    return {"status": "success"}


def delete_stashed_url(url_id: str, tool_context: ToolContext) -> dict:
    """
    Deletes a stashed URL.

    Args:
        url_id: The ID of the URL to delete.
        tool_context: The tool context.

    Returns:
        A dictionary with the status of the operation.
    """
    engine = database.connect_with_connector()

    with engine.connect() as conn:
        delete_stmt = sqlalchemy.delete(database.stashed_urls).where(
            database.stashed_urls.c.url_id == url_id
        )
        conn.execute(delete_stmt)
        conn.commit()

    return {"status": "success"}


def get_stashed_url_by_url(user_id: str, url: str, tool_context: ToolContext) -> dict:
    """
    Retrieves a stashed URL by its URL for a specific user.

    Args:
        user_id: The ID of the user.
        url: The URL to retrieve.
        tool_context: The tool context.

    Returns:
        A dictionary containing the URL's ID if found, otherwise an empty dictionary.
    """
    engine = database.connect_with_connector()
    with engine.connect() as conn:
        select_url = sqlalchemy.select(database.stashed_urls).where(
            database.stashed_urls.c.user_id == user_id,
            database.stashed_urls.c.url == url,
        )
        url_obj = conn.execute(select_url).fetchone()
    if url_obj:
        return {"url_id": url_obj.url_id}
    return {}



