# -*- coding: utf-8 -*-
# This file is part of Shuup Onboarding
#
# Copyright (c) 2020 Christian Hess
#
# This source code is licensed under the OSL version 3.0 found in the
# LICENSE file in the root directory of this source tree.
from django.core.urlresolvers import reverse
from django.http.request import QueryDict
from django.http.response import HttpResponseRedirect
from django.views.generic import FormView
from shuup.admin.shop_provider import get_shop
from shuup.admin.supplier_provider import get_supplier

from shuup_onboarding.base import Onboarding
from shuup_onboarding.onboard import get_onboarding_provider, OnboardingContext
from shuup_onboarding.storage import OnboardingSessionStorage


class AdminOnboardingView(FormView):
    form_class = None
    template_name = "shuup_onboarding/admin/onboard.jinja"

    def dispatch(self, request, *args, **kwargs):
        onboarding_process_id = self.kwargs["process_id"]
        storage = OnboardingSessionStorage(onboarding_process_id, request.session)
        onboarding_context = OnboardingContext(
            storage=storage,
            shop=get_shop(request),
            supplier=get_supplier(request),
            user=request.user
        )
        self.onboarding = get_onboarding_provider().get_onboarding(
            onboarding_process_id,
            onboarding_context
        )   # type: Onboarding
        self.current_step = self.onboarding.get_current_step()

        if not self.current_step:
            return HttpResponseRedirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request"] = self.request
        context["onboarding"] = self.onboarding
        context["onboard_step"] = self.current_step
        return context

    def get_form(self, form_class=None):
        if self.current_step:
            return self.current_step.get_form(**self.get_form_kwargs())

    def form_valid(self, form):
        self.current_step.save(form)

    def get_success_url(self):
        success_url = self.onboarding.get_success_url()
        if isinstance(success_url, str):
            return reverse(success_url)
        return reverse(success_url[0], kwargs=success_url[1])

    def _check_next_step(self, request, *args, **kwargs):
        # no more steps, it means we are done with this onboarding
        self.current_step = self.onboarding.get_current_step()

        if not self.current_step:
            return HttpResponseRedirect(self.get_success_url())

        # there are more steps
        request.POST = QueryDict()
        request.method = "GET"
        return self.get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # the current step allows skipping and there is a skip flag in POST, call skip for it
        if self.current_step.can_skip() and request.POST.get("skip"):
            self.current_step.skip()
            return self._check_next_step(request, *args, **kwargs)

        if request.POST.get("previous"):
            previous_step = self.onboarding.get_previous_step()
            if previous_step:
                previous_step.undo()
            return self._check_next_step(request, *args, **kwargs)

        form = self.get_form()
        if form.is_valid():
            self.form_valid(form)
            return self._check_next_step(request, *args, **kwargs)

        return self.form_invalid(form)
