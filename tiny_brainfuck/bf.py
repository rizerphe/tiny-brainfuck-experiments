from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable


class Environment:
    def __init__(self, input_fn: Callable[[], str], output_fn: Callable[[str], None]):
        self.memory: dict[int, int] = {}
        self.pointer = 0
        self.input_fn = input_fn
        self.output_fn = output_fn

    def inc(self):
        self.memory[self.pointer] = (self.memory.get(self.pointer, 0) + 1) % 256

    def dec(self):
        self.memory[self.pointer] = (self.memory.get(self.pointer, 0) + 255) % 256

    def left(self):
        self.pointer -= 1

    def right(self):
        self.pointer += 1

    def out(self):
        self.output_fn(chr(self.memory.get(self.pointer, 0)))

    def inp(self):
        self.memory[self.pointer] = ord(self.input_fn())


class Tag(Enum):
    INC = "+"
    DEC = "-"
    LEFT = "<"
    RIGHT = ">"
    OUT = "."
    IN = ","
    LOOP = "[]"


@dataclass
class Instruction:
    tag: Tag
    body: list[Instruction] = field(default_factory=list)
    length: int = 1

    def __len__(self):
        return self.length

    @classmethod
    def parse(cls, code: str, i: int) -> Instruction | None:
        match code[i]:
            case "+":
                return cls(Tag.INC)
            case "-":
                return cls(Tag.DEC)
            case "<":
                return cls(Tag.LEFT)
            case ">":
                return cls(Tag.RIGHT)
            case ".":
                return cls(Tag.OUT)
            case ",":
                return cls(Tag.IN)
            case "[":
                body: list[Instruction] = []
                i += 1
                length = 2
                while code[i] != "]":
                    n = cls.parse(code, i)
                    if n is not None:
                        body.append(n)
                        i += len(n)
                        length += len(n)
                    else:
                        i += 1
                        length += 1
                return cls(Tag.LOOP, body, length)
            case "]":
                raise ValueError("Unmatched ']'")
            case _:
                return None

    @classmethod
    def parse_all(cls, code: str) -> list[Instruction]:
        instructions = []
        i = 0
        while i < len(code):
            instruction = cls.parse(code, i)
            if instruction is None:
                i += 1
            else:
                instructions.append(instruction)
                i += len(instruction)
        return instructions

    def run(self, env: Environment):
        match self.tag:
            case Tag.INC:
                env.inc()
            case Tag.DEC:
                env.dec()
            case Tag.LEFT:
                env.left()
            case Tag.RIGHT:
                env.right()
            case Tag.OUT:
                env.out()
            case Tag.IN:
                env.inp()
            case Tag.LOOP:
                while env.memory.get(env.pointer, 0) != 0:
                    for i in self.body:
                        i.run(env)


class Inputer:
    def __init__(self, prepared: str = "") -> None:
        self.inputed_digits = 0
        self.prepared = prepared

    def __call__(self):
        self.inputed_digits += 1
        return self.prepared[min(self.inputed_digits, len(self.prepared)) - 1]


def main():
    import sys

    if len(sys.argv) != 2:
        print("Usage: bf.py <file>")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        code = f.read()

    instructions = Instruction.parse_all(code)
    inputer = Inputer("10000 10000 4")
    env = Environment(inputer, print)
    for i in instructions:
        i.run(env)

    print(f"read {inputer.inputed_digits} digits")


if __name__ == "__main__":
    main()
