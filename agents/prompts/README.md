# Agent prompts

One markdown file per agent. Keep each under 2000 tokens — short, imperative, hierarchical. Never inline prompts in Python code; load them from here at agent construction time.

Convention: filename = `<agent_id_snake_case>.md`. Prompts are created only with an approved agent.
