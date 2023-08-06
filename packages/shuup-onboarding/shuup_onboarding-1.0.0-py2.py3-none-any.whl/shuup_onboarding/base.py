# -*- coding: utf-8 -*-
# This file is part of Shuup Onboarding
#
# Copyright (c) 2020 Christian Hess
#
# This source code is licensed under the OSL version 3.0 found in the
# LICENSE file in the root directory of this source tree.
from typing import (
    Any, Dict, Iterable, List, Optional, Tuple, TYPE_CHECKING, Union
)

from django import forms
from django.conf import settings
from shuup.apps.provides import get_provide_objects

if TYPE_CHECKING:
    from shuup.core.models import Shop, Supplier
    from django.contrib.auth.models import AbstractUser


class AbstractOnboardingStorage:
    """
    Abstract class that represents a place where all the onboarding
    processing data is temporarily stored
    """
    def __getitem__(self, key: str) -> Any:
        raise NotImplementedError()

    def __setitem__(self, key: str, value):
        raise NotImplementedError()

    def __contains__(self, key):
        raise NotImplementedError()

    def __delitem__(self, key):
        raise NotImplementedError()

    def get(self, key, default=None):
        raise NotImplementedError()

    def pop(self, key, default=None):
        raise NotImplementedError()

    def setdefault(self, key, value):
        raise NotImplementedError()

    def has_key(self, key):
        raise NotImplementedError()

    def keys(self):
        raise NotImplementedError()

    def values(self):
        raise NotImplementedError()

    def items(self):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()


class AbstractOnboardingContext:
    storage = None      # type: AbstractOnboardingStorage
    shop = None         # type: Optional[Shop]
    supplier = None     # type: Optional[Supplier]
    user = None         # type: Optional[AbstractUser]

    def __init__(self, storage: AbstractOnboardingStorage, shop: 'Shop' = None, supplier: 'Supplier' = None,
                 user: 'AbstractUser' = None):
        self.storage = storage
        self.shop = shop
        self.supplier = supplier
        self.user = user


class OnboardingStep:
    identifier = ""         # type: str
    title = ""              # type: str
    description = ""        # type: Optional[str]
    icon = ""               # type: Optional[str]
    priority = 0            # type: int
    context = None          # type: AbstractOnboardingContext
    template_name = ""      # type: str
    js_template_name = ""   # type: str

    def __init__(self, context: AbstractOnboardingContext):
        self.context = context

    def skip(self):
        """
        Behave accordingly when user clicked to skip this step
        """
        raise NotImplementedError()

    def undo(self):
        """
        Remove the status of done and skipped and present this step again
        """
        raise NotImplementedError()

    def can_skip(self) -> bool:
        """
        Returns whether this step can be skipped.

        The user can skip some steps. Usually good for optional steps.
        """
        raise NotImplementedError()

    def was_skipped(self) -> bool:
        """
        Returns whether this panel was ever skipped before.

        It should be used when `can_skip` returns True,
        to determine whether this step should be shown
        again after the panel was skipped once.
        """
        raise NotImplementedError()

    def is_done(self) -> bool:
        """
        Returns whether this step is done.

        It is done when the step is fully completed.
        """
        raise NotImplementedError()

    def is_visible(self) -> bool:
        """
        Returns whether this step is visible.

        If False is returned, it won't be on the steps list.
        """
        raise NotImplementedError()

    def get_form(self, **kwargs) -> forms.Form:
        """
        Returns a form to configure the step.
        """
        raise NotImplementedError()

    def get_render_context(self) -> Dict:
        """
        Returns a context dictionary to access in the template.

        To have access to this context, use `step_context` variable in the template.
        """
        return {}

    def save(self, form):
        """
        Save the data form the form as it is valid.
        """
        raise NotImplementedError()


class Onboarding:
    _steps = []         # type: Iterable[OnboardingStep]
    _process_id = ""    # type: str
    _context = None     # type: AbstractOnboardingContext

    def __init__(self, process_id: str, onboarding_context: AbstractOnboardingContext):
        """
        Create a new onboarding process.
        The onboarding will load all steps for the given `process_id`.
        """
        self._process_id = process_id
        self._context = onboarding_context
        self._load_steps()

    def _load_steps(self):
        """
        Load all steps into memory
        """
        provides_key = "onboarding_process:{}".format(self._process_id)
        onboarding_steps = get_provide_objects(provides_key)
        steps = []

        # instantiate the steps
        for onboarding_step in onboarding_steps:
            steps.append(onboarding_step(self._context))

        self._steps = sorted(steps, key=lambda step: step.priority, reverse=True)   # type: Iterable[OnboardingStep]

    def get_pending_steps(self) -> List[OnboardingStep]:
        """
        Returns an iterable of the pending steps
        """
        pending = []
        for step in self._steps:
            if not step.is_visible():
                continue

            # step is done
            if step.is_done():
                continue

            # step can be skipped and was already skipped before, so skip it
            if step.can_skip() and step.was_skipped():
                continue

            pending.append(step)

        return pending

    def get_all_visible_steps(self) -> List[OnboardingStep]:
        """
        Retuns all visible steps
        """
        return [step for step in self._steps if step.is_visible()]

    def get_current_step(self) -> Optional[OnboardingStep]:
        """
        Returns the current step
        """
        pending_steps = self.get_pending_steps()
        if pending_steps:
            return pending_steps[0]

    def get_next_step(self) -> Optional[OnboardingStep]:
        """
        Returns the next step
        """
        current_step = self.get_current_step()
        if current_step:
            visible_steps = self.get_all_visible_steps()
            step_index = visible_steps.index(current_step)
            next_index = step_index + 1
            if next_index < len(visible_steps):
                return visible_steps[next_index]

    def get_previous_step(self) -> Optional[OnboardingStep]:
        """
        Returns the previous step
        """
        current_step = self.get_current_step()
        if current_step:
            visible_steps = self.get_all_visible_steps()
            step_index = visible_steps.index(current_step)
            prev_index = step_index - 1
            if prev_index >= 0:
                return visible_steps[prev_index]

    def get_success_url(self) -> Union[str, Tuple[str, Dict]]:
        """
        Returns the success url for reverse.

        It can return a tuple of url name and a dictionary
        when the url has kwargs to pass.

        Examples:

            `return "myapp.myurl"`
            or
            `return "myapp.myobject", {pk: object.id}`

        """
        return settings.SHUUP_ONBOARDING_DEFAULT_SUCCESS_URL

    def finish(self):
        """
        All done, clear the onboarding storage
        """
        self._context.storage.clear()
