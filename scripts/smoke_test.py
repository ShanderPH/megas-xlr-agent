"""Run Megas-o against the BR Masters lineup brief and print the Backlog JSON."""

import asyncio
import json
from dotenv import load_dotenv

from agents import megas_o
from schemas.brief import FeatureRequest, ProjectBrief

load_dotenv()

BRIEF = ProjectBrief(
    name="BR Masters",
    slug="br-masters",
    domain=(
        "Brazilian football predictions — gamified betting-style picks "
        "for the Brasileirão season"
    ),
    tech_stack=[
        "Next.js 16",
        "TypeScript 5.6",
        "Supabase (Postgres + Auth + Storage)",
        "HeroUI v3",
        "Tailwind CSS v4",
        "Framer Motion",
        "Zod",
        "Mercado Pago SDK",
        "SofaScore API via RapidAPI",
        "HMAC-SHA256 webhook verification",
    ],
    constraints=[
        "Multi-tenant; each user owns their picks",
        "pt-BR primary locale; EN secondary",
        "Must respect Brazilian holidays and timezone (America/Sao_Paulo)",
        "All monetary values in BRL, rounded to cents",
    ],
    target_users=(
        "Brazilian football fans aged 18-45 who want to gamify "
        "their predictions for weekly Brasileirão rounds"
    ),
)

FEATURE = FeatureRequest(
    title="Escalar o time da rodada",
    description=(
        "User selects 11 players (1 GK + 10 outfield in a valid 4-3-3, 4-4-2, "
        "or 3-5-2 tactical formation) for a given round of the Brasileirão. "
        "Players must come from teams playing that round. SofaScore API feeds "
        "fresh lineups, injuries, and suspensions. Users submit before kickoff; "
        "once the round begins, the lineup locks. Scoring is based on real-player "
        "performance during the round — goals, assists, cards, minutes played."
    ),
    business_goal=(
        "Increase weekly active user engagement and session depth "
        "during Brasileirão rounds"
    ),
    success_metric=(
        "At least 60% of active users submit a lineup for each round; "
        "average time-to-submit under 8 minutes"
    ),
)


async def main() -> None:
    prompt = (
        "ProjectBrief:\n"
        + BRIEF.model_dump_json(indent=2)
        + "\n\nFeatureRequest:\n"
        + FEATURE.model_dump_json(indent=2)
    )
    result = await megas_o.arun(prompt)
    backlog = result.content
    print(json.dumps(backlog.model_dump(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
