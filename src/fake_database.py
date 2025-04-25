from typing import Dict, Any, Optional

class Database:
    def __init__(self):
        self._storage: Dict[str, Any] = {}

    async def connect(self) -> None:
        """Simulate database connection"""
        pass

    async def disconnect(self) -> None:
        """Simulate database disconnection"""
        pass

    async def get(self, key: str) -> Optional[Any]:
        """Retrieve a value from the database"""
        return self._storage.get(key)

    async def set(self, key: str, value: Any) -> None:
        """Store a value in the database"""
        self._storage[key] = value

    async def delete(self, key: str) -> None:
        """Remove a value from the database"""
        self._storage.pop(key, None)

    async def clear(self) -> None:
        """Clear all values from the database"""
        self._storage.clear()

    async def keys(self) -> list[str]:
        """Get all keys in the database"""
        return list(self._storage.keys())