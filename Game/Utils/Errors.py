class GameError(Exception):
    """Base error for every expected failure in the game (shown to the user as a message)."""


class ValidationError(GameError):
    """Invalid input data."""