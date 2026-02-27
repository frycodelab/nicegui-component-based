"""Design System page — live reference for every CSS component and utility token."""

import asyncio
from nicegui import ui, app
from services.notifications import notify, notify_ongoing

def content() -> None:

    # ── Page header ──────────────────────────────────────────────
    ui.label('Design System').classes('page-title mb-2')
    ui.label('Every CSS component & utility token at a glance.').classes('text-sm text-muted mb-4')
    ui.element('div').classes('divider')

    # ── 1. TYPOGRAPHY ────────────────────────────────────────────
    ui.label('1 · Typography').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        ui.label('LABEL TEXT (label-text)').classes('label-text mb-3')
        for cls in ['text-xs', 'text-sm', 'text-base', 'text-lg', 'text-xl', 'text-2xl']:
            ui.label(f'.{cls} — The quick brown fox').classes(f'{cls} mb-1')
        ui.element('div').classes('divider')
        for cls in ['font-normal', 'font-medium', 'font-semi', 'font-bold']:
            ui.label(f'.{cls} — The quick brown fox').classes(f'{cls} mb-1')
        ui.element('div').classes('divider')
        with ui.row().classes('gap-3 flex-wrap'):
            for cls in ['text-muted', 'text-faint', 'text-success', 'text-warning', 'text-danger', 'text-info']:
                ui.label(f'.{cls}').classes(cls)

    # ── 2. BUTTONS ───────────────────────────────────────────────
    ui.label('2 · Buttons').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        ui.label('VARIANTS').classes('label-text mb-3')
        with ui.row().classes('gap-2 flex-wrap mb-3'):
            for variant in ['button-primary', 'button-secondary', 'button-outline', 'button-ghost', 'button-danger', 'button-success']:
                ui.button(variant.replace('button-', '').capitalize(), color='white').props('flat no-caps').classes(f'button {variant}')
        ui.element('div').classes('divider')
        ui.label('SIZES').classes('label-text mb-3')
        with ui.row().classes('gap-2 items-center flex-wrap mb-3'):
            ui.button('Small', color='white').props('flat no-caps').classes('button button-primary button-sm')
            ui.button('Default', color='white').props('flat no-caps').classes('button button-primary')
            ui.button('Large', color='white').props('flat no-caps').classes('button button-primary button-lg')
        ui.element('div').classes('divider')
        ui.label('DISABLED').classes('label-text mb-3')
        with ui.row().classes('gap-2 flex-wrap'):
            ui.button('Disabled Primary', color='white').props('flat no-caps').classes('button button-primary disabled')
            ui.button('Disabled Outline', color='white').props('flat no-caps').classes('button button-outline disabled')

    # ── 3. CARDS & PANELS ────────────────────────────────────────
    ui.label('3 · Cards & Panels').classes('section-title mt-4 mb-2')
    with ui.row().classes('gap-4 flex-wrap mb-4'):
        with ui.element('div').classes('card').style('min-width:260px'):
            ui.label('Card Title').classes('card-title')
            ui.label('Supporting description goes here, in muted text.').classes('card-description')
            ui.label('Body content area — anything can live here.').classes('text-sm')
            with ui.element('div').classes('card-footer'):
                ui.button('Action', color='white').props('flat no-caps').classes('button button-primary button-sm')
                ui.button('Cancel', color='white').props('flat no-caps').classes('button button-outline button-sm')
        with ui.element('div').classes('panel').style('min-width:260px'):
            ui.label('Panel').classes('section-title mb-1')
            ui.label('Lighter faint-bg panel for secondary info.').classes('text-sm text-muted')

    # ── 4. BADGES ────────────────────────────────────────────────
    ui.label('4 · Badges').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        with ui.row().classes('gap-2 flex-wrap'):
            for variant in ['badge-default', 'badge-primary', 'badge-success', 'badge-warning', 'badge-danger', 'badge-info', 'badge-outline']:
                ui.label(variant.replace('badge-', '').capitalize()).classes(f'badge {variant}')

    # ── 5. STATUS DOTS ───────────────────────────────────────────
    ui.label('5 · Status Dots').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        with ui.row().classes('gap-4 flex-wrap items-center'):
            for state in ['success', 'warning', 'danger', 'info', 'muted']:
                with ui.row().classes('items-center gap-2'):
                    ui.element('span').classes(f'status-dot {state}')
                    ui.label(state.capitalize()).classes('text-sm')

    # ── 6. ALERTS ────────────────────────────────────────────────
    ui.label('6 · Alerts').classes('section-title mt-4 mb-2')
    with ui.column().classes('gap-2 w-full mb-4'):
        ui.label('Default alert — informational neutral message.').classes('alert')
        ui.label('Success — Operation completed successfully.').classes('alert alert-success')
        ui.label('Warning — Please review before continuing.').classes('alert alert-warning')
        ui.label('Danger — An error occurred, action required.').classes('alert alert-danger')
        ui.label('Info — Here is something you should know.').classes('alert alert-info')

    # ── 7. NOTIFICATIONS ─────────────────────────────────────────
    ui.label('7 · Notifications').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        ui.label('TYPES').classes('label-text mb-3')
        with ui.row().classes('gap-2 flex-wrap mb-3'):
            ui.button('Default',  color='white', on_click=lambda: notify('Default notification message.')).props('flat no-caps').classes('button button-secondary')
            ui.button('Positive', color='white', on_click=lambda: notify('Operation completed successfully.', type='positive')).props('flat no-caps').classes('button button-success')
            ui.button('Negative', color='white', on_click=lambda: notify('An error occurred, action required.', type='negative')).props('flat no-caps').classes('button button-danger')
            ui.button('Warning',  color='white', on_click=lambda: notify('Please review before continuing.', type='warning')).props('flat no-caps').classes('button button-outline')
            ui.button('Info',     color='white', on_click=lambda: notify('Here is something you should know.', type='info')).props('flat no-caps').classes('button button-outline')
            async def show_ongoing():
                n = notify_ongoing('Loading, please wait…', title='Ongoing')
                await asyncio.sleep(3)
                n.dismiss()
            ui.button('Ongoing', color='white', on_click=show_ongoing).props('flat no-caps').classes('button button-outline')
        ui.element('div').classes('divider')
        ui.label('POSITIONS').classes('label-text mb-3')
        with ui.row().classes('gap-2 flex-wrap mb-3'):
            for pos in ['top-left', 'top', 'top-right', 'bottom-left', 'bottom', 'bottom-right']:
                ui.button(pos, color='white', on_click=lambda p=pos: notify(f'Position: {p}', type='info', position=p)).props('flat no-caps').classes('button button-outline button-sm')
        ui.element('div').classes('divider')

    # ── 8. INPUTS ────────────────────────────────────────────────
    ui.label('8 · Inputs').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        ui.label('DEFAULT').classes('label-text mb-3')
        with ui.column().classes('gap-3 w-full'):
            with ui.element('div').classes('w-full'):
                ui.label('Label').classes('field-label')
                ui.input(placeholder='Default input…').classes('w-full').props('outlined')
                ui.label('Helper hint text').classes('field-hint')
            with ui.element('div').classes('w-full'):
                ui.label('Password').classes('field-label')
                ui.input(placeholder='Enter password…', password=True, password_toggle_button=True).classes('w-full').props('outlined')
            with ui.element('div').classes('w-full'):
                ui.label('Disabled').classes('field-label')
                ui.input(value='Cannot edit this', placeholder='Disabled…').classes('w-full').props('outlined disable')
            with ui.element('div').classes('w-full'):
                ui.label('Error state').classes('field-label')
                ui.input(value='bad@value', placeholder='Error…').classes('w-full input-error').props('outlined')
                ui.label('This field is required.').classes('field-error')

    # ── 9. INPUT GROUPS ──────────────────────────────────────────
    ui.label('9 · Input Groups').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        with ui.column().classes('gap-3 w-full'):
            ui.label('ICON PREFIX').classes('label-text mb-1')
            search = ui.input(placeholder='Search…').classes('w-full').props('outlined rounded clearable')
            search.add_slot('prepend', '<q-icon name="search" />')

            ui.label('ICON SUFFIX').classes('label-text mb-1')
            email = ui.input(placeholder='Email address…').classes('w-full').props('outlined')
            email.add_slot('append', '<q-icon name="email" />')

            ui.label('TEXT PREFIX + SUFFIX').classes('label-text mb-1')
            with ui.input(placeholder='0.00').classes('w-full').props('outlined') as amount:
                amount.add_slot('prepend', '<span style="padding:0 8px;color:var(--muted-fg);font-size:0.9rem">€</span>')
                amount.add_slot('append',  '<span style="padding:0 8px;color:var(--muted-fg);font-size:0.9rem">EUR</span>')

    # ── 10. SELECT ────────────────────────────────────────────────
    ui.label('10 · Select').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        with ui.column().classes('gap-3 w-full'):
            ui.label('SINGLE SELECT').classes('label-text mb-1')
            ui.select(['Option A', 'Option B', 'Option C'], value='Option A').classes('w-full').props('outlined')
            ui.label('MULTI SELECT').classes('label-text mb-1')
            ui.select(['Red', 'Green', 'Blue', 'Yellow'], multiple=True, value=['Red', 'Blue']).classes('w-full').props('outlined use-chips')

    # ── 11. PROGRESS ─────────────────────────────────────────────
    ui.label('11 · Progress').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        ui.label('LINEAR').classes('label-text mb-3')
        with ui.column().classes('gap-3 w-full mb-3'):
            with ui.element('div').classes('progress-wrap'):
                ui.label('Default (45%)').classes('text-xs text-muted mb-1')
                ui.linear_progress(value=0.45, show_value=False).classes('progress-bar')
            with ui.element('div').classes('progress-wrap'):
                ui.label('Success (78%)').classes('text-xs text-muted mb-1')
                ui.linear_progress(value=0.78, show_value=False).classes('progress-bar progress-success')
            with ui.element('div').classes('progress-wrap'):
                ui.label('Warning (55%)').classes('text-xs text-muted mb-1')
                ui.linear_progress(value=0.55, show_value=False).classes('progress-bar progress-warning')
            with ui.element('div').classes('progress-wrap'):
                ui.label('Danger (30%)').classes('text-xs text-muted mb-1')
                ui.linear_progress(value=0.30, show_value=False).classes('progress-bar progress-danger')
            with ui.element('div').classes('progress-wrap'):
                ui.label('Indeterminate').classes('text-xs text-muted mb-1')
                ui.linear_progress(show_value=False).props('indeterminate').classes('progress-bar')
        ui.element('div').classes('divider')
        ui.label('CIRCULAR').classes('label-text mb-3')
        with ui.row().classes('gap-4 items-center flex-wrap'):
            ui.circular_progress(value=45,  min=0, max=100, show_value=True).props('color=primary size=64px track-color=grey-3')
            ui.circular_progress(value=78,  min=0, max=100, show_value=True).props('color=positive size=64px track-color=grey-3')
            ui.circular_progress(value=30,  min=0, max=100, show_value=True).props('color=negative size=64px track-color=grey-3')
            ui.circular_progress(value=100, min=0, max=100, show_value=True).props('indeterminate color=primary size=64px track-color=grey-3')

    # ── 12. DIALOG ───────────────────────────────────────────────
    ui.label('12 · Dialog').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        with ui.row().classes('gap-2 flex-wrap'):
            with ui.dialog() as info_dialog, ui.card().classes('dialog-card'):
                ui.label('Confirm action').classes('dialog-title')
                ui.label('Are you sure you want to proceed? This cannot be undone.').classes('dialog-body')
                with ui.element('div').classes('dialog-footer'):
                    ui.button('Cancel', on_click=info_dialog.close, color='white').props('flat no-caps').classes('button button-outline button-sm')
                    ui.button('Confirm', on_click=info_dialog.close, color='white').props('flat no-caps').classes('button button-primary button-sm')
            ui.button('Open Dialog', on_click=info_dialog.open, color='white').props('flat no-caps').classes('button button-secondary')

            with ui.dialog() as danger_dialog, ui.card().classes('dialog-card'):
                ui.label('Delete item').classes('dialog-title text-danger')
                ui.label('This will permanently delete the record. Continue?').classes('dialog-body')
                with ui.element('div').classes('dialog-footer'):
                    ui.button('Cancel', on_click=danger_dialog.close, color='white').props('flat no-caps').classes('button button-outline button-sm')
                    ui.button('Delete', on_click=danger_dialog.close, color='white').props('flat no-caps').classes('button button-danger button-sm')
            ui.button('Danger Dialog', on_click=danger_dialog.open, color='white').props('flat no-caps').classes('button button-danger')

    # ── 13. TOOLTIP / POPOVER ────────────────────────────────────
    ui.label('13 · Tooltip & Popover').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        ui.label('TOOLTIPS').classes('label-text mb-3')
        with ui.row().classes('gap-3 flex-wrap mb-4'):
            with ui.button('Hover me', color='white').props('flat no-caps').classes('button button-secondary'):
                ui.tooltip('Simple tooltip text').classes('tooltip')
            with ui.button('Top', color='white').props('flat no-caps').classes('button button-outline'):
                ui.tooltip('Appears on top').props('anchor="top middle" self="bottom middle"').classes('tooltip')
            with ui.button('Danger tip', color='white').props('flat no-caps').classes('button button-danger'):
                ui.tooltip('⚠ Destructive action!').classes('tooltip tooltip-danger')
        ui.element('div').classes('divider')
        ui.label('POPOVER (Menu)').classes('label-text mb-3')
        with ui.button('Open Popover', icon='more_vert', color='white').props('flat no-caps').classes('button button-outline'):
            with ui.menu().classes('popover').props('anchor="bottom left" self="top left" no-refocus no-focus'):
                with ui.menu_item('Edit', on_click=lambda: notify('Edit clicked', type='info')):
                    ui.icon('edit').classes('account-icon')
                with ui.menu_item('Duplicate', on_click=lambda: notify('Item duplicated', type='positive')):
                    ui.icon('content_copy').classes('account-icon')
                ui.separator()
                with ui.menu_item('Delete', on_click=lambda: notify('Item deleted', type='negative')):
                    ui.icon('delete').classes('account-icon text-danger')

    # ── 14. TOGGLES, CHECKBOXES, RADIO ───────────────────────────
    ui.label('14 · Toggles, Checkboxes & Radio').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        with ui.row().classes('gap-8 flex-wrap'):
            with ui.column().classes('gap-2'):
                ui.label('CHECKBOX').classes('label-text mb-1')
                ui.checkbox('Unchecked')
                ui.checkbox('Checked', value=True)
                ui.checkbox('Disabled').props('disable')
            with ui.column().classes('gap-2'):
                ui.label('TOGGLE').classes('label-text mb-1')
                ui.toggle(['Off', 'On'], value='Off')
                ui.switch('Switch off')
                ui.switch('Switch on', value=True)
            with ui.column().classes('gap-2'):
                ui.label('RADIO').classes('label-text mb-1')
                ui.radio(['Option A', 'Option B', 'Option C'], value='Option A')

    # ── 15. TABS ─────────────────────────────────────────────────
    ui.label('15 · Tabs').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        with ui.tabs().classes('tabs-bar') as tabs:
            tab_overview  = ui.tab('Overview',  icon='dashboard')
            tab_analytics = ui.tab('Analytics', icon='bar_chart')
            tab_settings  = ui.tab('Settings',  icon='settings')
        with ui.tab_panels(tabs, value=tab_overview).classes('w-full mt-3'):
            with ui.tab_panel(tab_overview):
                ui.label('Overview panel content — dashboard widgets would live here.').classes('text-sm text-muted')
            with ui.tab_panel(tab_analytics):
                ui.label('Analytics panel — charts and KPIs go here.').classes('text-sm text-muted')
            with ui.tab_panel(tab_settings):
                ui.label('Settings panel — configuration options here.').classes('text-sm text-muted')

    # ── 16. DATA TABLE ───────────────────────────────────────────
    ui.label('16 · Data Table').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        rows = [
            {'id': 'ORD-001', 'customer': 'Acme Corp',    'status': 'success', 'label': 'Shipped',    'amount': '€ 1,240.00'},
            {'id': 'ORD-002', 'customer': 'Beta GmbH',    'status': 'warning', 'label': 'Pending',    'amount': '€   380.50'},
            {'id': 'ORD-003', 'customer': 'Gamma Ltd',    'status': 'danger',  'label': 'Cancelled',  'amount': '€   720.00'},
            {'id': 'ORD-004', 'customer': 'Delta AG',     'status': 'info',    'label': 'Processing', 'amount': '€ 2,100.00'},
        ]
        with ui.element('table').classes('data-table w-full'):
            with ui.element('thead'):
                with ui.element('tr'):
                    for col in ['Order ID', 'Customer', 'Status', 'Amount']:
                        with ui.element('th'):
                            ui.label(col)
            with ui.element('tbody'):
                for row in rows:
                    with ui.element('tr'):
                        with ui.element('td'):
                            ui.label(row['id'])
                        with ui.element('td'):
                            ui.label(row['customer'])
                        with ui.element('td'):
                            ui.label(row['label']).classes(f'badge badge-{row["status"]}')
                        with ui.element('td'):
                            ui.label(row['amount'])

    # ── 17. TEXTAREA ─────────────────────────────────────────────
    ui.label('17 · Textarea').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        with ui.column().classes('gap-3 w-full'):
            with ui.element('div').classes('w-full'):
                ui.label('Default').classes('field-label')
                ui.textarea(placeholder='Write something…').classes('w-full').props('outlined rows=3')
            with ui.element('div').classes('w-full'):
                ui.label('Disabled').classes('field-label')
                ui.textarea(value='Cannot edit this content.').classes('w-full').props('outlined rows=3 disable')
            with ui.element('div').classes('w-full'):
                ui.label('Auto-grow').classes('field-label')
                ui.textarea(placeholder='Grows as you type…').classes('w-full').props('outlined autogrow')

    # ── 18. DATE & TIME PICKERS ──────────────────────────────────
    ui.label('18 · Date & Time Pickers').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        with ui.row().classes('gap-6 flex-wrap'):
            with ui.column().classes('gap-2'):
                ui.label('DATE').classes('label-text mb-1')
                ui.date(value='2026-02-26').classes('picker-card').props('today-btn')
            with ui.column().classes('gap-2'):
                ui.label('TIME').classes('label-text mb-1')
                ui.time(value='09:30').classes('picker-card')

    # ── 19. SLIDERS ──────────────────────────────────────────────
    ui.label('19 · Sliders').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        with ui.column().classes('gap-5 w-full'):
            with ui.element('div').classes('w-full'):
                ui.label('Default').classes('field-label mb-2')
                ui.slider(min=0, max=100, value=40).classes('w-full').props('label')
            with ui.element('div').classes('w-full'):
                ui.label('With step (10)').classes('field-label mb-2')
                ui.slider(min=0, max=100, value=60, step=10).classes('w-full').props('label snap markers')
            with ui.element('div').classes('w-full'):
                ui.label('Range slider').classes('field-label mb-2')
                ui.range(min=0, max=100, value={'min': 20, 'max': 75}).classes('w-full').props('label')

    # ── 20. NUMBER INPUT ─────────────────────────────────────────
    ui.label('20 · Number Input').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        with ui.row().classes('gap-4 flex-wrap'):
            with ui.element('div').classes('w-full').style('max-width:200px'):
                ui.label('Integer').classes('field-label')
                ui.number(value=42, min=0, max=999, step=1).classes('w-full').props('outlined')
            with ui.element('div').classes('w-full').style('max-width:200px'):
                ui.label('Decimal').classes('field-label')
                ui.number(value=3.14, min=0, step=0.01, format='%.2f').classes('w-full').props('outlined')
            with ui.element('div').classes('w-full').style('max-width:200px'):
                ui.label('Disabled').classes('field-label')
                ui.number(value=100).classes('w-full').props('outlined disable')

    # ── 21. FILE UPLOAD ──────────────────────────────────────────
    ui.label('21 · File Upload').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        ui.upload(label='Drop files here or click to browse',
                  on_upload=lambda e: notify(f'Uploaded: {e.name}', type='positive', title='Upload complete'),
                  on_rejected=lambda: notify('File rejected — check type or size.', type='negative', title='Upload failed'),
                  max_file_size=5_000_000).classes('w-full upload-area').props('flat bordered accept=".pdf,.png,.jpg,.xlsx"')

    # ── 22. ACCORDION / EXPANSION ────────────────────────────────
    ui.label('22 · Accordion').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4 p-0'):
        with ui.expansion('What is this design system?', icon='help_outline').classes('accordion-item'):
            ui.label('A collection of reusable, consistently styled UI components built on NiceGUI + Quasar + custom CSS design tokens.').classes('text-sm text-muted')
        ui.element('div').classes('divider m-0')
        with ui.expansion('How do I use the button variants?', icon='code').classes('accordion-item'):
            ui.label('Add color=\'white\' and .props(\'flat no-caps\') together with the .button .button-{variant} classes.').classes('text-sm text-muted')
        ui.element('div').classes('divider m-0')
        with ui.expansion('Can I customize colors?', icon='palette').classes('accordion-item'):
            ui.label('Yes — edit the CSS variables in :root inside global-css.css. All components reference the same tokens.').classes('text-sm text-muted')

    # ── 23. STEPPER / WIZARD ─────────────────────────────────────
    ui.label('23 · Stepper').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        with ui.stepper(value='Details').props('vertical').classes('w-full stepper') as stepper:
            with ui.step('Details', icon='person'):
                ui.label('Fill in your personal details.').classes('text-sm text-muted mb-3')
                with ui.row().classes('gap-2 mt-2'):
                    ui.button('Continue', color='white', on_click=stepper.next).props('flat no-caps').classes('button button-primary button-sm')
            with ui.step('Address', icon='home'):
                ui.label('Enter your shipping address.').classes('text-sm text-muted mb-3')
                with ui.row().classes('gap-2 mt-2'):
                    ui.button('Back', color='white', on_click=stepper.previous).props('flat no-caps').classes('button button-outline button-sm')
                    ui.button('Continue', color='white', on_click=stepper.next).props('flat no-caps').classes('button button-primary button-sm')
            with ui.step('Review', icon='check_circle'):
                ui.label('Review and confirm your order.').classes('text-sm text-muted mb-3')
                with ui.row().classes('gap-2 mt-2'):
                    ui.button('Back', color='white', on_click=stepper.previous).props('flat no-caps').classes('button button-outline button-sm')
                    ui.button('Submit', color='white', on_click=lambda: notify('Order submitted!', type='positive', title='Success')).props('flat no-caps').classes('button button-primary button-sm')

    # ── 24. AVATAR & CHIPS ───────────────────────────────────────
    ui.label('24 · Avatar & Chips').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        ui.label('AVATAR').classes('label-text mb-3')
        with ui.row().classes('gap-4 items-center flex-wrap mb-4'):
            ui.avatar('AB', color='primary',  text_color='white', size='48px')
            ui.avatar('JD', color='positive', text_color='white', size='48px')
            ui.avatar('XY', color='negative', text_color='white', size='48px')
            ui.avatar(icon='person', color='secondary', size='48px')
            ui.avatar(icon='star',   color='warning',   size='48px')
        ui.element('div').classes('divider')
        ui.label('CHIPS').classes('label-text mb-3')
        with ui.row().classes('gap-2 flex-wrap'):
            for label, cls in [('Default','chip'), ('Primary','chip chip-primary'), ('Success','chip chip-success'),
                                ('Warning','chip chip-warning'), ('Danger','chip chip-danger'), ('Info','chip chip-info')]:
                ui.label(label).classes(cls)
        ui.element('div').classes('divider mt-3')
        ui.label('CHIPS WITH ICON').classes('label-text mb-3')
        with ui.row().classes('gap-2 flex-wrap'):
            with ui.element('span').classes('chip chip-primary'):
                ui.icon('check_circle').style('font-size:14px;margin-right:4px')
                ui.label('Active')
            with ui.element('span').classes('chip chip-danger'):
                ui.icon('cancel').style('font-size:14px;margin-right:4px')
                ui.label('Rejected')
            with ui.element('span').classes('chip chip-success'):
                ui.icon('local_shipping').style('font-size:14px;margin-right:4px')
                ui.label('Shipped')

    # ── 26. SKELETON ─────────────────────────────────────────────
    ui.label('26 · Skeleton / Loading').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        with ui.column().classes('gap-3 w-full'):
            ui.label('TEXT LINES').classes('label-text mb-2')
            with ui.column().classes('gap-2 w-full'):
                ui.element('div').classes('skeleton skeleton-text').style('width:60%')
                ui.element('div').classes('skeleton skeleton-text').style('width:90%')
                ui.element('div').classes('skeleton skeleton-text').style('width:75%')
            ui.element('div').classes('divider')
            ui.label('CARD PLACEHOLDER').classes('label-text mb-2')
            with ui.row().classes('gap-3 items-center'):
                ui.element('div').classes('skeleton skeleton-avatar')
                with ui.column().classes('gap-2 flex-1'):
                    ui.element('div').classes('skeleton skeleton-text').style('width:50%')
                    ui.element('div').classes('skeleton skeleton-text').style('width:80%')
            ui.element('div').classes('skeleton skeleton-rect mt-2')

    # ── 27. SPLITTER ─────────────────────────────────────────────
    ui.label('27 · Splitter').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        with ui.splitter(value=40).classes('w-full splitter-wrap').style('height:120px') as splitter:
            with splitter.before:
                ui.label('Left pane').classes('section-title p-4')
                ui.label('Drag the handle to resize.').classes('text-sm text-muted px-4')
            with splitter.after:
                ui.label('Right pane').classes('section-title p-4')
                ui.label('Both sides are scrollable.').classes('text-sm text-muted px-4')

    # ── 28. CODE DISPLAY ─────────────────────────────────────────
    ui.label('28 · Code Display').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        ui.code('''from nicegui import ui

def content() -> None:
    ui.button("Hello", color="white").props("flat no-caps").classes("button button-primary")
    ui.notify("Done!", type="positive")
''').classes('w-full code-block')

    # ── 29. TIMELINE ─────────────────────────────────────────────
    ui.label('29 · Timeline').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        with ui.timeline(side='right'):
            ui.timeline_entry('Order placed by customer via web portal.',
                              title='Order Created', subtitle='Feb 26, 09:12', icon='shopping_cart', color='primary')
            ui.timeline_entry('Payment confirmed. Transaction ID: TXN-884421.',
                              title='Payment Confirmed', subtitle='Feb 26, 09:15', icon='credit_card', color='positive')
            ui.timeline_entry('Item picked and packed in warehouse B.',
                              title='Packed', subtitle='Feb 26, 11:40', icon='inventory_2', color='info')
            ui.timeline_entry('Handed to carrier. Tracking: DHL-99281744.',
                              title='Shipped', subtitle='Feb 26, 14:05', icon='local_shipping', color='warning')
            ui.timeline_entry('Awaiting delivery to customer address.',
                              title='In Transit', subtitle='Pending', icon='pending', color='negative')

    # ── 30. BREADCRUMBS & PAGINATION ─────────────────────────────
    ui.label('30 · Breadcrumbs & Pagination').classes('section-title mt-4 mb-2')
    with ui.element('div').classes('card mb-4'):
        ui.label('BREADCRUMBS').classes('label-text mb-3')
        with ui.row().classes('items-center gap-1 breadcrumb mb-4'):
            for i, (label, icon) in enumerate([('Home', 'home'), ('Orders', 'receipt_long'), ('ORD-001', 'article')]):
                with ui.row().classes('items-center gap-1'):
                    ui.icon(icon).classes('breadcrumb-icon')
                    ui.label(label).classes('breadcrumb-el' + (' breadcrumb-active' if i == 2 else ''))
                if i < 2:
                    ui.icon('chevron_right').classes('breadcrumb-sep')
        ui.element('div').classes('divider')
        ui.label('PAGINATION').classes('label-text mb-3')
        ui.pagination(value=3, min=1, max=10).props('direction-links boundary-links color=primary').classes('pagination')
