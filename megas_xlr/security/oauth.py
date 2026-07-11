import base64
import hashlib
import secrets
from dataclasses import dataclass
from urllib.parse import urlencode


@dataclass(frozen=True)
class PkceRequest:
    state: str
    verifier: str
    authorization_url: str


def create_github_authorization_request(client_id: str, redirect_uri: str) -> PkceRequest:
    state = secrets.token_urlsafe(32)
    verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(verifier.encode()).digest()
    challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    query = urlencode(
        {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": "read:user",
            "state": state,
            "code_challenge": challenge,
            "code_challenge_method": "S256",
        }
    )
    return PkceRequest(state, verifier, f"https://github.com/login/oauth/authorize?{query}")
