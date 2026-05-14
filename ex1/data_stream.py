#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self, name: str):
        self.datas: list[str] = []
        self.index: int = 0
        self.name: str = name
        self.ingests_count: int = 0

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
                self.ingests_count += 1

            else:
                for d in data:
                    self.datas.append(str(d))
                    self.ingests_count += 1

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
                self.ingests_count += 1

            else:
                for d in data:
                    self.datas.append(d)
                    self.ingests_count += 1

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
                self.ingests_count += 1

            else:
                for d in data:
                    self.datas.append(f"{d['log_level']}: {d['log_message']}")
                    self.ingests_count += 1

        except Exception as e:
            print(f"Got exception : {e}")


class DataStream:
    def __init__(self):
        self.data_processors: list[DataProcessor] = []
        print("Initialize Data Stream ...")

    def register_processor(self, proc: DataProcessor) -> None:
        self.data_processors.append(proc)
        print(f"Registering {proc.name} Processor")

    def process_stream(self, stream: list[Any]) -> None:
        validated: bool

        if len(self.data_processors) == 0:
            print("Careful, you want to process stream but you dont't \
have any data processor registered !\n")

        else:
            for data in stream:
                validated = False

                for data_processor in self.data_processors:
                    if data_processor.validate(data) is True:
                        data_processor.ingest(data)
                        validated = True
                        break

                if validated is False:
                    print(f"DataStream error - Can't process element \
in stream : {data}")

    def print_processors_stats(self) -> None:
        print("\n == DataStream Statistics == ")
        if len(self.data_processors) == 0:
            print("No processor found, no data.\n")

        else:
            for data_processor in self.data_processors:
                print(f"{data_processor.name} Processor: total \
{data_processor.ingests_count} items processed, \
remaining {len(data_processor.datas)} on processor")
            print("")


if __name__ == "__main__":
    numeric = NumericProcessor("Numeric")
    text = TextProcessor("Text")
    log = LogProcessor("Log")

    print(" === Code Nexus - Data Stream === \n")

    data_stream = DataStream()

    data_stream.print_processors_stats()

    data_stream.register_processor(numeric)

    print("\nSend first batch of data on stream : ['Hello world', \
[3.14, -1, 2.71], [{'log_level': 'WARNING', 'log_message': 'Telnet \
access! Use ssh instead'}, {'log_level': 'INFO', 'log_message': 'User wil \
is connected'}], 42, ['Hi', 'five']]")
    data_stream.process_stream(['Hello world', [3.14, -1, 2.71],
                                [{'log_level': 'WARNING', 'log_message':
                                    'Telnet access! Use ssh instead'},
                                {'log_level': 'INFO', 'log_message': 'User'
                                    'wil is connected'}], 42, ['Hi', 'five']])

    data_stream.print_processors_stats()

    data_stream.register_processor(text)
    data_stream.register_processor(log)

    print("\nSend the same batch again.")
    data_stream.process_stream(['Hello world',
                                [3.14, -1, 2.71], [{'log_level': 'WARNING',
                                                    'log_message': 'Telnet'
                                                    'access! Use ssh instead'},
                                                   {'log_level': 'INFO',
                                                    'log_message': 'User wil'
                                                    'is connected'}], 42,
                                ['Hi', 'five']])

    data_stream.print_processors_stats()

    print("Consume some elements from the data processors: Numeric 3, Text 2, \
Log 1")
    numeric.output()
    numeric.output()
    numeric.output()
    text.output()
    text.output()
    log.output()

    data_stream.print_processors_stats()
