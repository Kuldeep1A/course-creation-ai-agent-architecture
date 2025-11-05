I want to alter this codebase to be a full multi-agent architecture, which will consist of ADK agents that will curate research, refine, judge each other, and build the content before sending it back to the frontend. 

The frontend will pass that request to the agent syste, which will be comprised of several ADK agents speaking to each other.

To accomplish this, we want a few things.

1. A sample frontend. The code for this is not so important, it just needs to b e there to illustrate how to connect to an ADK system on the backend.
2. The code for the ADK agent systems. Use the @GEMINI.md file to understand how to work with ADK and A2A. All the agents should be able to communicate with each other to complete the task.
3. The code and deployment instructions for putting the agents on the cloud.
4. The code to integrate the ADK agent system into the frontend.