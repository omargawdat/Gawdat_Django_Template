from dataclasses import dataclass


@dataclass
class TokenData:
    access: str
    refresh: str
