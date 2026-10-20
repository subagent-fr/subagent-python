"""subagent-mail is now escouade-mail: this last version re-exports escouade_mail.

subagent-mail devient escouade-mail : cette dernière version réexporte escouade_mail.
"""
import warnings

from escouade_mail import *  # noqa: F401,F403
from escouade_mail import __all__, __version__  # noqa: F401

warnings.warn(
    "subagent-mail est devenu escouade-mail : pip install escouade-mail, puis import escouade_mail.",
    DeprecationWarning,
    stacklevel=2,
)
