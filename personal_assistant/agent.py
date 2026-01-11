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

"""Personal Assistant Agent."""

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from . import tools
from .sub_agents.checkmate.agent import checkmate_agent
from .sub_agents.stash.agent import stash_agent

MODEL = "gemini-2.5-pro"


personal_assistant_agent = LlmAgent(
    name="personal_assistant_agent",
    model=MODEL,
    description=(
        "A personal assistant that can help with various tasks."
    ),
    instruction=prompt.PERSONAL_ASSISTANT_PROMPT,
    tools=[
        tools.save_user_name,
        #AgentTool(agent=checkmate_agent),
        #AgentTool(agent=stash_agent),
    ],
    sub_agents=[checkmate_agent, stash_agent]
)

root_agent = personal_assistant_agent
