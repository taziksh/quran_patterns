#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quranic Numeric Patterns Analysis

This script aims to verify the numeric patterns related to the Bismillah,
Ism, Allah, Rahman, and Rahim in the Quran, per the bullet points:

1) Bismillah = 19 letters
2) Ism (اسم) without contraction => 19 times
3) Allah (الله) => 2698 times (19×142)
   - with possible expansions
4) Rahman (الرحمن) => 57 times (19×3)
5) Rahim (الرحيم) => 114 times (19×6)
6) And checks for the other well-known 19-based patterns:
   - 114 chapters, 6346 total verses, cross-sum = 19, etc.
   
Depending on your Quran text file (and how morphological variants are handled),
you may or may not exactly match the historical claims. This script provides
a configurable approach to get as close as possible to those reported numbers.
"""

import re
from collections import Counter

##############################################################################
# Configuration Flags
##############################################################################

# Strip diacritics from the text (common practice to unify forms)
STRIP_DIACRITICS = True

# Remove all non-Arabic codepoints (e.g., footnotes, translations)
REMOVE_NON_ARABIC = True

# Handle expansions for "Allah"
# Options:
#   - "strict": only count standalone "الله"
#   - "expanded": also count "بالله", "اللهم", "والله", "فلله", etc.
#   - "both": return both numbers
ALLAH_MODE = "both"

# Enable or disable debugging prints (minimal logs by default)
DEBUG = False

##############################################################################
# Regex Patterns
##############################################################################

# For Ism, we only want the standalone form "اسم" (excluding pronoun endings).
# The bullet point explicitly says: "[Also no plural forms, or those with pronoun endings]"
PATTERN_ISM = [r"\bاسم\b"]

# For Allah, define two sets of patterns:
ALLAH_PATTERNS_STRICT = [r"\bالله\b"]
ALLAH_PATTERNS_EXPANDED = [
    r"\bالله\b",     # standalone
    r"\bاللهم\b",    # vocative
    r"\bبالله\b",
    r"\bوالله\b",
    r"\bفلله\b",
    r"\bتالله\b"
    # Add more if needed
]

# Rahman & Rahim (standalone):
PATTERN_RAHMAN = [r"\bالرحمن\b"]
PATTERN_RAHIM  = [r"\bالرحيم\b"]

##############################################################################
# Functions
##############################################################################

def load_text_file(filename):
    """
    Load a text file and return its contents as a single string.
    """
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()

def preprocess_text(text):
    """
    Preprocess the Quranic text by optionally removing non-Arabic codepoints
    and/or stripping diacritics, depending on configuration flags.
    """
    # Remove all non-Arabic codepoints if configured:
    if REMOVE_NON_ARABIC:
        # Keep only Arabic letters (U+0600 to U+06FF) plus whitespace
        text = re.sub(r"[^\u0600-\u06FF\s]", "", text)

    # Strip diacritics if configured:
    if STRIP_DIACRITICS:
        # This range covers common Arabic diacritics, harakat, etc.
        # You can adapt if your text has other special diacritics.
        diacritics_regex = re.compile(r"[\u064B-\u0652\u0670\u06D6-\u06ED]")
        text = diacritics_regex.sub("", text)

    # Normalize spacing
    text = re.sub(r"\s+", " ", text).strip()

    return text

def count_occurrences_regex(text, patterns):
    """
    For a list of regex patterns, sum the total number of matches across them.
    """
    total = 0
    for pat in patterns:
        matches = re.findall(pat, text)
        match_count = len(matches)
        total += match_count
        if DEBUG:
            print(f"[DEBUG] Pattern '{pat}' found {match_count} matches.")
    return total

def count_allah(text):
    """
    Count 'Allah' based on the ALLAH_MODE configuration:
    - 'strict': only standalone 'الله'
    - 'expanded': includes other morphological variants
    - 'both': return a tuple (strict_count, expanded_count)
    """
    strict_count = count_occurrences_regex(text, ALLAH_PATTERNS_STRICT)
    expanded_count = count_occurrences_regex(text, ALLAH_PATTERNS_EXPANDED)

    if ALLAH_MODE == "strict":
        return strict_count
    elif ALLAH_MODE == "expanded":
        return expanded_count
    else:
        # "both"
        return (strict_count, expanded_count)

def verify_bismillah_letters():
    """
    Verify that the phrase 'بسم الله الرحمن الرحيم' has 19 letters after
    any configured stripping of diacritics, etc.
    """
    bismillah = "بسم الله الرحمن الرحيم"
    # Preprocess with the same logic, so we know how many letters remain
    processed_bismillah = preprocess_text(bismillah)
    letter_count = sum(1 for c in processed_bismillah if c.isalpha())
    return letter_count

def main():
    # 1) Load raw text of the Quran
    raw_text = load_text_file("quran-simple.txt")

    # 2) Preprocess
    prepped_text = preprocess_text(raw_text)

    # 3) Verify Bismillah letter count
    bismillah_letter_count = verify_bismillah_letters()
    print(f"Bismillah letter count (should be 19): {bismillah_letter_count}")

    # 4) Count occurrences of key words
    ism_count    = count_occurrences_regex(prepped_text, PATTERN_ISM)
    allah_count  = count_allah(prepped_text)  # can be an int or a tuple
    rahman_count = count_occurrences_regex(prepped_text, PATTERN_RAHMAN)
    rahim_count  = count_occurrences_regex(prepped_text, PATTERN_RAHIM)

    print("\n--- WORD COUNTS ---")
    print(f"Ism (اسم) [No pronoun forms]: {ism_count}")
    if isinstance(allah_count, tuple):
        strict, expanded = allah_count
        print(f"Allah (الله) [Strict]: {strict}")
        print(f"Allah (الله) [Expanded]: {expanded}")
    else:
        print(f"Allah (الله): {allah_count}")

    print(f"Rahman (الرحمن): {rahman_count}")
    print(f"Rahim (الرحيم): {rahim_count}")

    # 5) Display known bullet-point references
    # These are not derived from the text but known from the claim:
    #   - 114 chapters
    #   - 6346 verses
    #   - cross sum of 6346 = 19
    #   - etc.
    chapters = 114
    verses = 6346
    cross_sum_verses = sum(map(int, str(verses)))

    print("\n--- KNOWN BULLET DATA ---")
    print(f"Chapters: {chapters} (19×6)")
    print(f"Total Verses (with Bismillah): {verses} (19×334)")
    print(f"Cross-sum of 6346 = {cross_sum_verses} (should be 19)")
    print("Bismillah Count: 114 (19×6)")
    print("Missing Bismillah in Chapter 9, extra in 27 => 19 chapters apart")
    print("Surah 27:30 => 27 + 30 = 57 (19×3)")

    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()
