# -*- coding: utf-8 -*-
# This file is part of Shuup Onboarding
#
# Copyright (c) 2020 Christian Hess
#
# This source code is licensed under the OSL version 3.0 found in the
# LICENSE file in the root directory of this source tree.
import shuup.apps


class AppConfig(shuup.apps.AppConfig):
    name = "shuup_onboarding"
    label = "shuup_onboarding"
    required_installed_apps = [
        "shuup.admin"
    ]
    provides = {
        "admin_module": [
            "shuup_onboarding.admin.OnboardingAdmin"
        ]
    }
