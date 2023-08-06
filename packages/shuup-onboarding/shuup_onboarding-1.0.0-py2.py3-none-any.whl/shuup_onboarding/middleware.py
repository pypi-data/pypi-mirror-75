# -*- coding: utf-8 -*-
# This file is part of Shuup Onboarding
#
# Copyright (c) 2020 Christian Hess
#
# This source code is licensed under the OSL version 3.0 found in the
# LICENSE file in the root directory of this source tree.
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from shuup.admin.shop_provider import get_shop
from shuup.admin.supplier_provider import get_supplier
from shuup.apps.provides import get_identifier_to_object_map
from django.conf import settings

from shuup_onboarding.onboard import get_onboarding_provider, OnboardingContext
from shuup_onboarding.storage import OnboardingSessionStorage


class BaseAdminOnboardingMiddleware(MiddlewareMixin):
    """
    Base middleware that checks for a single onboarding process.

    If the onboarding has pending steps, then redirect the user to
    complete the missing steps.
    """

    # The process ID that this middleware is going to track
    onboarding_process_id = ""  # type: str

    allowed_views = [
        "shuup_admin:login",
        "shuup_admin:logout",
        "shuup_admin:home",
        "shuup_admin:tour",
        "shuup_admin:wizard",
        "shuup_admin:logout",
        "shuup_admin:menu",
        "shuup_admin:menu_toggle",
        "shuup_admin:js-catalog",
        "shuup_admin:set-language",
        "shuup_admin:stop-impersonating-staff",
        "shuup_admin:recover_password",
        "shuup_admin:request_password",
        "shuup_admin:onboarding.onboard",
    ]

    def process_view(self, request, view_func, view_args, view_kwargs):
        # have you forgot to customize this?
        assert self.onboarding_process_id

        # user not authenticated
        if not request.user.is_authenticated():
            return

        # not admin view
        if not request.resolver_match.view_name or request.resolver_match.app_name != "shuup_admin":
            return

        # ignore this view
        if request.resolver_match.view_name in self.allowed_views:
            return

        # ignore this view too
        if request.resolver_match.view_name in settings.SHUUP_ONBOARDING_MIDDLEWARE_IGNORE_VIEWS:
            return

        storage = OnboardingSessionStorage(self.onboarding_process_id, request.session)
        onboarding_context = OnboardingContext(
            storage=storage,
            shop=get_shop(request),
            supplier=get_supplier(request),
            user=request.user
        )
        onboarding = get_onboarding_provider().get_onboarding(self.onboarding_process_id, onboarding_context)

        # steps missing, redirect to the onboard process
        if onboarding.get_current_step():
            return HttpResponseRedirect(
                reverse("shuup_admin:onboarding.onboard", kwargs=dict(process_id=self.onboarding_process_id))
            )
