from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Implication(AKnight, And(AKnave, AKnight)),
    Implication(AKnave, Not(And(AKnave, AKnight)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Implication(AKnight, And(BKnave, AKnave)),
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    Or(Implication(AKnight, And(AKnight, BKnight)),
    Implication(AKnight, And(AKnave, BKnave))),

    Or(Implication(AKnave, And(AKnave, BKnight)),
    Implication(AKnave, And(AKnight, BKnave))),

    Or(Implication(BKnight, And(AKnight, BKnave)),
    Implication(BKnight, And(AKnave, BKnight))),

    Or(Implication(BKnave, And(AKnight, BKnight)),
    Implication(BKnave, And(AKnave, BKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    Implication(AKnight, And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)))),
    Implication(AKnave, Not(And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))))),

    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight)),

    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    Implication(BKnight, Implication(And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))), AKnave)),
    Implication(BKnave, Not(Implication(And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))), AKnave)))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
