from pydantic import BaseModel


class Region(BaseModel):
    """Region of a Report."""
    slug: str
