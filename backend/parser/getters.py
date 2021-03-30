import json
from pathlib import Path
from typing import Any, Dict, List


class AbstractGetter:

    @classmethod
    def get_events(cls) -> List[Dict[str, Any]]:
        raise NotImplementedError


class SavedFixturesGetter(AbstractGetter):
    """
    Retrieves data from fixtures stored in the files folder
    """

    @classmethod
    def get_events(cls) -> List[Dict[str, Any]]:
        total = []
        for fixture_path in cls.get_fixtures():
            with open(fixture_path) as f:
                data = json.load(f)
                total += data["results"]
        return total

    @classmethod
    def get_fixtures(cls) -> List[str]:
        """
        Get list of fixtures
        """
        files_dir = Path(__file__).resolve().parent / "files"
        return [str(fixture) for fixture in files_dir.iterdir()]
