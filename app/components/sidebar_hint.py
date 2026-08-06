"""Sidebar hint: design-system tooltip that names a collapsed nav item.

When the sidebar shrinks to icon-only width the text labels are hidden, so each
icon exposes a right-anchored ``.tooltip`` on hover that reveals its destination
path. The hint is unused while the sidebar is expanded because the label shows.
"""

from nicegui import ui
from services import i18n


def sidebar_hint(text: str, *, translate: bool = True) -> ui.tooltip:
    """Attach a right-side design-system tooltip to the current nav link.

    Call inside a nav link's element scope. Pass a translation key (``translate``
    on) or a literal string (``translate`` off). Returns the tooltip so the shell
    can toggle its visibility with the sidebar's collapsed state.
    """
    tip = (ui.tooltip(i18n.t(text) if translate else text)
           .classes('tooltip sidebar-hint')
           .props('anchor="center right" self="center left" :offset="[16, 0]" '
                  'transition-show="jump-right" transition-hide="jump-left"'))
    if translate:
        i18n.bind(tip, text)
    return tip
