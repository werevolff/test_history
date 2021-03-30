from dataclasses import dataclass
from typing import List


@dataclass
class AbstractView:
    messages: List[str]
    delimiter_start: str = "\n\n***"
    delimiter_end: str = "***"

    def output_data(self):
        raise NotImplementedError


class PrintView(AbstractView):
    """
    View Event History with print
    """

    def output_data(self):
        print(self.delimiter_start)
        for i, message in enumerate(self.messages):
            print(message)
            if i + 1 < len(self.messages):
                print("\n")
        print(self.delimiter_end)
