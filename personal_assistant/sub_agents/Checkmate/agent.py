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

"""Checkmate agent for verifying information."""

from google.adk import Agent
from . import tools

from . import prompt

MODEL = "gemini-2.5-pro"

checkmate_agent = Agent(
    model=MODEL,
    name="Checkmate",
    instruction=prompt.CHECKMATE_PROMPT,
    tools=[
        tools.get_user_by_name,
        tools.add_user,
        tools.add_user_and_list,
        tools.add_task_to_list,
        tools.get_todo_list,
        tools.ask_for_confirmation,
        tools.update_user_name,
        tools.update_list_name,
        tools.delete_user,
        tools.delete_list,
        tools.get_list_by_name,
    ],
)
