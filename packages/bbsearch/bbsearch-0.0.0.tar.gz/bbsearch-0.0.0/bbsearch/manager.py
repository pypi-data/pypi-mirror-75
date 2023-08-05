from typing import Optional, List, Generator

from .client import AuthenticatedClient
from .api.programs import get_programs, get_program
from .models import Program


class BugBountySearch:
    def __init__(
        self, token: str,
    ):
        self.client = AuthenticatedClient(
            base_url="https://api.dev.bugbountysearch.com", token=token,
        )

    def _paginate(self, api_function, **kwargs):
        page = 0
        while page is not None:
            targets = api_function(client=self.client, page=page, **kwargs)
            for target in targets.data:
                yield target
            page = targets.next_page

    def get_program(self, slug: str) -> Program:
        return get_program(client=self.client, slug=slug)

    def get_programs(
        self,
        *,
        name: Optional[str] = "",
        types: Optional[List[str]] = [],
        platforms: Optional[List[str]] = [],
        exclude_platforms: Optional[List[str]] = [],
        rewards: Optional[List[str]] = [],
    ) -> Generator[Program, None, None]:
        for program in self._paginate(
            get_programs,
            name=name,
            types=types,
            platforms=platforms,
            exclude_platforms=exclude_platforms,
            rewards=rewards,
        ):
            yield program
