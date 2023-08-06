from typing import TypeVar, Union, Callable, Iterable

T = TypeVar("T")

# Find the first item in an iterable
# Safe to use for lazy iterables
def find(l: Iterable[T], pred: Callable[[T], bool]) -> Union[T, None]:
    try:
        # Nifty little generator trick from https://stackoverflow.com/a/9542768
        return next(x for x in l if pred(x))
    except StopIteration:
        return None


def make_id(n_uces: int, start_from: int = 0):
    def next_id():
        next_id.i += 1
        seq_number_digits_required = len(str(n_uces))

        return "uce" + str(next_id.i).zfill(seq_number_digits_required)

    next_id.i = start_from

    return next_id
