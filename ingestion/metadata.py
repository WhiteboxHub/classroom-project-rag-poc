from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import uuid

@dataclass
class DocumentMetadata:
    source: str
    page: int
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "page": self.page,
            "id": self.id,
            **self.extra
        }
