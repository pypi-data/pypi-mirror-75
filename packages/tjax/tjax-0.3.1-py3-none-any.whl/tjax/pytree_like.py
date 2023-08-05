from __future__ import annotations

from typing import Hashable, Protocol, Sequence, Tuple, Type, TypeVar, runtime_checkable

from .annotations import PyTree

__all__ = ['PyTreeLike']


T = TypeVar('T', bound='PyTreeLike')


@runtime_checkable
class PyTreeLike(Protocol):

    def tree_flatten(self) -> Tuple[Sequence[PyTree], Hashable]:
        """
        Returns:
            trees: A JAX PyTree of trees representing the object.
            hashed: Data that will be treated as constant through JAX operations.
        """
        ...

    @classmethod
    def tree_unflatten(cls: Type[T], hashed: Hashable, trees: Sequence[PyTree]) -> T:
        """
        Args:
            hashed: Data that will be treated as constant through JAX operations.
            trees: A JAX PyTree of trees from which the object is constructed.
        Returns:
            A constructed object.
        """
        ...
