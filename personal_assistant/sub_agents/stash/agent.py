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

"""Stash agent for storing information."""

from google.adk import Agent
from google.adk.tools.url_context_tool import UrlContextTool
from . import tools
from . import prompt

MODEL = "gemini-2.5-pro"

stash_agent = Agent(
    model=MODEL,
    name="Stash",
    instruction=prompt.STASH_PROMPT,
    tools=[
        tools.stash_url,
        tools.get_stashed_urls,
        tools.get_user_by_name,
        tools.add_user,
        tools.ask_for_confirmation,
        tools.update_stashed_url,
        tools.delete_stashed_url,
        tools.get_stashed_url_by_url,
    ],
)
