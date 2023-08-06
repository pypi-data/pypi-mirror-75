"""
Core functionality and mixins.
"""
# pylint: disable=too-few-public-methods

from __future__ import annotations
from typing import TypeVar, Generic, Optional, Type, Any, List, Dict


T = TypeVar('T')


class SingletonMeta(type, Generic[T]):  # pylint: disable=unsubscriptable-object
    """Singleton metaclass."""
    _instance: Optional[T] = None

    def __call__(cls, *args: List[Any], **kwargs: Dict[str, Any]
                 ) -> T:
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class ChildsTreeMixin:
    """Applying childs tree functionality."""
    _childs_list: List[Any]
    _childs: Optional[Dict[str, Any]] = None

    def __init__(self, *args: Any, **kwargs: Dict[str, Any]) -> None:
        self._childs_list: List[Any] = [
            i(*args, **kwargs) for i in self.childs.values()
        ]

    @property
    def childs(self) -> Dict[str, Type[Any]]:
        """Return childs classes dict."""
        if self._childs is None:
            self._childs = {
                child.__name__: child
                for child in self.__class__.__subclasses__()
            }
        return self._childs
