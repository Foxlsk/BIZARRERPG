import re
from Utils.Errors import ValidationError

class Validation:
    UsernamePattern = re.compile(r"^[A-Za-z0-9_]{3,20}$")
    EmailPattern = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
    NamePattern = re.compile(r"^[A-Za-zÀ-ÿ0-9' ]{3,20}$")
    CodePattern = re.compile(r"^[a-z0-9_]{3,40}$")

    def Username(Value):
        Value = str(Value).strip()
        if not Validation.UsernamePattern.match(Value):
            raise ValidationError("Username must have 3-20 characters (letters, numbers or _).")
        return Value

    def Email(Value):
        Value = str(Value).strip().lower()
        if len(Value) > 100 or not Validation.EmailPattern.match(Value):
            raise ValidationError("Invalid email address.")
        return Value

    def Password(Value):
        Value = str(Value)
        if len(Value) < 8 or len(Value) > 64:
            raise ValidationError("Password must have between 8 and 64 characters.")
        if not re.search(r"[A-Za-z]", Value) or not re.search(r"[0-9]", Value):
            raise ValidationError("Password must contain at least one letter and one number.")
        return Value

    def CharacterName(Value):
        Value = " ".join(str(Value).split())
        if not Validation.NamePattern.match(Value):
            raise ValidationError("Name must have 3-20 characters (letters, numbers, spaces or ').")
        return Value

    def Code(Value):
        Value = str(Value).strip().lower()
        if not Validation.CodePattern.match(Value):
            raise ValidationError("Code must have 3-40 characters (lowercase letters, numbers or _).")
        return Value

    def Text(Value, Field, MinLength=1, MaxLength=200):
        Value = str(Value).strip()
        if len(Value) < MinLength or len(Value) > MaxLength:
            raise ValidationError(f"{Field} must have between {MinLength} and {MaxLength} characters.")
        return Value

    def Int(Value, Field, Min=None, Max=None):
        try:
            Number = int(str(Value).strip())
        except (TypeError, ValueError):
            raise ValidationError(f"{Field} must be a whole number.")
        if Min is not None and Number < Min:
            raise ValidationError(f"{Field} must be at least {Min}.")
        if Max is not None and Number > Max:
            raise ValidationError(f"{Field} must be at most {Max}.")
        return Number

    def Probability(Value, Field):
        try:
            Number = float(str(Value).strip().replace(",", "."))
        except (TypeError, ValueError):
            raise ValidationError(f"{Field} must be a number between 0 and 1.")
        if Number < 0 or Number > 1:
            raise ValidationError(f"{Field} must be between 0 and 1.")
        return Number

    def Choice(Value, Field, Options):
        for Option in Options:
            if str(Value).strip().lower() == Option.lower():
                return Option
        raise ValidationError(f"{Field} must be one of: {', '.join(Options)}.")
