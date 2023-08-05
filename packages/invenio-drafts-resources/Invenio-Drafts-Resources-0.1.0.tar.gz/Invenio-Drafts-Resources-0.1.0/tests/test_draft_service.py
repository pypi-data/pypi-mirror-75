# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio Drafts Resources module to create REST APIs"""

import pytest
from invenio_pidstore.models import PIDStatus
from sqlalchemy.orm.exc import NoResultFound


def test_create_draft_of_new_record(app, draft_service, input_draft,
                                    fake_identity):
    """Test draft creation of a non-existing record."""
    # Needs `app` context because of invenio_access/permissions.py#166
    identified_draft = draft_service.create(
        data=input_draft, identity=fake_identity
    )

    assert identified_draft.id

    for key, value in input_draft.items():
        assert identified_draft.record[key] == value


def test_create_draft_of_existing_record(app, draft_service, record_service,
                                         input_record, fake_identity):
    """Test draft creation of an existing record."""
    # Needs `app` context because of invenio_access/permissions.py#166
    # Create new record
    identified_record = record_service.create(
        data=input_record, identity=fake_identity
    )

    recid = identified_record.id
    assert recid

    for key, value in input_record.items():
        assert identified_record.record[key] == value

    # Create new draft of said record
    orig_title = input_record['title']
    input_record['title'] = "Edited title"
    identified_draft = draft_service.edit(
        data=input_record,
        identity=fake_identity,
        id_=recid
    )

    assert identified_draft.id == recid

    for key, value in input_record.items():
        assert identified_draft.record[key] == value

    # Check the actual record was not modified
    identified_record = draft_service.read(id_=recid, identity=fake_identity)

    assert identified_record.record['title'] == orig_title


def test_publish_draft_of_new_record(app, draft_service, input_record,
                                     fake_identity):
    """Test draft publication of a non-existing record.

    It has to first create said draft.
    """
    # Needs `app` context because of invenio_access/permissions.py#166
    # Crate the draft
    identified_draft = draft_service.create(
        data=input_record, identity=fake_identity
    )
    assert identified_draft.id
    for pid in identified_draft.pids:
        assert pid.status == PIDStatus.NEW

    for key, value in input_record.items():
        assert identified_draft.record[key] == value

    # Publish it
    identified_record = draft_service.publish(
        id_=identified_draft.id, identity=fake_identity
    )

    assert identified_record.id
    for pid in identified_record.pids:
        assert pid.status == PIDStatus.REGISTERED

    for key, value in input_record.items():
        assert identified_record.record[key] == value

    # Check draft deletion
    # TODO: Remove import when exception is properly handled
    with pytest.raises(NoResultFound):
        identified_draft = draft_service.read_draft(
            identified_draft.id, identity=fake_identity
        )

    # Test record exists
    identified_record = draft_service.read(
        identified_record.id, identity=fake_identity
    )

    assert identified_record.id
    for pid in identified_record.pids:
        assert pid.status == PIDStatus.REGISTERED

    for key, value in input_record.items():
        assert identified_record.record[key] == value
