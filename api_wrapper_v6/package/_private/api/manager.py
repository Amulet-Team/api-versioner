from __future__ import annotations

from typing import Dict, Type, List, TYPE_CHECKING

if TYPE_CHECKING:
    from package._private.abstract import AbstractAPI, AbstractAPIFactory


class FactoryManager:
    def __init__(self):
        self.__apis: Dict[Type[AbstractAPI], AbstractAPIFactory] = {}
        print("manager", self)

    @property
    def factories(self) -> List[AbstractAPIFactory]:
        # return self.__apis
        return list(self.__apis.values())

    def register(self, factory: AbstractAPIFactory):
        if factory.APIBase in self.__apis:
            raise Exception(f"Tried to register factory for {factory.APIBase} more than once")
        self.__apis[factory.APIBase] = factory
        print(factory)


api_manager = FactoryManager()
