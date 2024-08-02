from functools import lru_cache
import itertools
import time


def achieve_n(n: int) -> str:
    if n > 128:
        return "-" * (256 - n)
    else:
        return "+" * n


def run_n_times(
    initial: int,
    decrement: int,
    repeat: int,
    additional: int,
    operation: str,
    suboperation: str | None = None,
) -> str:
    # ++++   [ --- > operation < ] > operation <
    if initial == 0:
        return (suboperation or operation) * additional
    if additional == 0:
        return (
            achieve_n(initial)
            + "["
            + achieve_n(decrement)
            + ">"
            + operation * repeat
            + "<]"
        )
    return (
        achieve_n(initial)
        + "["
        + achieve_n(decrement)
        + ">"
        + operation * repeat
        + "<]>"
        + (suboperation or operation) * additional
        + "<"
    )


def get_n_runs(
    initial: int, decrement: int, repeat: int, additional: int
) -> int | None:
    i = additional
    x = initial
    if x == 0:
        return i
    for _ in range(256):
        i += repeat
        x += decrement
        x %= 256
        if x == 0:
            return i
    return None


@lru_cache
def runable(max_deviation: int) -> list[tuple[int, int, int, int]]:
    candidates = itertools.product(
        itertools.chain(range(max_deviation), range(256 - max_deviation, 256)),
        range(256 - max_deviation, 256),
        range(max_deviation),
        range(max_deviation),
    )
    n_to_block = {}
    for i, candidate in enumerate(candidates):
        if i % 10000 == 0:
            total_candidates = max_deviation**4 * 2
            print(
                f"{i}/{total_candidates} - {i / total_candidates * 100:.2f}%; "
                f"{len(n_to_block)} best blocks found",
                end="\r",
            )
        n_runs = get_n_runs(*candidate)
        if n_runs is not None:
            if n_runs not in n_to_block:
                n_to_block[n_runs] = candidate
            else:
                existing = n_to_block[n_runs]
                length_existing = len(run_n_times(*existing, "."))
                length_candidate = len(run_n_times(*candidate, "."))
                if length_candidate < length_existing:
                    n_to_block[n_runs] = candidate
    print()
    return sorted(n_to_block.values())


def generate_increment(
    target: int, depth: int = 1, mod_256: bool = False, max_deviation: int = 6
) -> str | None:
    suitable: list[str] = []
    r = runable(max_deviation)
    start = time.time()
    for i, blocks in enumerate(
        itertools.product(
            r,
            repeat=depth,
        )
    ):
        if i % 10000 == 0:
            time_taken = time.time() - start
            time_estimated = time_taken / (i + 1) * (len(r) ** depth - i)
            time_left = time_estimated - time_taken
            print(
                f"{i}/{len(r) ** depth} - {i / (len(r) ** depth) * 100:.2f}%; "
                f"{len(suitable)} solutions found, ["
                f"{int(time_taken // 60)}:{int(time_taken % 60):02} > "
                f"{int(time_left // 60)}:{int(time_left % 60):02}]",
                end="\r",
            )
        n_runs = 1
        for initial, decrement, repeat, additional in blocks:
            n_subruns = get_n_runs(initial, decrement, repeat, additional)
            if n_subruns is None:
                break
            n_runs *= n_subruns
        else:
            if target == (n_runs % 256 if mod_256 else n_runs):
                operation = "."
                for initial, decrement, repeat, additional in blocks:
                    operation = run_n_times(
                        initial, decrement, repeat, additional, operation
                    )
                suitable.append(operation)
    return min(suitable, key=len) if suitable else None


deviation = 20
print(len(runable(deviation)), "unique blocks")
result = generate_increment(120238, 2, False, deviation)
print()
print(result)
if result:
    print(f"Length: {len(result)}")
