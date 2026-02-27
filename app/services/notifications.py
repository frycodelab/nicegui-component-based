"""
Custom notification service — renders fully styled HTML toasts.
Usage:
    from services.notifications import notify, notify_ongoing
    notify('Saved successfully', type='positive', title='Success')
    notify('Something went wrong', type='negative', title='Error')
    notify('Review your input', type='warning')
    notify('Server restarted', type='info')

    handle = await notify_ongoing('Processing…', title='Loading')
    await asyncio.sleep(3)
    handle.dismiss()
"""

import uuid
from nicegui import ui

# Global default position — change once here to affect all notifications.
# Accepted values: 'top-left' | 'top' | 'top-right' |
#                  'bottom-left' | 'bottom' | 'bottom-right'
DEFAULT_POSITION: str = 'bottom-right'

# CSS properties per position
_POS_CSS: dict[str, str] = {
    'top-left':     'top:24px;left:24px;align-items:flex-start;flex-direction:column;',
    'top':          'top:24px;left:50%;transform:translateX(-50%);align-items:center;flex-direction:column;',
    'top-right':    'top:24px;right:24px;align-items:flex-end;flex-direction:column;',
    'bottom-left':  'bottom:24px;left:24px;align-items:flex-start;flex-direction:column-reverse;',
    'bottom':       'bottom:24px;left:50%;transform:translateX(-50%);align-items:center;flex-direction:column-reverse;',
    'bottom-right': 'bottom:24px;right:24px;align-items:flex-end;flex-direction:column-reverse;',
}

# Tabler icon unicode characters per type
_ICONS = {
    'positive': '\uea67',   # circle-check
    'negative': '\uea6a',   # circle-x
    'warning':  '\uea06',   # alert-triangle
    'info':     '\ueac5',   # info-circle
    'default':  '\ueac5',   # info-circle
}

_TITLES = {
    'positive': 'Success',
    'negative': 'Error',
    'warning':  'Warning',
    'info':     'Info',
    'default':  'Notice',
}

_JS = """
(function() {{
  // ensure per-position container exists
  const containerId = 'toast-container-' + {pos_key!r};
  let container = document.getElementById(containerId);
  if (!container) {{
    container = document.createElement('div');
    container.id = containerId;
    container.style.cssText = 'position:fixed;z-index:99999;display:flex;gap:10px;pointer-events:none;{pos_css}';
    document.body.appendChild(container);
  }}

  const type     = {type!r};
  const icon     = {icon!r};
  const title    = {title!r};
  const message  = {message!r};
  const duration = {duration};

  const toast = document.createElement('div');
  toast.className = 'toast';

  toast.innerHTML = `
    <div class="toast-accent toast-accent-${{type}}"></div>
    <div class="toast-body">
      <span class="toast-icon toast-icon-${{type}}">${{icon}}</span>
      <div class="toast-content">
        <span class="toast-title">${{title}}</span>
        <span class="toast-message">${{message}}</span>
      </div>
      <button class="toast-close">&#xeb55;</button>
    </div>
    <div class="toast-progress toast-progress-${{type}}" style="width:100%"></div>
  `;

  container.appendChild(toast);

  // close button
  toast.querySelector('.toast-close').addEventListener('click', () => dismiss(toast));

  // progress bar shrink
  const bar = toast.querySelector('.toast-progress');
  bar.style.transition = `width ${{duration}}ms linear`;
  requestAnimationFrame(() => requestAnimationFrame(() => {{ bar.style.width = '0%'; }}));

  // auto dismiss
  const timer = setTimeout(() => dismiss(toast), duration);

  function dismiss(el) {{
    clearTimeout(timer);
    el.classList.add('toast-out');
    el.addEventListener('animationend', () => el.remove(), {{once: true}});
  }}
}})();
"""


def notify(
    message: str,
    type: str = 'default',
    title: str | None = None,
    duration: int = 4000,
    position: str | None = None,
) -> None:
    """Show a custom HTML notification toast."""
    t = type if type in _ICONS else 'default'
    pos = position or DEFAULT_POSITION
    pos = pos if pos in _POS_CSS else 'bottom-right'
    ui.run_javascript(_JS.format(
        type=t,
        icon=_ICONS[t],
        title=title if title is not None else _TITLES[t],
        message=message,
        duration=duration,
        pos_key=pos,
        pos_css=_POS_CSS[pos],
    ))


class _OngoingNotification:
    def __init__(self, toast_id: str) -> None:
        self._id = toast_id

    def dismiss(self) -> None:
        ui.run_javascript(f"""
        (function() {{
          const el = document.getElementById({self._id!r});
          if (el) {{
            el.classList.add('toast-out');
            el.addEventListener('animationend', () => el.remove(), {{once: true}});
          }}
        }})();
        """)


def notify_ongoing(message: str, title: str = 'Loading', position: str | None = None) -> _OngoingNotification:
    """Show a persistent spinner toast. Returns a handle with .dismiss()."""
    toast_id = f'toast-ongoing-{uuid.uuid4().hex[:8]}'
    pos = position or DEFAULT_POSITION
    pos = pos if pos in _POS_CSS else 'bottom-right'
    pos_css = _POS_CSS[pos]
    container_id = f'toast-container-{pos}'
    ui.run_javascript(f"""
    (function() {{
      let container = document.getElementById({container_id!r});
      if (!container) {{
        container = document.createElement('div');
        container.id = {container_id!r};
        container.style.cssText = 'position:fixed;z-index:99999;display:flex;gap:10px;pointer-events:none;{pos_css}';
        document.body.appendChild(container);
      }}
      const toast = document.createElement('div');
      toast.className = 'toast';
      toast.id = {toast_id!r};
      toast.innerHTML = `
        <div class="toast-accent toast-accent-default"></div>
        <div class="toast-body">
          <span class="toast-spinner"></span>
          <div class="toast-content">
            <span class="toast-title">{title}</span>
            <span class="toast-message">{message}</span>
          </div>
        </div>
      `;
      container.appendChild(toast);
    }})();
    """)
    return _OngoingNotification(toast_id)
