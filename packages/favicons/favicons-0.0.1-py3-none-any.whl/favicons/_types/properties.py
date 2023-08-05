"""Custom data model for favicon properties."""

# Standard Library
import json as _json
from typing import Dict, Iterable, Optional


class FaviconProperties:
    """Data Model for Favicon Properties."""

    def __init__(
        self,
        image_fmt: str,
        dimensions: Iterable[int],
        prefix: str,
        rel: Optional[str] = None,
    ) -> None:
        """Set properties."""

        self.image_fmt = image_fmt
        self.rel = rel
        self.dimensions = dimensions
        self.prefix = prefix

    @property
    def width(self) -> int:
        """Width from dimensions."""
        return self.dimensions[0]

    @property
    def height(self) -> int:
        """Height from dimensions."""
        return self.dimensions[1]

    def __repr__(self):
        """Representation of instance."""
        attr_names = (a for a in self.__dir__() if not a.startswith("_"))
        attrs = (f"{a}={getattr(self, a)}" for a in attr_names)
        return f"{self.__class__.__name__}({', '.join(attrs)})"

    def __str__(self):
        """Represent instance as string."""
        return self._get_filename_parts()

    def dict(self) -> Dict:
        """Represent instance as dict."""
        return {
            "image_format": self.image_fmt,
            "dimensions": list(self.dimensions),
            "prefix": self.prefix,
            "rel": self.rel,
        }

    def json(self) -> str:
        """Represent instance as JSON string."""
        return _json.dumps(self.dict())

    def _get_filename_parts(self) -> Iterable:
        """Don't add dimensions to favicon.ico."""
        if self.image_fmt == "ico":
            parts = (
                self.prefix,
                ".",
                self.image_fmt,
            )
        else:

            parts = (
                self.prefix,
                "-",
                "x".join(str(d) for d in self.dimensions),
                ".",
                self.image_fmt,
            )
        return "".join(parts)
