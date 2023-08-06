# -*- coding: utf-8 -*-
# This file is part of Shuup Onboarding
#
# Copyright (c) 2020 Christian Hess
#
# This source code is licensed under the OSL version 3.0 found in the
# LICENSE file in the root directory of this source tree.
from typing import Any

from django.contrib.sessions.backends.base import SessionBase

from shuup_onboarding.base import AbstractOnboardingStorage


class OnboardingSessionStorage(AbstractOnboardingStorage):
    """
    Class that represents a place where all the onboarding
    processing data is temporarily stored
    """
    _session = None   # type: SessionBase

    def __init__(self, process_id: str, session: SessionBase):
        self._session = session
        self._session_key = "onboarding_{}".format(process_id)
        if self._session_key not in self._session:
            self._session[self._session_key] = {}

    def __getitem__(self, key: str) -> Any:
        return self._session[self._session_key].get(key)

    def __setitem__(self, key: str, value):
        self._session[self._session_key][key] = value
        self._session.modified = True

    def __contains__(self, key):
        return key in self._session[self._session_key]

    def __delitem__(self, key):
        del self._session[self._session_key][key]
        self._session.modified = True

    def get(self, key, default=None):
        return self._session[self._session_key].get(key, default)

    def pop(self, key, default=None):
        val = self._session[self._session_key].pop(key, default)
        self._session.modified = True
        return val

    def keys(self):
        return self._session[self._session_key].keys()

    def values(self):
        return self._session[self._session_key].values()

    def items(self):
        return self._session[self._session_key].items()

    def clear(self):
        self._session[self._session_key] = {}
        self._session.modified = True
