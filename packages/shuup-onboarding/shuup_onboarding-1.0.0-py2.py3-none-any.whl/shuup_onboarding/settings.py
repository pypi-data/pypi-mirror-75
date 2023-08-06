# -*- coding: utf-8 -*-
# This file is part of Shuup Onboarding
#
# Copyright (c) 2020 Christian Hess
#
# This source code is licensed under the OSL version 3.0 found in the
# LICENSE file in the root directory of this source tree.

#: Spec function that returns a class to privde the onboarding class
#: for a given process and context
#:
SHUUP_ONBOARDING_PROVIDER_SPEC = "shuup_onboarding.onboard.OnboardingProvider"

#: Defines the default success URL to redirect the user after the admin onboarding
#:
SHUUP_ONBOARDING_DEFAULT_SUCCESS_URL = "shuup_admin:dashboard"


#: Defines an extra list of views to be ignored by the middleware
#: Example:
#:
#:  SHUUP_ONBOARDING_MIDDLEWARE_IGNORE_VIEWS = ["shuup_admin:myapp.my_url"]
#:
SHUUP_ONBOARDING_MIDDLEWARE_IGNORE_VIEWS = []
