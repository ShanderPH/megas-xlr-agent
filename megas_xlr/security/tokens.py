from datetime import UTC, datetime, timedelta
from typing import Any

import jwt
from pydantic import BaseModel


class TokenClaims(BaseModel):
    sub: str
    iss: str
    aud: str
    scopes: tuple[str, ...]
    exp: int
    iat: int


def issue_token(
    subject: str,
    scopes: tuple[str, ...],
    *,
    issuer: str,
    audience: str,
    signing_key: str,
    ttl_seconds: int,
) -> str:
    now = datetime.now(UTC)
    claims = TokenClaims(
        sub=subject,
        iss=issuer,
        aud=audience,
        scopes=scopes,
        iat=int(now.timestamp()),
        exp=int((now + timedelta(seconds=ttl_seconds)).timestamp()),
    )
    return jwt.encode(claims.model_dump(), signing_key, algorithm="HS256")


def decode_token(token: str, *, issuer: str, audience: str, signing_key: str) -> TokenClaims:
    payload: dict[str, Any] = jwt.decode(
        token, signing_key, algorithms=["HS256"], issuer=issuer, audience=audience
    )
    return TokenClaims.model_validate(payload)
