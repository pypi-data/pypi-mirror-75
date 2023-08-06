# -*- coding: utf-8 -*-
# This file is part of Shuup Onboarding
#
# Copyright (c) 2020 Christian Hess
#
# This source code is licensed under the OSL version 3.0 found in the
# LICENSE file in the root directory of this source tree.
from django.utils.translation import ugettext_lazy as _
from shuup.admin.base import AdminModule, MenuEntry
from shuup.admin.utils.urls import admin_url


class OnboardingAdmin(AdminModule):
    name = _("Onboarding")
    breadcrumbs_menu_entry = MenuEntry(name, url="shuup_admin:onboarding.onboard")

    def get_urls(self):
        return [
            admin_url(
                r"^onboard/(?P<process_id>.+)/",
                "shuup_onboarding.admin.views.AdminOnboardingView",
                name="onboarding.onboard"
            )
        ]
