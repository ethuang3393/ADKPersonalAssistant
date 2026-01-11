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

"""Tools for the Checkmate agent to interact with the database."""

import uuid
from google.adk.tools import ToolContext
import sqlalchemy
from personal_assistant import database

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

def add_user(user_name: str, tool_context: ToolContext) -> dict:
    """
    Adds a new user to the database.

    Args:
        user_name: The name of the user.
        tool_context: The tool context.

    Returns:
        A dictionary with the status of the operation and the new user's ID.
    """
    engine = database.connect_with_connector()
    user_id = str(uuid.uuid4())

    with engine.connect() as conn:
        conn.execute(
            database.users.insert().values(user_id=user_id, user_name=user_name)
        )
        conn.commit()

    return {"status": "success", "user_id": user_id}

def add_user_and_list(user_name: str, list_name: str, tool_context: ToolContext) -> dict:
    """
    Adds a new user (if not exists) and a new to-do list for that user.

    Args:
        user_name: The name of the user.
        list_name: The name of the to-do list.
        tool_context: The tool context.

    Returns:
        A dictionary with the status of the operation, user_id, and list_id.
    """
    engine = database.connect_with_connector()
    
    user_data = get_user_by_name(user_name, tool_context)
    if user_data:
        user_id = user_data["user_id"]
    else:
        new_user_data = add_user(user_name, tool_context)
        user_id = new_user_data["user_id"]

    list_id = str(uuid.uuid4())

    with engine.connect() as conn:
        conn.execute(
            database.todolists.insert().values(
                list_id=list_id, user_id=user_id, list_name=list_name
            )
        )
        conn.commit()

    return {"status": "success", "user_id": user_id, "list_id": list_id}


def add_task_to_list(list_id: str, task_description: str, tool_context: ToolContext) -> dict:
    """
    Adds a new task to a to-do list.

    Args:
        list_id: The ID of the to-do list.
        task_description: The description of the task.
        tool_context: The tool context.

    Returns:
        A dictionary with the status of the operation.
    """
    engine = database.connect_with_connector()
    task_id = str(uuid.uuid4())

    with engine.connect() as conn:
        conn.execute(
            database.tasks.insert().values(
                task_id=task_id,
                list_id=list_id,
                task_description=task_description,
                is_completed=False,
            )
        )
        conn.commit()

    return {"status": "success", "task_id": task_id}


def get_todo_list(user_id: str, tool_context: ToolContext) -> dict:
    """
    Retrieves the to-do list for a user.

    Args:
        user_id: The ID of the user.
        tool_context: The tool context.

    Returns:
        A dictionary with the to-do list.
    """
    engine = database.connect_with_connector()

    with engine.connect() as conn:
        select_lists = sqlalchemy.select(database.todolists).where(
            database.todolists.c.user_id == user_id
        )
        lists = conn.execute(select_lists).fetchall()
        
        result = []
        for l in lists:
            list_id = l.list_id
            select_tasks = sqlalchemy.select(database.tasks).where(
                database.tasks.c.list_id == list_id
            )
            tasks = conn.execute(select_tasks).fetchall()
            result.append({
                "list_name": l.list_name,
                "tasks": [{"description": t.task_description, "completed": t.is_completed} for t in tasks]
            })

    return {"todo_lists": result}

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


def update_user_name(user_id: str, new_user_name: str, tool_context: ToolContext) -> dict:
    """
    Updates a user's name in the database.

    Args:
        user_id: The ID of the user to update.
        new_user_name: The new name for the user.
        tool_context: The tool context.

    Returns:
        A dictionary with the status of the operation.
    """
    engine = database.connect_with_connector()
    with engine.connect() as conn:
        update_stmt = (
            sqlalchemy.update(database.users)
            .where(database.users.c.user_id == user_id)
            .values(user_name=new_user_name)
        )
        conn.execute(update_stmt)
        conn.commit()
    return {"status": "success"}


def update_list_name(list_id: str, new_list_name: str, tool_context: ToolContext) -> dict:
    """
    Updates a to-do list's name in the database.

    Args:
        list_id: The ID of the list to update.
        new_list_name: The new name for the list.
        tool_context: The tool context.

    Returns:
        A dictionary with the status of the operation.
    """
    engine = database.connect_with_connector()
    with engine.connect() as conn:
        update_stmt = (
            sqlalchemy.update(database.todolists)
            .where(database.todolists.c.list_id == list_id)
            .values(list_name=new_list_name)
        )
        conn.execute(update_stmt)
        conn.commit()
    return {"status": "success"}


def delete_user(user_id: str, tool_context: ToolContext) -> dict:
    """
    Deletes a user and all their associated data from the database.

    Args:
        user_id: The ID of the user to delete.
        tool_context: The tool context.

    Returns:
        A dictionary with the status of the operation.
    """
    engine = database.connect_with_connector()
    with engine.connect() as conn:
        # This will cascade delete tasks and stashed_urls due to ForeignKeys
        delete_stmt = sqlalchemy.delete(database.users).where(
            database.users.c.user_id == user_id
        )
        conn.execute(delete_stmt)
        conn.commit()
    return {"status": "success"}


def delete_list(list_id: str, tool_context: ToolContext) -> dict:
    """
    Deletes a to-do list and all its tasks from the database.

    Args:
        list_id: The ID of the list to delete.
        tool_context: The tool context.

    Returns:
        A dictionary with the status of the operation.
    """
    engine = database.connect_with_connector()
    with engine.connect() as conn:
        # This will cascade delete tasks due to ForeignKey
        delete_stmt = sqlalchemy.delete(database.todolists).where(
            database.todolists.c.list_id == list_id
        )
        conn.execute(delete_stmt)
        conn.commit()
    return {"status": "success"}

def get_list_by_name(user_id: str, list_name: str, tool_context: ToolContext) -> dict:
    """
    Retrieves a to-do list's ID by its name for a specific user.

    Args:
        user_id: The ID of the user.
        list_name: The name of the to-do list.
        tool_context: The tool context.

    Returns:
        A dictionary containing the list's ID if found, otherwise an empty dictionary.
    """
    engine = database.connect_with_connector()
    with engine.connect() as conn:
        select_list = sqlalchemy.select(database.todolists).where(
            database.todolists.c.user_id == user_id,
            database.todolists.c.list_name == list_name
        )
        lst = conn.execute(select_list).fetchone()
    if lst:
        return {"list_id": lst.list_id}
    return {}