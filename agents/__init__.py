from agents.megas_o import create_megas_o
from db import create_db

megas_o, _model = create_megas_o(create_db())

__all__ = ["megas_o"]
