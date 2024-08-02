import sys

if len(sys.argv) < 2:
    print("Usage: python3 bf.py <filename>")
    sys.exit(1)

with open(sys.argv[1]) as f:
    code = f.read()


def reversed_pointer(s: str) -> str:
    return "".join(
        {
            ">": "<",
            "<": ">",
        }.get(c, c)
        for c in s
    )


def reversed_arithmetic(s: str) -> str:
    return "".join(
        {
            "+": "-",
            "-": "+",
        }.get(c, c)
        for c in s
    )


def multiply_shifts(s: str, m_by: int = 2) -> str:
    return "".join(
        {
            ">": ">" * m_by,
            "<": "<" * m_by,
        }.get(c, c)
        for c in s
    )


output = "".join(c for c in code if c in "+-<>.,[]")
meaningless_sequences = {
    "+-": "",
    "<>": "",
    "][-]": "]",
    "[-],": ",",
    "+>-<-": ">-<",
    "]>-<[-]": "]>-<",
    "+>+<-": ">+<",
    "]>+<[-]": "]>+<",
    "+>.<-": ">.<",
    "]>.<[-]": "]>.<",
    "+>,<-": ">,<",
    "]>,<[-]": "]>,<",
}

meaningless_sequences = {
    **meaningless_sequences,
    **{
        reversed_pointer(k): reversed_pointer(v)
        for k, v in meaningless_sequences.items()
    },
}
meaningless_sequences = {
    **meaningless_sequences,
    **{
        reversed_arithmetic(k): reversed_arithmetic(v)
        for k, v in meaningless_sequences.items()
    },
}
meaningless_sequences = {
    **meaningless_sequences,
    **{
        multiply_shifts(k, 2): multiply_shifts(v, 2)
        for k, v in meaningless_sequences.items()
    },
}
meaningless_sequences = {
    **meaningless_sequences,
    **{
        multiply_shifts(k, 3): multiply_shifts(v, 3)
        for k, v in meaningless_sequences.items()
    },
}
meaningless_sequences = {
    **meaningless_sequences,
    **{
        multiply_shifts(k, 4): multiply_shifts(v, 4)
        for k, v in meaningless_sequences.items()
    },
}
meaningless_sequences = {
    **meaningless_sequences,
    **{
        multiply_shifts(k, 5): multiply_shifts(v, 5)
        for k, v in meaningless_sequences.items()
    },
}
meaningless_sequences = {
    **meaningless_sequences,
    **{
        multiply_shifts(k, 7): multiply_shifts(v, 7)
        for k, v in meaningless_sequences.items()
    },
}
while any(seq in output for seq in meaningless_sequences.keys()):
    for seq, replacement in meaningless_sequences.items():
        output = output.replace(seq, replacement)

print(output, f"{len(output)} bytes", sep="\n")
