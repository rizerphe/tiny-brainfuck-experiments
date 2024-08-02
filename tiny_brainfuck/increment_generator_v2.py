from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import itertools
import math
import time
from typing import Iterator


def achieve_n(n: int) -> str:
    if n > 128:
        return "-" * (256 - n)
    else:
        return "+" * n


def len_of_achieve_n(n: int) -> int:
    if n > 128:
        return 256 - n
    else:
        return n


@lru_cache
def get_n_repeats(initial, decrement) -> int | None:
    x = initial
    if x == 0:
        return 0
    i = 0
    for _ in range(256):
        x += decrement
        x %= 256
        i += 1
        if x == 0:
            return i
    return None


@lru_cache
def runable(max_deviation_inc: int, max_deviation_dec: int) -> list[tuple[int, int]]:
    candidates = itertools.product(
        itertools.chain(range(max_deviation_inc), range(256 - max_deviation_inc, 256)),
        range(256 - max_deviation_dec, 256),
    )
    n_to_block: dict[int, tuple[int, int]] = {}
    for i, candidate in enumerate(candidates):
        if i % 10000 == 0:
            total_candidates = max_deviation_inc * max_deviation_dec * 2
            print(
                f"{i}/{total_candidates} - {i / total_candidates * 100:.2f}%; "
                f"{len(n_to_block)} best blocks found",
                end="\r",
            )
        n_runs = get_n_repeats(*candidate)
        if n_runs is None:
            continue
        if n_runs not in n_to_block:
            n_to_block[n_runs] = candidate
        else:
            existing = n_to_block[n_runs]
            length_existing = existing[0] and len_of_achieve_n(
                existing[0]
            ) + len_of_achieve_n(existing[1])
            length_candidate = candidate[0] and len_of_achieve_n(
                candidate[0]
            ) + len_of_achieve_n(candidate[1])
            if length_candidate < length_existing:
                n_to_block[n_runs] = candidate
    print()
    print(f"Total blocks: {len(n_to_block)}")
    return sorted(n_to_block.values())


class Operation:
    def __init__(self, operation: str, max_repeats: int, repeats: int = 1) -> None:
        self.operation = operation
        self.length = len(operation)
        self.max_repeats = max_repeats
        self.repeats = repeats

    def __len__(self) -> int:
        return self.length * self.repeats

    def __str__(self) -> str:
        return self.operation * self.repeats

    def __iter__(self) -> Iterator[Operation]:
        for i in range(self.max_repeats):
            yield Operation(self.operation, self.max_repeats, i)

    def n_options(self) -> int:
        return self.max_repeats

    def runs(self) -> int:
        return self.repeats

    def breakdown(self):
        print(f"this is the operation itself, repeated {self.repeats} times")


@dataclass
class IncrementRealization:
    initial: int
    decrement: int
    repeated_operation: Operation | IncrementRealization
    additional_operation: Operation | IncrementRealization

    def __str__(self) -> str:
        if self.initial == 0:
            return str(self.additional_operation)
        if self.additional_operation.runs() == 0:
            return (
                achieve_n(self.initial)
                + "["
                + achieve_n(self.decrement)
                + ">"
                + str(self.repeated_operation)
                + "<]"
            )
        return (
            achieve_n(self.initial)
            + "["
            + achieve_n(self.decrement)
            + ">"
            + str(self.repeated_operation)
            + "<]>"
            + str(self.additional_operation)
            + "<"
        )

    def __len__(self) -> int:
        if self.initial == 0:
            return len(self.additional_operation)
        if self.additional_operation.runs() == 0:
            return (
                len_of_achieve_n(self.initial)
                + len_of_achieve_n(self.decrement)
                + len(self.repeated_operation)
                + 4
            )
        return (
            len_of_achieve_n(self.initial)
            + len_of_achieve_n(self.decrement)
            + len(self.repeated_operation)
            + len(self.additional_operation)
            + 6
        )

    def runs(self) -> int | None:
        additional_runs = self.additional_operation.runs()
        if additional_runs is None:
            return None
        repeated_runs = self.repeated_operation.runs()
        if repeated_runs is None:
            return None
        repeats = get_n_repeats(self.initial, self.decrement)
        return None if repeats is None else repeats * repeated_runs + additional_runs

    def breakdown(self):
        print(
            "Repeated child:",
            self.repeated_operation,
            f"({self.repeated_operation.runs()} runs; {len(self.repeated_operation)} chars)",
        )
        print(
            "Additional child:",
            self.additional_operation,
            f"({self.additional_operation.runs()} runs; {len(self.additional_operation)} chars)",
        )
        print("Initial:", self.initial)
        print("Decrement:", self.decrement)
        print(f"Will repeat {get_n_repeats(self.initial, self.decrement)} times")
        runs = self.runs()
        if runs is None:
            print("Cannot calculate total runs")
        else:
            print(f"Will run the operation {runs} times")
            print(f"That's {runs % 256} mod 256")
        print("---repeated child breakdown---")
        self.repeated_operation.breakdown()
        print("---additional child breakdown---")
        self.additional_operation.breakdown()


class Increment:
    def __init__(
        self,
        child_options: Increment | Operation,
        deviation_inc: int = 4,
        deviation_dec: int | None = None,
    ):
        self.child_options = child_options
        self.deviation_inc = deviation_inc
        self.deviation_dec = deviation_dec or (deviation_inc * 2)

    def __iter__(self):
        for repeated_op in self.child_options:
            for additional_op in self.child_options:
                for initial, decrement in runable(
                    self.deviation_inc, self.deviation_dec
                ):
                    yield IncrementRealization(
                        initial=initial,
                        decrement=decrement,
                        repeated_operation=repeated_op,
                        additional_operation=additional_op,
                    )

    def n_options(self):
        return (
            len(runable(self.deviation_inc, self.deviation_dec))
            * self.child_options.n_options() ** 2
        )

    def filtered(
        self, target: int, mod_256: bool = False
    ) -> Iterator[IncrementRealization]:
        total = self.n_options()
        shortest_found = math.inf
        shortest_content = ""
        start = time.time()
        for i, realization in enumerate(self):
            if i % 100000 == 0:
                time_taken = time.time() - start
                time_needed = time_taken / (i + 1) * total
                time_remaining = time_needed - time_taken
                print(
                    f"{i/total*100:.2f}%; {shortest_found} shortest: {shortest_content} "
                    f"[{time_taken:.2f}s taken, {time_remaining:.2f}s remaining]",
                    end="\r",
                )
            runs = realization.runs()
            if runs is None:
                continue
            if target == (runs % 256 if mod_256 else runs):
                shortest_found = min(shortest_found, len(realization))
                if shortest_found == len(realization):
                    shortest_content = str(realization)
                yield realization


increment = Increment(Increment(Operation(",", 6)))
print(increment.n_options())
print(f"10 ^ {math.log10(increment.n_options()):.2f}")
shortest = min(increment.filtered(110000), key=len, default=None)
# shortest = max(increment, key=lambda x: x.runs() or 0, default=None)
print("\n" * 3)
if shortest is not None:
    print(shortest)
    shortest.breakdown()
    print("\n" * 2)
    print("length:", len(shortest))
print(shortest)
