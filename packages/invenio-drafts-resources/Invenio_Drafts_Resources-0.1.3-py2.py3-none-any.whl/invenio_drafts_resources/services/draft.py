# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Draft Service."""

import uuid

from invenio_db import db
from invenio_pidstore.models import PIDStatus
from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records_resources.services import MarshmallowDataValidator, \
    RecordService, RecordServiceConfig

from ..resource_units import IdentifiedRecordDraft
from .permissions import DraftPermissionPolicy
from .schemas import DraftMetadataSchemaJSONV1


class RecordDraftServiceConfig(RecordServiceConfig):
    """Draft Service configuration."""

    # Service configuration
    permission_policy_cls = DraftPermissionPolicy

    # RecordService configuration
    resource_unit_cls = IdentifiedRecordDraft

    # DraftService configuration.
    # WHY: We want to force user input choice here.
    draft_cls = None
    draft_data_validator = MarshmallowDataValidator(
        schema=DraftMetadataSchemaJSONV1
    )


class RecordDraftService(RecordService):
    """Draft Service interface."""

    RecordIdProviderV2.default_status_with_obj = PIDStatus.NEW
    default_config = RecordDraftServiceConfig

    # Over write resolver because default status is a class attr
    @property
    def resolver(self):
        """Factory for creating a draft resolver instance."""
        return self.config.resolver_cls(
            pid_type=self.config.resolver_pid_type,
            getter=self.record_cls.get_record,
            registered_only=False
        )

    # Draft attrs
    @property
    def draft_cls(self):
        """Factory for creating a record class."""
        return self.config.draft_cls

    @property
    def draft_data_validator(self):
        """Returns an instance of the draft data validator."""
        return self.config.draft_data_validator

    @property
    def draft_resolver(self):
        """Factory for creating a draft resolver instance."""
        return self.config.resolver_cls(
            pid_type=self.config.resolver_pid_type,
            getter=self.draft_cls.get_record,
            registered_only=False
        )

    def resolve_draft(self, id_):
        """Resolve a persistent identifier to a record draft."""
        return self.draft_resolver.resolve(id_)

    # High-level API
    # Inherits record read, search, create, delete and update

    def read_draft(self, id_, identity):
        """Retrieve a record."""
        pid, record = self.resolve_draft(id_)
        self.require_permission(identity, "read", record=record)
        # Todo: how do we deal with tombstone pages
        return self.resource_unit(pid=pid, record=record)

    def create(self, data, identity):
        """Create a draft for a new record.

        It does not eagerly create the associated record.
        """
        self.require_permission(identity, "create")
        validated_data = self.draft_data_validator.validate(data)
        rec_uuid = uuid.uuid4()
        pid = self.minter(record_uuid=rec_uuid, data=validated_data)
        draft = self.draft_cls.create(validated_data, id_=rec_uuid)

        db.session.commit()  # Persist DB
        if self.indexer:
            self.indexer.index(draft)

        return self.config.resource_unit_cls(pid=pid, record=draft)

    def edit(self, id_, data, identity):
        """Create a draft for an existing record.

        :param id_: record PID value.
        """
        pid, record = self.resolve(id_)
        self.require_permission(identity, "create")
        validated_data = self.draft_data_validator.validate(data)
        draft = self.draft_cls.create(validated_data, id_=record.id,
                                      fork_version_id=record.revision_id)
        db.session.commit()  # Persist DB
        if self.indexer:
            self.indexer.index(draft)

        return self.config.resource_unit_cls(pid=pid, record=draft)

    def publish(self, id_, identity):
        """Publish a draft."""
        self.require_permission(identity, "publish")
        # Get draft
        pid, draft = self.resolve_draft(id_=id_)
        # Validate and create record, register PID
        data = draft.dumps()
        # Validate against record schema
        validated_data = self.data_validator.validate(data)
        # Use same UUID
        record = self.record_cls.create(validated_data, id_=draft.id)
        pid.register()
        # Remove draft
        draft.delete()
        db.session.commit()  # Persist DB
        # Index the record
        if self.indexer:
            # FIXME: /invenio-drafts-resources/issues/21
            # self.indexer.delete(draft)
            self.indexer.index(record)

        return self.resource_unit(pid=pid, record=record)
