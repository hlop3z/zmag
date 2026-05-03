from spoc import SingletonMeta

import re
import unicodedata


def _safe(v):
    return v if isinstance(v, str) else str(v)


def _normalize(v):
    """Normalize unicode (e.g., accents) to ASCII-friendly form."""
    return unicodedata.normalize("NFKD", _safe(v)).encode("ascii", "ignore").decode()


STRING_TRANSFORMS = {
    "lower": lambda v: _safe(v).lower(),
    "upper": lambda v: _safe(v).upper(),
    "title": lambda v: _safe(v).title(),
    "capitalize": lambda v: _safe(v).capitalize(),
    "strip": lambda v: _safe(v).strip(),
    "replace_space_with_underscore": lambda v: _safe(v).replace(" ", "_"),
    "remove_spaces": lambda v: _safe(v).replace(" ", ""),
    "collapse_spaces": lambda v: " ".join(_safe(v).split()),
    "snake_case": lambda v: "_".join(_safe(v).strip().lower().split()),
    "kebab_case": lambda v: "-".join(_safe(v).strip().lower().split()),
    "only_digits": lambda v: "".join(ch for ch in _safe(v) if ch.isdigit()),
    "only_alpha": lambda v: "".join(ch for ch in _safe(v) if ch.isalpha()),
    "only_alnum": lambda v: "".join(ch for ch in _safe(v) if ch.isalnum()),
    "normalize_ascii": lambda v: _normalize(v),
    "slugify": lambda v: re.sub(r"[^a-z0-9]+", "-", _normalize(v).lower()).strip("-"),
    "single_line": lambda v: " ".join(_safe(v).splitlines()),
    "trim_to_none": lambda v: (_safe(v).strip() or None),
}


class Tools(metaclass=SingletonMeta):
    def __init__(self):
        # Tools
        self.cleanup = {**STRING_TRANSFORMS}


tools: Tools = Tools()
