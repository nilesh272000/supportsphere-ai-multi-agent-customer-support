"""Least-privilege tool registry and runtime authorization."""
from dataclasses import dataclass
from typing import Callable, Any

class ToolAccessDenied(PermissionError):
    pass

@dataclass(frozen=True)
class Tool:
    name: str
    handler: Callable[..., dict]

class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, Tool] = {}
        self._permissions: dict[str, frozenset[str]] = {}

    def register(self, name: str, handler: Callable[..., dict]) -> None:
        self._tools[name] = Tool(name, handler)

    def grant(self, specialist: str, *tool_names: str) -> None:
        unknown = set(tool_names) - self._tools.keys()
        if unknown:
            raise KeyError(f"Unknown tools: {sorted(unknown)}")
        self._permissions[specialist] = frozenset(tool_names)

    def call(self, specialist: str, tool_name: str, **kwargs: Any) -> dict:
        allowed = self._permissions.get(specialist, frozenset())
        if tool_name not in allowed:
            raise ToolAccessDenied(f"{specialist} is not allowed to call {tool_name}")
        tool = self._tools.get(tool_name)
        if tool is None:
            raise KeyError(f"Tool is not registered: {tool_name}")
        return tool.handler(**kwargs)

    def allowed_tools(self, specialist: str) -> frozenset[str]:
        return self._permissions.get(specialist, frozenset())
