# -*- coding: utf-8 -*-
# This file is part of Shuup Onboarding
#
# Copyright (c) 2020 Christian Hess
#
# This source code is licensed under the OSL version 3.0 found in the
# LICENSE file in the root directory of this source tree.
from shuup.utils.importing import cached_load

from shuup_onboarding.base import AbstractOnboardingContext, Onboarding


class OnboardingContext(AbstractOnboardingContext):
    """
    Nothing to add
    """
    pass


class OnboardingProvider:
    """
    Default onboarding provider
    """
    @classmethod
    def get_onboarding(cls, process_id: str, onboarding_context: AbstractOnboardingContext) -> Onboarding:
        """
        Returns the onboarding process instance
        """
        return Onboarding(process_id, onboarding_context)


def get_onboarding_provider() -> OnboardingProvider:
    return cached_load("SHUUP_ONBOARDING_PROVIDER_SPEC")
