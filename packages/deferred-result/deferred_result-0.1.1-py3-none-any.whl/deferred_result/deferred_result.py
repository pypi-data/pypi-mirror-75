from threading import Event
from typing import TypeVar, Generic, Optional

T = TypeVar('T')


class DeferredResult(Generic[T]):
    def __init__(self) -> None:
        self._finished = Event()
        self._value: Optional[T] = None
        self._error: Optional[Exception] = None

    def resolve(self, value: T) -> None:
        if self._finished.is_set():
            raise RuntimeError('Deferred result already resolved')

        self._value = value
        self._finished.set()

    def reject(self, error: Exception) -> None:
        if self._finished.is_set():
            raise RuntimeError('Deferred result already resolved')

        self._error = error
        self._finished.set()

    def get(self, timeout=None) -> T:
        if not self._finished.wait(timeout):
            raise TimeoutError()

        if self._error:
            raise self._error

        return self._value

    @classmethod
    def resolved(cls, value: T) -> 'DeferredResult[T]':
        r = DeferredResult[T]()
        r.resolve(value)

        return r

    @classmethod
    def rejected(cls, error: Exception) -> 'DeferredResult[T]':
        r = DeferredResult()
        r.reject(error)

        return r
