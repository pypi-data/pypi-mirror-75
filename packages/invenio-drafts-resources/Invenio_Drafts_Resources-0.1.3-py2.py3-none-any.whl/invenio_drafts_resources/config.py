# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
# Copyright (C) 2020 Northwestern University.
#
# Invenio-Drafts-Resources is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.

"""Invenio-Drafts-Resources Configuration."""

DRAFTS_RESOURCES_LINK_URLS = {
    'record': '{base}/records/{pid}',
    'records': '{base}/records/',
    'draft': '{base}/records/{pid}/draft/',
}
