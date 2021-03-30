import re
from dataclasses import dataclass
from typing import Dict, Any, Optional, List, Union

from deepdiff import DeepDiff


@dataclass
class AbstractParser:
    data: Dict[str, Any]
    previous_data: Optional[Dict[str, Any]]

    @property
    def messages(self) -> List[str]:
        """
        Forms strings for the Event presentation
        """
        raise NotImplementedError


@dataclass
class Event(AbstractParser):
    @property
    def messages(self) -> List[str]:
        messages = [
            f"Event by: {self.user_verbose}",
            self.event_title,
            self.data["event_time"],
        ]
        if self.flat_changes_message:
            messages.append(self.flat_changes_message)
        for message in self.nested_changes_messages:
            messages.append(message)
        return messages

    @property
    def user_verbose(self) -> str:
        """
        Forms a user's view
        """
        if self.data["user"] and (
            self.data["user"]["first_name"] or self.data["user"]["last_name"]
        ):
            names = [
                self.data["user"][name]
                for name in ["first_name", "last_name"]
                if self.data["user"][name]
            ]
            return " ".join(names)
        elif self.data["user"]:
            return self.data["user"]["username"] or self.data["user"]["id"]
        return "system"

    @property
    def flat_changes_message(self) -> str:
        """
        Generates a message if flat fields in model_data have changed
        """
        if self.previous_data:
            difference = self.__get_differences(
                self.flat_model_data_previous, self.flat_model_data
            )
            return self.__clear_deepdiff_key_notation(difference)
        # An empty string in python is not None, however, the if check fails
        return ""

    @property
    def nested_changes_messages(self) -> List[str]:
        """
        Generates messages about changes of objects nested in model_data
        """
        messages = []
        for key, value in self.nested_differences.items():
            if value:
                messages.append(f"{key}: " + self.__clear_deepdiff_key_notation(value))
        return messages

    @property
    def event_title(self) -> str:
        """
        Event title
        """
        action_name = self.data["extra_data"].get("action_name")
        return (
            f"{self.data['event_type']} - {action_name}"
            if action_name
            else self.data["event_type"]
        )

    @property
    def state(self) -> str:
        return self.data["model_data"]["state"]

    @property
    def status(self) -> str:
        return self.data["model_data"]["status"]

    @property
    def flat_model_data(self) -> Dict[str, Any]:
        """
        model_data without nested objects (flat fields only)
        """
        return self.__filter_flat_data(self.data["model_data"])

    @property
    def flat_model_data_previous(self):
        """
        model_data without nested objects (flat fields only) (previous result)
        """
        return (
            self.__filter_flat_data(self.previous_data["model_data"])
            if self.previous_data
            else None
        )

    @property
    def dict_model_data(self) -> Dict[str, Any]:
        """
        model_data only values of nested objects
        """
        return self.__filter_nested_data(self.data["model_data"])

    @property
    def dict_model_data_previous(self) -> Dict[str, Any]:
        """
        model_data only values of nested objects (previous result)
        """
        return (
            self.__filter_nested_data(self.previous_data["model_data"])
            if self.previous_data
            else None
        )

    @property
    def nested_differences(self) -> Dict[str, str]:
        """
        Gets the difference for each nested object in model_data
        """
        differences = {key: {} for key in self.dict_model_data}
        if self.previous_data:
            for key in differences.keys():
                differences[key] = self.__get_differences(
                    *self.__to_flat_nested_objects(key)
                )
        return differences

    def __clear_deepdiff_key_notation(self, value: str) -> str:
        """
        deepdiff generates poorly readable keys. This function clears them
        """
        return re.sub(r"root(\[\d+])?\[(?P<field_name>.*)]", r"\g<field_name>", value)

    def __get_differences(self, previous, current) -> str:
        diff = DeepDiff(previous, current, ignore_order=True, verbose_level=0)
        return diff.pretty()

    def __to_flat_nested_objects(self, key) -> Union[List[Dict], List[List], List[Any]]:
        """
        We delete objects with an excessive degree of nesting (do not check them)
        """
        previous = self.dict_model_data_previous.get(key)
        current = self.dict_model_data.get(key)
        if type(current) == type(previous) == dict:
            return [self.__filter_flat_data(previous), self.__filter_flat_data(current)]
        elif type(current) == type(previous) == list:
            return [
                [self.__filter_flat_data(child) for child in previous],
                [self.__filter_flat_data(child) for child in current],
            ]
        return [previous, current]

    def __filter_flat_data(self, data) -> Dict[str, Any]:
        return {
            key: value for key, value in data.items() if type(value) not in (list, dict)
        }

    def __filter_nested_data(self, data) -> Dict[str, Union[List, Dict]]:
        return {
            key: value for key, value in data.items() if type(value) in (list, dict)
        }
