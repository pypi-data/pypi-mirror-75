"""Base classes used by the Auraxium object model."""

import abc
import logging
from typing import (Any, ClassVar, get_args, List, Optional, Type,
                    TYPE_CHECKING, TypeVar, Union)

from .cache import TLRUCache
from .census import Query
from .errors import BadPayloadError
from .request import extract_payload, extract_single, run_query
from .types import CensusData

if TYPE_CHECKING:
    # This is only imported during static type checking to resolve the 'Client'
    # forward reference. During runtime, this would cause a circular import.
    from .client import Client

__all__ = ['Ps2Object', 'Cached', 'Named']

CachedT = TypeVar('CachedT', bound='Cached')
NamedT = TypeVar('NamedT', bound='Named')
Ps2DataT = TypeVar('Ps2DataT', bound='Ps2Data')
Ps2ObjectT = TypeVar('Ps2ObjectT', bound='Ps2Object')
log = logging.getLogger('auraxium.ps2')


class Ps2Data(metaclass=abc.ABCMeta):
    """Base class for PS2 data classes.

    This defines the interface used to populate the data classes.
    """

    def __post_init__(self) -> None:
        """Enforce type constraints after initialisation."""
        assert hasattr(self, '__annotations__')
        # pylint: disable=no-member
        for name, type_ in self.__annotations__.items():
            value = getattr(self, name)
            if types := get_args(type_):
                if not any(isinstance(value, t) for t in types):
                    raise TypeError(
                        f'Field {name} got {type(value)}, expected {type_}')
            elif not isinstance(value, type_):
                raise TypeError(
                    f'Field {name} got {type(value)}, expected {type_}')

    @classmethod
    @abc.abstractmethod
    def from_census(cls: Type[Ps2DataT], data: CensusData) -> Ps2DataT:
        """Populate the data class with values from the dictionary.

        This parses the API response and casts the appropriate types.
        """
        ...


class Ps2Object(metaclass=abc.ABCMeta):
    """Common base class for all PS2-related objects.

    Subclasses must implement the abstract Ps2Object._extract_fields()
    method used to validate Census API responses before storage.
    """

    # NOTE: These names will be overwritten by the abstract class properties
    # below, but mypy seems to be confused by them, typing them as
    # Callable[[], str].
    # This is redundant but ensures mypy can supply correct type hints for
    # these attributes while still requiring subclasses to overwrite them.
    collection: ClassVar[str] = ''
    id_field: ClassVar[str] = ''

    @property  # type: ignore
    @classmethod
    @abc.abstractmethod
    def collection(cls) -> str:  # pylint: disable=function-redefined
        """Return the unique collection associated with this object."""
        raise NotImplementedError

    @property  # type: ignore
    @classmethod
    @abc.abstractmethod
    def id_field(cls) -> str:  # pylint: disable=function-redefined
        """Return the ID field name for this object."""
        raise NotImplementedError

    def __init__(self, data: CensusData, client: 'Client') -> None:
        """Initialise the object.

        This sets the object's id attribute and populates it using the
        provided payload.

        Args:
            data: The census response dictionary to populate the
                object with.
            client (optional): The client object to use for requests
                performed via this object. Defaults to None.

        """
        id_ = int(data[self.id_field])
        log.debug('Instantiating <%s:%d> using payload: %s',
                  self.__class__.__name__, id_, data)
        self.id = id_  # pylint: disable=invalid-name
        self._client = client
        try:
            self.data = self._build_dataclass(data)
        except KeyError as err:
            raise BadPayloadError(
                f'Unable to populate {self.__class__.__name__} due to a '
                f'missing key: {err.args[0]}') from err

    def __eq__(self, value: Any) -> bool:
        if not isinstance(value, self.__class__):
            return False
        return self.id == value.id

    def __hash__(self) -> int:
        return hash((self.__class__, self.id))

    def __repr__(self) -> str:
        """Return the unique string representation of this object.

        This will take the form of <Class:id>, e.g. <Weapon:108>.

        Returns:
            A string representing the object.

        """
        return f'<{self.__class__.__name__}:{self.id}>'

    @staticmethod
    @abc.abstractmethod
    def _build_dataclass(data: CensusData) -> Ps2Data:
        ...

    @classmethod
    async def count(cls: Type[Ps2ObjectT], client: 'Client',
                    **kwargs: Any) -> int:
        """Return the number of items matching the given terms.

        Args:
            client: The client through which to perform the request.
            **kwargs: Any number of filters to apply.

        Returns:
            The number of entries entries.

        """
        service_id = 's:example' if client is None else client.service_id
        query = Query(cls.collection, service_id=service_id, **kwargs)
        result = await run_query(query, verb='count', session=client.session)
        try:
            return int(result['count'])
        except KeyError as err:
            raise BadPayloadError(
                'Missing key "count" in API response') from err
        except ValueError as err:
            raise BadPayloadError(f'Invalid count: {result["count"]}') from err

    @classmethod
    async def find(cls: Type[Ps2ObjectT], results: int = 10, *,
                   offset: int = 0,
                   promote_exact: bool = False, check_case: bool = True,
                   client: 'Client', **kwargs: Any) -> List[Ps2ObjectT]:
        """Return a list of entries matching the given terms.

        This returns up to as many entries as indicated by the results
        argument. Note that it may be fewer.

        Args:
            results (optional): The maximum number of results. Defaults
                to 10.
            offset (optional): The number of entries to skip. Useful
                for paginated views. Defaults to 0.
            promote_exact (optional): If enabled, exact matches to
                non-exact searches will always come first in the return
                list. Defaults to False.
            check_case (optional): Whether to check case when comparing
                strings. Note that case-insensitive searches are much
                more expensive. Defaults to True.
            client: The client through which to perform the request.
            **kwargs: Any number of filters to apply.

        Returns:
            A list of matching entries.

        """
        # kwargs = dict(cls._translate_field(k, v) for k, v in kwargs.items())
        service_id = 's:example' if client is None else client.service_id
        query = Query(cls.collection, service_id=service_id, **kwargs)
        query.limit(results)
        if offset > 0:
            query.offset(offset)
        query.exact_match_first(promote_exact).case(check_case)
        matches = await run_query(query, verb='get', session=client.session)
        return [cls(i, client=client) for i in extract_payload(
            matches, cls.collection)]

    @classmethod
    async def get(cls: Type[Ps2ObjectT], client: 'Client',
                  check_case: bool = True, **kwargs: Any
                  ) -> Optional[Ps2ObjectT]:
        """Return the first entry matching the given terms.

        Like Ps2Object.get(), but will only return one item.

        Args:
            client: The client through which to perform the request.
            check_case (optional): Whether to check case when comparing
                strings. Note that case-insensitive searches are much
                more expensive. Defaults to True.

        Returns:
            A matching entry, or None if not found.

        """
        results = await cls.find(client=client, results=1,
                                 check_case=check_case, **kwargs)
        if results:
            return results[0]
        return None

    @classmethod
    async def get_by_id(cls: Type[Ps2ObjectT], id_: int, *, client: 'Client'
                        ) -> Optional[Ps2ObjectT]:
        """Retrieve an object by its unique Census ID.

        Args:
            id_: The unique ID of the object.
            client: The client through which to perform the request.

        Returns:
            The entry with the matching ID, or None if not found.

        """
        filters: CensusData = {cls.id_field: id_}
        results = await cls.find(client=client, results=1, **filters)
        if results:
            return results[0]
        return None

    def query(self) -> Query:
        """Return a query from the current object.

        This is a utility method targeted at advanced users and
        developers. It is generally not required for most use cases.
        """
        return Query(collection=self.collection,
                     service_id=self._client.service_id)


class Cached(Ps2Object, metaclass=abc.ABCMeta):
    """Base class for cacheable data types.

    This generates a cache for each subclass that allows the storage
    and retrieval of objects by ID. This cache can be customised using
    keyword arguments as part of the class definition.

    This customisation is done via two parameters: the cache size and
    the TTU.

    The cache size defines the maximum number of items the
    cache may bold before it will discard the least recently used item
    for every new item added.

    The TTU (time-to-use) will independently
    discard items that are older than the given number of seconds to
    ensure data does not go too far out of date.
    """

    _cache: ClassVar[TLRUCache[int, Any]]

    def __init__(self, data: CensusData, client: 'Client') -> None:
        """Initialise the cached object."""
        super().__init__(data=data, client=client)
        self._cache.add(self.id, self)

    @classmethod
    def __init_subclass__(cls: Type[CachedT], cache_size: int,
                          cache_ttu: float = 0.0) -> None:
        """Initialise a cacheable subclass.

        This sets up the TLRU cache for the given subclass using the
        keyword arguments provided.

        Args:
            cache_size: The maximum number of items in the cache. Once
                the cache reaches this number of items, it will delete
                the  least recently used item for every new item added.
            cache_ttu (optional): The time-to-use for cache items. If
                an item is older than its TTU allows, it will be
                re-fetched regardless of how often it is accessed.
                Defaults to 0.0.

        """
        super().__init_subclass__()
        log.debug('Setting up cache for %s (size: %d, ttu: %.1f sec.)',
                  cls.__name__, cache_size, cache_ttu)
        cls._cache = TLRUCache(size=cache_size, ttu=cache_ttu,
                               name=f'{cls.__name__}_Cache')

    @classmethod
    def alter_cache(cls, size: int, ttu: Optional[float] = None) -> None:
        """Modify the class cache to use a new size and TTU.

        This will update and clear the cache for the current class.

        Args:
            size: The new cache size.
            ttu (optional): The new item TTU. Defaults to None.

        Raises:
            ValueError: Raised if the size is less than 1.

        """
        if size < 1:
            raise ValueError(f'{size} is not a valid cache size')
        cls._cache.clear()
        cls._cache.size = size
        if ttu is not None:
            cls._cache.ttu = ttu

    @classmethod
    def _check_cache(cls: Type[CachedT], id_: int) -> Optional[CachedT]:
        """Attempt to restore an item from the cache.

        If the item cannot be found, None will be returned instead.

        Args:
            id_: The unique identifier the item is cached by.

        Returns:
            An existing instance if found, or None if the object has
            not been retrieved before or expired.

        """
        return cls._cache.get(id_)

    @classmethod
    async def get_by_id(cls: Type[CachedT], id_: int, *, client: 'Client'
                        ) -> Optional[CachedT]:
        """Retrieve an object by by ID.

        This query uses caches and might return an existing instance if
        the object has been recently retrieved. Use the no_cache flag
        to force retrieval of fresh data.

        If no session is provided, one will be created locally. It is
        highly recommended to always specify a session object.

        Args:
            id_: The unique id of the object.
            client: The client through which to perform the request.

        Returns:
            The object matching the given ID or None if no match was
            found.

        """
        filters: CensusData = {cls.id_field: id_}
        log.debug('<%s:%d> requested', cls.__name__, id_)
        if (instance := cls._cache.get(id_)) is not None:
            log.debug('%r restored from cache', instance)
            return instance  # type: ignore
        log.debug('<%s:%d> not cached, generating API query...',
                  cls.__name__, id_)
        return await cls.get(client=client, **filters)


class Named(Cached, cache_size=0, cache_ttu=0.0, metaclass=abc.ABCMeta):
    """Mix-in class for named objects."""

    _cache: ClassVar[TLRUCache[Union[int, str], Any]]  # type: ignore

    def __init__(self, *args: Any, locale: Optional[str] = None,
                 **kwargs: Any) -> None:
        """Initialise the named object.

        This sets the object's id attribute and adds it to the cache.

        Args:
            locale: The locale under which to cache this object.
            *args: Any extra positional arguments are forwarded to the
                Cached class's initialiser.
            **kwargs: Any keyword arguments are forwarded to the
                Cached class's initialiser.

        """
        super().__init__(*args, **kwargs)
        if locale is not None:
            key = f'{locale}_{self.name(locale=locale).lower()}'
            self._cache.add(key, self)

    def __repr__(self) -> str:
        """Return the unique string representation of the faction.

        This will take the form of <class:id:name>, e.g.
        <Item:2:NC4 Mag-Shot>.

        Returns:
            A string representing the object.

        """
        return (f'<{self.__class__.__name__}:{self.id}:'
                f'\'{self.name(locale="en")}\'>')

    def __str__(self) -> str:
        """Return the string representation of this object.

        This calls the Named.name() method for the English locale.

        Returns:
            A string representation of the object.

        """
        return self.name(locale='en')

    @classmethod
    async def get_by_name(cls: Type[NamedT], name: str, *, locale: str = 'en',
                          client: 'Client') -> Optional[NamedT]:
        """Retrieve an object by its unique name.

        This query is always case-insensitive.

        Args:
            name: The name to search for.
            locale (optional): The locale of the search key. Defaults
                to 'en'.
            client: The client through which to perform the request.

        Returns:
            The entry with the matching name, or None if not found.

        """
        key = f'{locale}_{name.lower()}'
        log.debug('%s "%s"[%s] requested', cls.__name__, name, locale)
        if (instance := cls._cache.get(key)) is not None:
            log.debug('%r restored from cache', instance)
            return instance  # type: ignore
        log.debug('%s "%s"[%s] not cached, generating API query...',
                  cls.__name__, name, locale)
        query = Query(cls.collection, service_id=client.service_id)
        query.case(False).add_term(field=f'name.{locale}', value=name)
        payload = await run_query(query, verb='get', session=client.session)
        payload = extract_single(payload, cls.collection)
        return cls(payload, locale=locale, client=client)

    def name(self, locale: str = 'en') -> str:
        """Return the localised name of the object.

        Args:
            locale (optional): The locale identifier to return.
                Defaults to 'en'.

        Raises:
            ValueError: Raised if the given locale is unknown.

        Returns:
            The localised name of the object.

        """
        data = self.data
        assert hasattr(data, 'name')
        try:
            return str(getattr(data.name, locale))  # type: ignore
        except AttributeError as err:
            raise ValueError(f'Invalid locale: {locale}') from err
