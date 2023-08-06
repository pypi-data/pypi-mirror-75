from typing import Union


class Collection(list):

    def avg(self, key: str = None) -> Union[float, None]:
        """Alias for the average method.

        Args:
            key: Key to pass into average method.

        Returns:
            Result of the average method.
        """
        return self.average(key)

    def average(self, key: str = None) -> Union[float, None]:
        """Return the average of the collection.

        Whenever key is set the average of the values that are assosiated with this
        key will be used to calculate the average.

        Args:
            key: Key to use for the average calculation.

        Returns:
            Average of the (key) values in the Collection.
        """
        if not len(self):
            return float('nan')
        if not key:
            return sum(self) / len(self)
        else:
            return sum([element[key] for element in self]) / len(self)

    def chunk(self, chunk_size: int) -> 'Collection':
        """Break the collection into smaller collections of size chunk_size.

        Args:
            chunk_size: Size of each chunk.

        Returns:
            Collection of chunks.
        """
        return collect([collect(self[i:i + chunk_size])
                        for i in range(0, len(self), chunk_size)])

    def collapse(self) -> "Collection":
        """Collapse collection of arrays into a single flat collection.

        Returns:
            Flattened collection.
        """
        return collect([item for sublist in self for item in sublist])

    def concat(self, other) -> "Collection":
        """Append a given array or collection to the current collection.

        Returns:
            Combined collection.
        """
        return collect(self + other)

    def contains(self):
        raise NotImplementedError

    def contains_strict(self):
        raise NotImplementedError

    def count(self):
        return len(self)

    def count_by(self):
        raise NotImplementedError

    def cross_join(self):
        raise NotImplementedError

    def dd(self):
        raise NotImplementedError

    def diff(self):
        raise NotImplementedError

    def diff_assoc(self):
        raise NotImplementedError

    def diff_keys(self):
        raise NotImplementedError

    def dump(self):
        raise NotImplementedError

    def duplicates(self):
        raise NotImplementedError

    def duplicates_strict(self):
        raise NotImplementedError

    def each(self):
        raise NotImplementedError

    def each_spread(self):
        raise NotImplementedError

    def every(self):
        raise NotImplementedError

    def except_(self):
        raise NotImplementedError

    def filter(self):
        raise NotImplementedError

    def first(self):
        # TODO: Should return first value that passes certain criteria.
        return self[0]

    def first_where(self):
        raise NotImplementedError

    def flat_map(self):
        raise NotImplementedError

    def flatten(self):
        raise NotImplementedError

    def flip(self):
        raise NotImplementedError

    def forget(self):
        raise NotImplementedError

    def for_page(self):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError

    def group_by(self):
        raise NotImplementedError

    def has(self):
        raise NotImplementedError

    def implode(self):
        raise NotImplementedError

    def intersect(self):
        raise NotImplementedError

    def intersect_by_keys(self):
        raise NotImplementedError

    def is_empty(self):
        raise NotImplementedError

    def is_not_empty(self):
        raise NotImplementedError

    def join(self):
        raise NotImplementedError

    def key_by(self):
        raise NotImplementedError

    def keys(self):
        raise NotImplementedError

    def last(self):
        raise NotImplementedError

    def macro(self):
        raise NotImplementedError

    def make(self):
        raise NotImplementedError

    def map(self):
        raise NotImplementedError

    def map_into(self):
        raise NotImplementedError

    def map_spread(self):
        raise NotImplementedError

    def mapToGroups(self):
        raise NotImplementedError

    def mapWithKeys(self):
        raise NotImplementedError

    def max(self):
        raise NotImplementedError

    def median(self):
        raise NotImplementedError

    def merge(self):
        raise NotImplementedError

    def mergeRecursive(self):
        raise NotImplementedError

    def min(self):
        raise NotImplementedError

    def mode(self):
        raise NotImplementedError

    def nth(self):
        raise NotImplementedError

    def only(self):
        raise NotImplementedError

    def pad(self):
        raise NotImplementedError

    def partition(self):
        raise NotImplementedError

    def pipe(self):
        raise NotImplementedError

    def pluck(self):
        raise NotImplementedError

    def pop(self):
        raise NotImplementedError

    def prepend(self):
        raise NotImplementedError

    def pull(self):
        raise NotImplementedError

    def push(self):
        raise NotImplementedError

    def put(self):
        raise NotImplementedError

    def random(self):
        raise NotImplementedError

    def reduce(self):
        raise NotImplementedError

    def reject(self):
        raise NotImplementedError

    def replace(self):
        raise NotImplementedError

    def replaceRecursive(self):
        raise NotImplementedError

    def reverse(self):
        raise NotImplementedError

    def search(self):
        raise NotImplementedError

    def shift(self):
        raise NotImplementedError

    def shuffle(self):
        raise NotImplementedError

    def skip(self):
        raise NotImplementedError

    def skipUntil(self):
        raise NotImplementedError

    def skipWhile(self):
        raise NotImplementedError

    def slice(self):
        raise NotImplementedError

    def some(self):
        raise NotImplementedError

    def sort(self):
        raise NotImplementedError

    def sortBy(self):
        raise NotImplementedError

    def sortByDesc(self):
        raise NotImplementedError

    def sortDesc(self):
        raise NotImplementedError

    def sortKeys(self):
        raise NotImplementedError

    def sortKeysDesc(self):
        raise NotImplementedError

    def splice(self):
        raise NotImplementedError

    def split(self):
        raise NotImplementedError

    def sum(self):
        raise NotImplementedError

    def take(self):
        raise NotImplementedError

    def takeUntil(self):
        raise NotImplementedError

    def takeWhile(self):
        raise NotImplementedError

    def tap(self):
        raise NotImplementedError

    def times(self):
        raise NotImplementedError

    def toArray(self):
        raise NotImplementedError

    def toJson(self):
        raise NotImplementedError

    def transform(self):
        raise NotImplementedError

    def union(self):
        raise NotImplementedError

    def unique(self):
        raise NotImplementedError

    def uniqueStrict(self):
        raise NotImplementedError

    def unless(self):
        raise NotImplementedError

    def unlessEmpty(self):
        raise NotImplementedError

    def unlessNotEmpty(self):
        raise NotImplementedError

    def unwrap(self):
        raise NotImplementedError

    def values(self):
        raise NotImplementedError

    def when(self):
        raise NotImplementedError

    def whenEmpty(self):
        raise NotImplementedError

    def whenNotEmpty(self):
        raise NotImplementedError

    def where(self):
        raise NotImplementedError

    def whereStrict(self):
        raise NotImplementedError

    def whereBetween(self):
        raise NotImplementedError

    def whereIn(self):
        raise NotImplementedError

    def whereInStrict(self):
        raise NotImplementedError

    def whereInstanceOf(self):
        raise NotImplementedError

    def whereNotBetween(self):
        raise NotImplementedError

    def whereNotIn(self):
        raise NotImplementedError

    def whereNotInStrict(self):
        raise NotImplementedError

    def whereNotNull(self):
        raise NotImplementedError

    def whereNull(self):
        raise NotImplementedError

    def wrap(self):
        raise NotImplementedError

    def zip(self):
        raise NotImplementedError

    # These Laravel Collection methods are key-based. We need to decide whether we
    # still can / want to implement these.
    # def combine(self):


def collect(data: list = None) -> Collection:
    data = data or []
    return Collection(data)


