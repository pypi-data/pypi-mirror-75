from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class AuthBase(ABC):
    """ this would best be an interface or abstract base class.
     views can supply their own object of a class subclassed from this class
     in order to implement the various security methods

     Auth object also provides for limiting database retrieval to records relating
     to the Auth object.  Typically a 'member' so only records for that member
     for this purpose should have method for each possible join value"""

    @property
    @abstractmethod
    def memberID(self) -> Any:
        pass

    @property
    @staticmethod
    def member_string(self) -> str:
        pass

    @property
    def sqlid(self) -> int:
        return 0  # a legacy of old data bases.. auth data includes the sqlid of the member


@dataclass
class AuthAnyBody(AuthBase):
    @property
    def memberID(self) -> Any:
        return 0

    @property
    def member_string(self) -> str:
        return "AnyBody"
