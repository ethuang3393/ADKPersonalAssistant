import asyncio
from personal_assistant.agent import root_agent
from google.adk.runners import InMemoryRunner
from google.genai import types

async def main():
    """Runs the agent with a sample query."""
    runner = InMemoryRunner(agent=root_agent, app_name="personal_assistant")
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    content = types.Content(parts=[types.Part(text="hello")])
    response = ""
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        print(event)
        if event.content and event.content.parts and event.content.parts[0].text:
            response = event.content.parts[0].text
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
