#!/usr/bin/python3
#
# wajig - Linux Administration in One Place
#
# A command line tool for managing your linux system
#
# Copyright 1995-2020 (c) Graham.Williams@togaware.com All rights reserved.
#
# This file is part of wajig.
#
# License is GPLv3

from fuzzywuzzy import fuzz
from fuzzywuzzy import process as fuzzprocess

fuzz.ratio("install", "ubinstall")

choices = ["update", "upgrade", "install", "status"]
fuzzprocess.extractOne("isntall", choices)
fuzzprocess.extractOne("ugrade", choices)

# -----------------------------------------------------------------------
# Fuzzy match helper
# -----------------------------------------------------------------------

def yes_or_no(msg, *params, yes=True):
    """Query yes or no with message.

    Args:
        msg (str): Message to be printed out.
        yes (bool): Indicates whether the default answer is yes or no.
    """

    print(msg.format(*params) + (" [Y/n]?" if yes else " [y/N]?"), end=" ")
    choice = input().lower()

    answer = True if yes else False

    if yes and choice == "n":
        answer = False

    if not yes and choice == "y":
        answer = True

    return answer



def find_best_match(misspelled, candidates):
    """Find the best matched word with <misspelled> in <candidates>."""

    return fuzzprocess.extractOne(misspelled,
                                  candidates,
                                  scorer=fuzz.ratio)

def is_misspelled(score):
    """Check misspelled in terms of score."""

    return score >= 80 and score != 100  # 80 is an empirical value.


def get_misspelled_command(command, available_commands):

    matched, score = find_best_match(command, available_commands)
    if is_misspelled(score):
        yes = yes_or_no(
            "The command '{}' is not supported.  Did you mean '{}'",
            command,
            matched,
            yes=True,
        )
        if yes:
            print()
            return matched

    return None


def get_misspelled_pkg(model):

    model_completion_list = get_model_completion_list()
    if len(model_completion_list) != 0:
        matched, score = find_best_match(model, model_completion_list)
        if is_misspelled(score):
            yes = yes_or_no(
                "The package '{}' was not found.  Did you mean '{}'",
                model,
                matched,
                yes=True,
            )
            if yes:
                print()
                return matched

    return None


#-----------------------------------------------------------------------

get_misspelled_command("isntall", choices)
