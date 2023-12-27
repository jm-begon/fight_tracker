from enum import Enum


class Size(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class Alignment(Enum):
    LG = "lawful good"
    NG = "neutral good"
    CG = "chaotic good"
    LN = "lawful neutral"
    NN = "neutral neutral"
    CN = "chaotic neutral"
    LE = "lawful evil"
    NE = "neutral evil"
    CE = "chaotic evil"
