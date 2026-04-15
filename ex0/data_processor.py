#!usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self):
        self.datas = []

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        

class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        elif isinstance(data, list):
            return all(isinstance(d, (int, float)) for d in data)
        else:
            return False
        
    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise Exception("Improper numeric data\n")
        
        if isinstance(data, (int, float)):
            self.datas.append(str(data))

        else:
            for d in data:
                self.datas.append(str(d))


class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        elif isinstance(data, list):
            return all(isinstance(d, str) for d in data)
        else:
            return False
        
    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise Exception("Improper string data\n")
        
        if isinstance(data, str):
            self.datas.append(data)

        else:
            for d in data:
                self.datas.append(d)


class LogProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(isinstance(key, str) and isinstance(value, str) for key, value in data.items())
        elif isinstance(data, list):
            if all(isinstance(d, dict) for d in data):
                for d in data:
                    if not all(isinstance(key, str) and isinstance(value, str) for key, value in d.items()):
                        return False
            else:
                return False
            return True
        else:
            return False

    def ingest(self, data: dict | list[dict]) -> None:
        