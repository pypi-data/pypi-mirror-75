# -*- coding: utf-8 -*-

from .db import engine


def initialize_database():
    from .models import Base

    Base.metadata.create_all(engine)


def reset_database():
    from .models import Base

    Base.metadata.drop_all(engine)
    initialize_database()


def validate(input_events):
    failures = []

    keys = [
        "name",
        "url",
        "city",
        "state",
        "country",
        "cfp_open",
        "cfp_end_date",
        "start_date",
        "end_date",
        "source",
        "tags",
        "kind",
        "by",
    ]

    # check for duplicates
    ie_names = [ie["name"].replace(" ", "").lower() for ie in input_events]
    if sorted(list(set(ie_names))) != sorted(ie_names):
        failures.append("Duplicate events found")

    # check if keys exist
    for ie in input_events:
        if set(keys).difference(set(ie.keys())):
            failures.append("Required fields not found")
            break

    return failures
