#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self):
        self.datas: list[str] = []
        self.index: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        try:
            if not self.datas:
                raise Exception("No data available for output")

            extracted: tuple[int, str] = (self.index, self.datas.pop(0))
            self.index += 1
            return extracted

        except Exception as e:
            print(f"{e}")
            return (-1, "None")


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True
        elif isinstance(data, list):
            return all(isinstance(d, (int, float)) for d in data)
        else:
            return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        try:
            if not self.validate(data):
                raise Exception("Improper numeric data\n")

            if isinstance(data, (int, float)):
                self.datas.append(str(data))

            else:
                for d in data:
                    self.datas.append(str(d))

        except Exception as e:
            print(f"Got exception : {e}")


class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        elif isinstance(data, list):
            return all(isinstance(d, str) for d in data)
        else:
            return False

    def ingest(self, data: str | list[str]) -> None:
        try:
            if not self.validate(data):
                raise Exception("Improper string data\n")

            if isinstance(data, str):
                self.datas.append(data)

            else:
                for d in data:
                    self.datas.append(d)

        except Exception as e:
            print(f"Got exception : {e}")


class LogProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(isinstance(key, str) and isinstance(value, str) for key,
                       value in data.items())
        elif isinstance(data, list):
            if all(isinstance(d, dict) for d in data):
                for d in data:
                    if not all(isinstance(key, str) and isinstance(value, str)
                               for key, value in d.items()):
                        return False
                return True
            else:
                return False
        else:
            return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        try:
            if not self.validate(data):
                raise Exception("Improper log data\n")

            if isinstance(data, dict):
                self.datas.append(f"{data['log_level']}: \
{data['log_message']}")

            else:
                for d in data:
                    self.datas.append(f"{d['log_level']}: {d['log_message']}")

        except Exception as e:
            print(f"Got exception : {e}")


if __name__ == "__main__":
    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()

    print(" === Code Nexus --- Data Processor === \n")

    print(" --- Testing numeric processor ...")

    print(f"Trying to validate input '42' : {numeric.validate(42)}")
    print(f"Trying to validate input 'oui' : {numeric.validate('oui')}")

    print("\nTest invalid ingestion of sting 'foo' without prior validation :")
    numeric.ingest("foo")

    print("Processing data : [1, 2, 3, 4, 5]")
    numeric.ingest([1, 2, 3, 4, 5])
    print("Extracting 3 values ...")
    nth_output, value = numeric.output()
    print(f"Numeric value {nth_output}: {value}")
    nth_output, value = numeric.output()
    print(f"Numeric value {nth_output}: {value}")
    nth_output, value = numeric.output()
    print(f"Numeric value {nth_output}: {value}")
    print("\nIngesting one more data")
    numeric.ingest(6)
    print("Extracting one more data")
    nth_output, value = numeric.output()
    print(f"Numeric value {nth_output}: {value}")

    print("\n --- Testing text processor ...")

    print(f"Trying to validate input '42' : {text.validate(42)}")

    print("\nProcessing data : ['Hello', 'Nexus', 'World']")
    text.ingest(["Hello", "Nexus", "World"])
    print("Extracting 2 values ...")
    nth_output, value = text.output()
    print(f"Text value {nth_output}: {value}")
    nth_output, value = text.output()
    print(f"Text value {nth_output}: {value}")

    print("\n --- Testing Log Processor ...")

    print(f"Trying to validate input 'Hello' : {log.validate('Hello')}")

    print("\nProcessing data : [{'log_level': 'NOTICE', 'log_message': \
'Connection to server'}, {'log_level': 'ERROR', 'log_message': \
'Unauthorized access!!'}]")
    log.ingest([{'log_level': 'NOTICE', 'log_message': 'Connection to \
server'}, {'log_level': 'ERROR', 'log_message': 'Unauthorized access!!'}])
    print("Extracting 3 values ...")
    nth_output, value = log.output()
    print(f"Log entry {nth_output}: {value}")
    nth_output, value = log.output()
    print(f"Log entry {nth_output}: {value}")
    nth_output, value = log.output()
    print(f"Log entry {nth_output}: {value}")
