from dataclasses import dataclass, field

import logging
import pandas as pd

from constants import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)
from repository import Repository


@dataclass(init=True)
class Result:
    name: str
    raw_value: float
    item: str
    factor: float = field(default=0.0, init=False)

    @property
    def value(self) -> float:
        """fake computation"""
        return self.raw_value * self.factor


class Model:
    """Handles data filtering."""

    def __init__(self, repository: Repository):
        self.repo = repository
        self.results = dict()

    def process(self):
        logger.debug(f"Processing len={len(self.repo.data)}")
        for v in self.repo.data.values():
            logger.debug(f"input process ={v.__repr__()}")
            r = Result(v.name, v.value, v.item)
            other = self.repo.other_data.get(v.name)
            if other:
                r.factor = other.factor
            self.results[r.name] = r

    def get_data_as_dataframe(self) -> pd.DataFrame:
        """Returns the dataset as a pandas DataFrame."""
        headers = (
            self.repo.column_infos["name"].col_name,
            self.repo.column_infos["raw_value"].col_name,
            self.repo.column_infos["value"].col_name,
            self.repo.column_infos["item"].col_name,
        )

        data = list()
        for v in self.results.values():
            data.append([v.name, v.raw_value, v.value, v.item])
        results = pd.DataFrame(data, columns=headers)
        logger.info(f"model results shape={results.shape}")
        return results
