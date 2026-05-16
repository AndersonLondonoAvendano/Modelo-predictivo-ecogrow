from typing import Annotated
from pydantic import Field

Password = Annotated[str, Field(..., min_length=8, max_length=128)]