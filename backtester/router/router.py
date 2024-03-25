from typing import Callable, Dict, Optional

from config.models.config import Workflow


class Router:
    def __init__(self, routes: Dict[Optional[Workflow], Callable[[], None]]) -> None:
        self.routes = routes

    def run(self, workflow: Optional[Workflow]) -> None:
        self.routes[workflow]()
