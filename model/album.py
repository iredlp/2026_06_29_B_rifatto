from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Set

@dataclass
class Album:
    AlbumId: int
    Title: str
    ArtistId: int

    list_brani: list = field(default_factory=list)
    list_generi: list = field(default_factory=list)

    # popolarita: int=0

    def __hash__(self):
        return hash(self.AlbumId)

    def __eq__(self, other):
        if isinstance(other, Album):
            return self.AlbumId == other.AlbumId
        return False

    def __repr__(self):
        return (f"{self.Title}  ({self.AlbumId if self.AlbumId is not None else 'N/D'})")