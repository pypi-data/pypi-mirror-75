# g4hunter_caller.py
# !/usr/bin/env python3


import json
import requests
import tenacity
import pandas as pd
from typing import Generator, List, Optional

from DNA_analyser_IBP.callers.user_caller import User
from DNA_analyser_IBP.callers.analyse_caller import AnalyseFactory, AnalyseModel
from DNA_analyser_IBP.utils import (
    Logger,
    generate_dataframe,
    validate_key_response,
    validate_text_response,
)


class G4HunterAnalyse(AnalyseModel):
    """G4Hunter analyse object finds guanine quadruplex in DNA/RNA sequence"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.result_count = kwargs.pop("resultCount")
        self.window_size = kwargs.pop("windowSize")
        self.threshold = kwargs.pop("threshold")
        self.frequency = kwargs.pop("frequency")

    def __str__(self):
        return f"G4Hunter {self.id} {self.title}"

    def __repr__(self):
        return f"<G4Hunter {self.id} {self.title}>"


class G4HunterAnalyseFactory(AnalyseFactory):
    """G4Hunter factory used for generating analyse for given sequence"""

    @tenacity.retry(wait=tenacity.wait_fixed(1), stop=tenacity.stop_after_attempt(3))
    def create_analyse(
        self,
        user: User,
        id: str,
        tags: Optional[List[str]],
        threshold: float,
        window_size: int,
    ) -> G4HunterAnalyse:
        """
        G4hunter analyse factory

        Args:
            user (User): user for auth
            id (str): sequence id
            tags (Optional[List[str]]): analyse tags
            threshold (float): threshold for g4hunter algorithm recommended 1.2
            window_size (int): window size for g4hunter algorithm recommended 25

        Returns:
            G4HunterAnalyse: G4Hunter object
        """
        # check range of parameters
        if 0 <= threshold <= 4 and 10 <= window_size <= 100:
            header: dict = {
                "Content-type": "application/json",
                "Accept": "application/json",
                "Authorization": user.jwt,
            }
            data: dict = json.dumps(
                {
                    "sequence": id,
                    "tags": tags or list(),
                    "threshold": threshold,
                    "windowSize": window_size,
                }
            )

            response: object = requests.post(
                f"{user.server}/analyse/g4hunter", headers=header, data=data
            )
            data: dict = validate_key_response(
                response=response, status_code=201, payload_key="payload"
            )
            return G4HunterAnalyse(**data)
        else:
            Logger.error("Value window size or threshold out of range!")


class G4HunterMethods:
    """G4HunterMethods holds all g4hunter server methods"""

    @staticmethod
    @tenacity.retry(wait=tenacity.wait_fixed(1), stop=tenacity.stop_after_attempt(3))
    def delete(user: User, id: str) -> bool:
        """
        Delete analyse by id

        Args:
            user (User): user for auth
            id (str): g4hunter analyse id
        Returns:
            bool: True if delete is successfull False if not
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "*/*",
            "Authorization": user.jwt,
        }

        response: object = requests.delete(
            f"{user.server}/analyse/g4hunter/{id}", headers=header
        )
        if response.status_code == 204:
            return True
        return False

    @staticmethod
    def load_by_id(user: User, id: str) -> G4HunterAnalyse:
        """
        Load one g4hunter analyse by id

        Args:
            user (User): user for auth
            id (str): g4hunter analyse id

        Returns:
            G4HunterAnalyse: G4Hunter object
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": user.jwt,
        }

        response: object = requests.get(
            f"{user.server}/analyse/g4hunter/{id}", headers=header)
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="payload"
        )
        return G4HunterAnalyse(**data)

    @staticmethod
    def load_all(
        user: User, tags: List[Optional[str]]
    ) -> Generator[G4HunterAnalyse, None, None]:
        """
        Load all g4hunter analyses

        Args:
            user (User): user for auth
            tags (List[Optional[str]]): filter tag for loading

        Returns:
            Generator[G4HunterAnalyse, None, None], Exception: G4Hunter object generator
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": user.jwt,
        }
        params: dict = {
            "order": "ASC",
            "requestForAll": "true",
            "pageSize": "ALL",
            "tags": tags or list(),
        }

        response: object = requests.get(
            f"{user.server}/analyse/g4hunter", headers=header, params=params
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="items"
        )
        for record in data:
            yield G4HunterAnalyse(**record)

    @staticmethod
    def load_result(user: User, id: str) -> pd.DataFrame:
        """
        Load G4Hunter analyse result

        Args:
            user (User): user for auth
            id (str): g4hunter analyse id

        Returns:
            pd.DataFrame: DataFrame with G4Hunter results
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": user.jwt,
        }
        params: dict = {"order": "ASC",
                        "requestForAll": "true", "pageSize": "ALL"}

        response: object = requests.get(
            f"{user.server}/analyse/g4hunter/{id}/quadruplex",
            headers=header,
            params=params,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="items"
        )
        return generate_dataframe(response=data)

    @staticmethod
    @tenacity.retry(wait=tenacity.wait_fixed(1), stop=tenacity.stop_after_attempt(3))
    def export_csv(user: User, id: str, aggregate: bool = True) -> str:
        """
        Export G4Hunter results as csv output

        Args:
            user (User): user for atuh
            id (str): g4hunter analyse id
            aggregate (bool): True if aggregate results else False

        Returns:
            str: csv file in string
        """
        header: dict = {"Accept": "text/plain", "Authorization": user.jwt}
        params: dict = {"aggregate": "true" if aggregate else "false"}

        response: object = requests.get(
            f"{user.server}/analyse/g4hunter/{id}/quadruplex.csv",
            headers=header,
            params=params,
        )
        return validate_text_response(response=response, status_code=200)

    @staticmethod
    def load_heatmap(user: User, id: str, segments: int) -> pd.DataFrame:
        """
        Download heatmap data for G4Hunter analyse

        Args:
            user (User): user for auth
            id (str): g4hunter analyse id
            segments (int): number of heatmap segments

        Returns:
            pd.DataFrame: dataFrame with heatmap data
        """
        header: dict = {
            "Content-type": "application/json",
            "Accept": "application/json",
            "Authorization": user.jwt,
        }
        params: dict = {"segments": segments}

        response = requests.get(
            f"{user.server}/analyse/g4hunter/{id}/heatmap",
            headers=header,
            params=params,
        )
        data: dict = validate_key_response(
            response=response, status_code=200, payload_key="data"
        )
        heatmap: pd.DataFrame = pd.DataFrame(data=data)
        heatmap.rename(
            columns={"count": "PQS_count", "coverage": "PQS_coverage"}, inplace=True
        )
        return heatmap
