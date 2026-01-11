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

# """Tools for the Personal Assistant agent."""

# from google.adk.tools import ToolContext

# def save_user_name(user_name: str, tool_context: ToolContext) -> dict:
#     """
#     Saves the user's name to the session state.

#     Args:
#         user_name: The name of the user.
#         tool_context: The tool context, which contains the session state.

#     Returns:
#         A dictionary with the status of the operation.
#     """
#     if hasattr(tool_context, "session") and tool_context.session:
#         tool_context.session.state['user:user_name'] = user_name
#         return {"status": "success", "message": f"User name '{user_name}' saved in '{tool_context.session.id}'."}
#     return {"status": "error", "message": "Session not found."}

import time
from google.adk.tools import ToolContext
from google.adk.events import Event, EventActions

def save_user_name(user_name: str, tool_context: ToolContext) -> dict:
    """
    Saves the user's name to the session state by returning an EventActions with a state_delta.

    Args:
        user_name: The name of the user.
        tool_context: The tool context.

    Returns:
        A dictionary containing the EventActions to update the state.
    """
    if hasattr(tool_context, "session") and tool_context.session:
        
        tool_context.state["user:user_name"] = user_name

        return {"status": "success", "message": f"User name '{user_name}' saved in '{tool_context.session.id}'."}

        # state_changes = {
        #     'user:user_name': user_name
        # }

        # Create EventActions with the state_delta
        # event_actions = EventActions(state_delta=state_changes)

        # Tools are expected to return a dictionary, which the ADK runner
        # can use to construct an Event. To signal a state update,
        # you can return a dictionary containing the serialized EventActions.
        # While ADK's internal mechanisms handle the event creation,
        # returning the action itself is the key.

        # The ADK framework will typically look for a return value
        # that can be interpreted as the result of the tool's action.
        # To update state, the tool should signal this intention.
        # The exact return format for state updates within a tool's
        # direct return can vary, but the principle is to an action
        # that the runner will process.

        # A more direct way to influence state from a tool is to
        # return the state_delta within a structured response.
        # Let's return a dictionary that includes the desired state changes.

        # return {
        #     "status": "success",
        #     "message": f"User name '{user_name}' set for session '{tool_context.session.id}'.",
        #     "state_delta": state_changes  # Signal the state change
        # }
    return {"status": "error", "message": "Session not found."}

# Example of how this tool would be wrapped and used (conceptual)
# from google.adk.tools import FunctionTool
# save_user_name_tool = FunctionTool(func=save_user_name)

# When the ADK runner executes this tool and receives a dictionary
# containing a 'state_delta' key, it can apply these changes
# to the session state through the SessionService.