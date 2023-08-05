__version__ = "1.0.0"

import hashlib
from collections import Counter
from re import findall
from secrets import choice
from string import ascii_letters, ascii_lowercase, ascii_uppercase
from string import digits as all_digits
from string import punctuation

import requests


def check_password(password):
    """Check a given password against known data breaches

    Note:
        This method uses the `Have I Been Pwned <https://haveibeenpwned.com/>`_ Passwords API. The unhashed password nor its full `SHA-1 <https://en.wikipedia.org/wiki/SHA-1>`_ hash never leave the device.

    Args:
        password (str): The password to check

    Returns:
        int: The number of times the password has been found
    """

    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest()

    response = requests.get(f"https://api.pwnedpasswords.com/range/{sha1[:5]}")

    hash_suffix_list = [x.split(":") for x in response.text.splitlines(False)]

    try:
        count = [
            count for suffix, count in hash_suffix_list if sha1.endswith(suffix.lower())
        ][0]
    except IndexError:
        return 0

    return int(count)


class PasswordRequirements:
    """A set of requirements to check passwords against

    Keyword Args:
        min_length (int): The minimum length of the password
        min_digits (int): The minimum number of digits in the password
        min_special (int): The minimum number of special characters in the password
        min_alpha (int): The minimum number of alphabetical characters in the password
        min_upper (int): The minimum number of uppercase letters in the password
        min_lower (int): The minimum number of lowercase letters in the password

    Todo:
        Use the :meth:`~passwd.check_password` method as a requirement option
    """

    def __init__(
        self,
        *,
        min_length=0,
        min_digits=0,
        min_special=0,
        min_alpha=0,
        min_upper=0,
        min_lower=0,
    ):
        self.min_length = min_length
        self.min_digits = min_digits
        self.min_special = min_special
        self.min_alpha = min_alpha
        self.min_upper = min_upper
        self.min_lower = min_lower

    def check(self, password):
        """Check a password against the requirements

        Args:
            password (str): The password to check

        Returns:
            bool: Whether the password meets all the given requirements
        """

        if len(password) < self.min_length:
            return False

        digits = len(findall(r"\d", password))
        if digits < self.min_digits:
            return False

        special_chars = sum(v for k, v in Counter(password).items() if k in punctuation)
        if special_chars < self.min_special:
            return False

        alpha_chars = sum(v for k, v in Counter(password).items() if k in ascii_letters)
        if alpha_chars < self.min_alpha:
            return False

        upper_chars = sum(
            v for k, v in Counter(password).items() if k in ascii_uppercase
        )
        if upper_chars < self.min_upper:
            return False

        lower_chars = sum(
            v for k, v in Counter(password).items() if k in ascii_lowercase
        )
        if lower_chars < self.min_lower:
            return False

        return True


class PasswordGenerator:
    """A random password generator

    Args:
        length (int): The length of the password

    Keyword Args:
        uppercase (bool): Whether to allow uppercase letters in the password
        lowercase (bool): Whether to allow lowercase letters in the password
        digits (bool): Whether to allow numerical digits in the password
        special (bool): Whether to allow special characters in the password
    """

    def __init__(
        self, length, *, uppercase=True, lowercase=True, digits=True, special=True
    ):
        self.length = length
        self.uppercase = uppercase
        self.lowercase = lowercase
        self.digits = digits
        self.special = special

    def generate(self):
        """Generate a random password

        Returns:
            str: The freshly generated password
        """
        allowed_chars = ""

        if self.uppercase:
            allowed_chars += ascii_uppercase

        if self.lowercase:
            allowed_chars += ascii_lowercase

        if self.digits:
            allowed_chars += all_digits

        if self.special:
            allowed_chars += punctuation

        return "".join(choice(allowed_chars) for _ in range(self.length))

    def __len__(self):
        return self.length if self.length >= 0 else 0
