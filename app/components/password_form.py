"""Reusable password-change form with a live requirement checklist.

Shared by the forced change-password page and the account settings page.
Callers render the form inside their own layout and add a submit button that
reads :pyattr:`PasswordChangeForm.new_pw` once :meth:`is_valid` returns True.
"""

from __future__ import annotations

from typing import Callable

from nicegui import ui

from services import i18n
from services.user_service import MAX_PASSWORD_LENGTH, MIN_PASSWORD_LENGTH, password_requirements


class PasswordChangeForm:
    def __init__(
        self,
        *,
        new_label: str = 'New password',
        confirm_label: str = 'Confirm password',
        on_change: Callable[[], None] | None = None,
        on_submit: Callable[[], None] | None = None,
    ) -> None:
        self._on_change = on_change

        with ui.element('div').classes('w-full'):
            ui.label(new_label).classes('field-label')
            self.new_pw = ui.input(password=True, password_toggle_button=True) \
                .classes('w-full').props(f'outlined dense maxlength={MAX_PASSWORD_LENGTH}')

        with ui.element('div').classes('w-full'):
            ui.label(confirm_label).classes('field-label')
            self.confirm_pw = ui.input(password=True, password_toggle_button=True) \
                .classes('w-full').props(f'outlined dense maxlength={MAX_PASSWORD_LENGTH}')
            if on_submit is not None:
                self.confirm_pw.on('keydown.enter', lambda: on_submit())

        self._checklist = ui.refreshable(self._render_checklist)
        self._checklist()

        self.new_pw.on_value_change(self._handle_change)
        self.confirm_pw.on_value_change(self._handle_change)

    def _render_checklist(self) -> None:
        for key, ok in password_requirements(self.new_pw.value or ''):
            with ui.row().classes('items-center gap-2'):
                ui.icon('check_circle' if ok else 'radio_button_unchecked', size='1rem') \
                    .classes('text-positive' if ok else 'text-muted')
                label = ui.label().classes('text-xs ' + ('text-positive' if ok else 'text-muted'))
                if key == 'password.req.length':
                    i18n.bind_format(label, key, min=MIN_PASSWORD_LENGTH, max=MAX_PASSWORD_LENGTH)
                else:
                    i18n.bind(label, key)

        match = self.passwords_match()
        has_confirm = bool(self.confirm_pw.value)
        with ui.row().classes('items-center gap-2'):
            ui.icon('check_circle' if match else 'radio_button_unchecked', size='1rem') \
                .classes('text-positive' if match else 'text-muted')
            i18n.bind(
                ui.label().classes(
                    'text-xs ' + (
                        'text-positive' if match
                        else ('text-negative' if has_confirm else 'text-muted')
                    )
                ),
                'password.match',
            )

    def _handle_change(self) -> None:
        self._checklist.refresh()
        if self._on_change is not None:
            self._on_change()

    def requirements_met(self) -> bool:
        return all(ok for _, ok in password_requirements(self.new_pw.value or ''))

    def passwords_match(self) -> bool:
        return bool(self.confirm_pw.value) and self.new_pw.value == self.confirm_pw.value

    def is_valid(self) -> bool:
        return self.requirements_met() and self.passwords_match()

    def reset(self) -> None:
        self.new_pw.value = ''
        self.confirm_pw.value = ''
        self._checklist.refresh()
