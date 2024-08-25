from typing import Protocol, List, Optional
from beanie import Document


class Repository(Protocol):
    async def add(self, entity: Document) -> Document:
        ...

    async def get(self, id: str) -> Optional[Document]:
        ...

    async def update(self, id: str, entity: Document) -> Optional[Document]:
        ...

    async def delete(self, id: str) -> bool:
        ...

    async def list(self) -> List[Document]:
        ...
