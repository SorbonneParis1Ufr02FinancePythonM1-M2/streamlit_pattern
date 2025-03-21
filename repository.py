import logging
import streamlit as st
from dataclasses import dataclass

import pandas as pd

from constants import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


@dataclass(init=True)
class ColumnDefinition:
    name: str
    col_name: str
    input: str


@dataclass(init=True)
class Data:
    name: str
    value: float
    item: str


@dataclass(init=True)
class OtherData:
    name: str
    factor: float


@st.cache_data
def _get_data(values, column_infos):
    """Loads the dataset using column names from the config."""
    logger.warning("get data uncached")
    results = dict()
    api_data = [
        {"id": "a", "value": 1, "item": "stuff 1"},
        {"id": "b", "value": 2, "item": "stuff 2"},
        {"id": "c", "value": 3, "item": "stuff 1"},
    ]
    for value in api_data:
        if value[column_infos["name"].input] in values:
            d = Data(
                name=value[column_infos["name"].input],
                value=value[column_infos["raw_value"].input],
                item=value[column_infos["item"].input],
            )
            results[d.name] = d
    logger.info(f"len data={len(results)}")
    return results


class Repository:
    """Handles data retrieval and configuration."""

    def __init__(self, config):
        self.config = config
        self.column_infos = dict()
        self._load_dataset_infos()
        self.names = list()
        self.data = dict()
        self.other_data = dict()
        self.load_names()

    def _load_dataset_infos(self):
        for key, value in self.config["column_infos"].items():
            dd = ColumnDefinition(
                name=key,
                col_name=value["col_name"],
                input=value["input"],
            )
            self.column_infos[key] = dd
        logger.info(f"len data_definitions={len(self.column_infos)}")

    def load_names(self):
        self.names = ["a", "b", "c"]

    def load_data(self, values):
        """Loads the dataset using column names from the config."""
        logger.warning("Getting data")
        self.data = _get_data(values, column_infos=self.column_infos)
        logger.info(f"len data={len(self.data)}")

    def load_other_data(self, values):
        """Loads the dataset using column names from the config."""
        api_data = [
            {"id": "a", "factor": 10},
            {"id": "b", "factor": 20},
            {"id": "c", "factor": 30},
        ]
        for value in api_data:
            if value[self.column_infos["name"].input] in values:
                d = OtherData(
                    name=value[self.column_infos["name"].input],
                    factor=value[self.column_infos["factor"].input],
                )
                self.other_data[d.name] = d
        logger.info(f"len other data={len(self.other_data)}")

    def get_data_as_dataframe(self) -> pd.DataFrame:
        """Returns the dataset as a pandas DataFrame."""
        headers = (
            self.column_infos["name"].col_name,
            self.column_infos["value"].col_name,
            self.column_infos["item"].col_name,
        )
        data = list()
        for v in self.data.values():
            data.append([v.name, v.value, v.item])
        return pd.DataFrame(data=data, columns=headers)

    def get_other_data_as_dataframe(self):
        """Returns the other dataset as a pandas DataFrame."""
        headers = (
            self.column_infos["name"].col_name,
            self.column_infos["factor"].col_name,
        )
        data = list()
        for v in self.other_data.values():
            data.append([v.name, v.factor])
        return pd.DataFrame(data=data, columns=headers)
