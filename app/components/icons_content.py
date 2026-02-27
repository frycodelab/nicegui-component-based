"""Icon browser — Tabler Icons + Google Material Icons; searchable grid with click-to-copy."""

import re
from pathlib import Path
from nicegui import ui

# ── Parse Tabler icons from icons.css at module load ──────────────────────────────────────────────────────
def _load_tabler_icons() -> list[str]:
    css_path = Path(__file__).parent.parent / "assets" / "css" / "icons.css"
    text = css_path.read_text(encoding="utf-8", errors="ignore")
    names = re.findall(r'\.ti-([\w-]+):before', text)
    return sorted(set(names))


_TABLER_ICONS: list[str] = _load_tabler_icons()

# ── Google Material Icons curated list ──────────────────────────────────────────────────────────────
_MATERIAL_ICONS: list[str] = sorted([
    # Navigation & UI
    "home","menu","close","search","settings","more_vert","more_horiz",
    "arrow_back","arrow_forward","arrow_upward","arrow_downward",
    "chevron_left","chevron_right","expand_more","expand_less",
    "first_page","last_page","navigate_before","navigate_next",
    "fullscreen","fullscreen_exit","open_in_new","open_in_full",
    "zoom_in","zoom_out","refresh","sync","loop","replay",
    "undo","redo","check","clear","add","remove","edit","delete",
    "save","cancel","done","done_all","block","report","warning",
    "info","help","help_outline","error","error_outline",
    "visibility","visibility_off","lock","lock_open","key",
    "filter_list","filter_alt","sort","swap_vert","swap_horiz",
    "drag_indicator","reorder","view_list","view_module","view_grid",
    "apps","dashboard","widgets","layers","map","location_on",
    "my_location","near_me","navigation","explore","compass_calibration",
    # People & Account
    "person","people","group","groups","account_circle","account_box",
    "face","supervised_user_circle","manage_accounts","badge","contacts",
    "person_add","person_remove","person_search","how_to_reg",
    "admin_panel_settings","supervisor_account","switch_account",
    # Communication
    "mail","mail_outline","email","inbox","send","reply","reply_all",
    "forward","drafts","markunread","mark_as_unread","chat","message",
    "sms","forum","comment","announcement","notifications",
    "notifications_none","notifications_active","notifications_off",
    "phone","phone_enabled","phone_disabled","call","call_end",
    "voicemail","contact_phone","contact_mail","dialpad","videocam",
    # Files & Folders
    "folder","folder_open","folder_special","folder_shared",
    "create_new_folder","insert_drive_file","file_copy","file_present",
    "attach_file","attachment","cloud","cloud_upload","cloud_download",
    "cloud_done","cloud_off","cloud_sync","upload","download","backup",
    "restore","description","article","assignment","list_alt","note",
    "notes","sticky_note_2","feed","summarize","topic","snippet_folder",
    # Data & Analytics
    "bar_chart","show_chart","pie_chart","donut_large","multiline_chart",
    "stacked_bar_chart","area_chart","waterfall_chart","bubble_chart",
    "leaderboard","analytics","insights","trending_up","trending_down",
    "trending_flat","table_chart","grid_on","dataset","data_object",
    "data_array","functions","calculate","schema","hub","device_hub",
    # Actions & Tools
    "build","build_circle","construction","handyman","hardware",
    "engineering","precision_manufacturing","factory","inventory",
    "inventory_2","warehouse","forklift","pallet","package","archive",
    "unarchive","move_to_inbox","outbox","publish","get_app",
    "print","print_disabled","scanner","content_cut","content_copy",
    "content_paste","content_paste_go","copy_all","select_all",
    "deselect","share","link","link_off","qr_code","qr_code_2",
    "barcode","format_list_bulleted","format_list_numbered","checklist",
    # Commerce & Finance
    "shopping_cart","shopping_cart_checkout","add_shopping_cart",
    "remove_shopping_cart","shopping_bag","shop","storefront","store",
    "local_mall","point_of_sale","payments","payment","credit_card",
    "account_balance","account_balance_wallet","monetization_on",
    "money","attach_money","currency_exchange","savings","receipt",
    "receipt_long","request_quote","invoice","price_check","sell",
    "local_offer","discount","loyalty","redeem","card_giftcard",
    # Shipping & Logistics
    "local_shipping","delivery_dining","two_wheeler","airport_shuttle",
    "flight","flight_takeoff","flight_land","train","directions_bus",
    "directions_car","directions_boat","cargo","conveyor_belt",
    "package_2","move","deployed_code","output",
    # Status & Alerts
    "check_circle","check_circle_outline","cancel","highlight_off",
    "radio_button_checked","radio_button_unchecked","indeterminate_check_box",
    "check_box","check_box_outline_blank","toggle_on","toggle_off",
    "fiber_manual_record","circle","square","star","star_border",
    "star_half","favorite","favorite_border","thumb_up","thumb_down",
    "emoji_emotions","sentiment_satisfied","sentiment_dissatisfied",
    "sentiment_neutral","mood","mood_bad","flag","outlined_flag",
    "tour","label","label_off","new_label","sell","bookmark",
    "bookmark_border","bookmark_add","bookmarks","turned_in","turned_in_not",
    # Time & Calendar
    "calendar_today","calendar_month","event","event_available",
    "event_busy","event_note","schedule","access_time","alarm",
    "alarm_add","alarm_off","alarm_on","timer","timer_off","hourglass_empty",
    "hourglass_full","hourglass_top","hourglass_bottom","watch_later",
    "date_range","today","history","update","pending","pending_actions",
    "more_time","time_to_leave","timelapse",
    # Media
    "play_arrow","pause","stop","skip_next","skip_previous","fast_forward",
    "fast_rewind","replay_10","forward_10","volume_up","volume_down",
    "volume_off","mute","mic","mic_off","headphones","speaker","tv",
    "movie","image","photo","photo_camera","camera","videocam","gif",
    "slideshow","collections","playlist_play","queue_music","library_music",
    # Devices & Tech
    "devices","computer","laptop","smartphone","tablet","watch",
    "monitor","desktop_windows","keyboard","mouse","storage","memory",
    "sd_card","usb","bluetooth","wifi","signal_wifi_4_bar",
    "network_check","router","dns","cloud_computing","terminal",
    "code","developer_mode","developer_board","integration_instructions",
    "bug_report","pest_control","verified","security","vpn_key",
    "fingerprint","face_recognition","qr_code_scanner","nfc",
    # Health & Safety
    "health_and_safety","local_hospital","medical_services","medication",
    "healing","vaccines","monitor_heart","bloodtype","clean_hands",
    "sanitizer","masks","sick","emergency","fire_extinguisher","smoke_free",
    # Nature & Environment
    "eco","park","nature","grass","forest","water","waves","ac_unit",
    "wb_sunny","cloud_queue","thunderstorm","foggy","grain","terrain",
    "landscaping","yard","local_florist","spa","energy_savings_leaf",
    "recycling","compost","water_drop","outdoor_grill",
    # Food & Dining
    "restaurant","local_dining","local_cafe","local_bar","fastfood",
    "dinner_dining","brunch_dining","lunch_dining","bakery_dining",
    "tapas","set_meal","ramen_dining","rice_bowl","no_food","no_drinks",
    # Misc Useful
    "lightbulb","lightbulb_outline","power","power_off","electric_bolt",
    "battery_full","battery_charging_full","battery_0_bar",
    "brightness_high","brightness_low","dark_mode","light_mode","contrast",
    "palette","brush","format_paint","colorize","texture","style",
    "font_download","text_fields","title","subject","short_text",
    "wrap_text","format_bold","format_italic","format_underlined",
    "format_align_left","format_align_center","format_align_right",
    "translate","language","public","travel_explore","place","map",
    "event_seat","meeting_room","stairs","elevator","escalator",
    "accessible","accessible_forward","wheelchair_pickup","elderly",
    "child_care","sports","sports_soccer","sports_basketball","fitness_center",
    "pool","golf_course","casino","celebration","cake","wine_bar",
    "emoji_events","military_tech","workspace_premium","verified_user",
    "gpp_good","gpp_bad","shield","policy","privacy_tip","encrypted",
])

_PAGE_SIZE = 200

# ── Copy-to-clipboard JS + tile CSS (injected once into page body) ────────────
_COPY_JS = """
<style>
    .ib-grid-inner {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(108px, 1fr));
        gap: 6px;
    }
    .ib-tile {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: 6px;
        padding: 12px 6px 10px;
        border-radius: 8px;
        border: 1px solid transparent;
        cursor: pointer;
        background: var(--faint, #f4f4f5);
        transition: background .12s, border-color .12s, transform .12s, box-shadow .12s;
        user-select: none;
        overflow: hidden;
    }
    .ib-tile:hover {
        background: #fff;
        border-color: #60a5fa;
        box-shadow: 0 1px 6px rgba(96,165,250,.22);
        transform: translateY(-1px);
    }
    .ib-tile.copied {
        background: #f0fdf4 !important;
        border-color: #4ade80 !important;
    }
    .ib-tile i.ti { font-size: 24px; color: #18181b; line-height: 1; }
    .ib-tile .material-icons { font-size: 24px; color: #18181b; line-height: 1; }
    .ib-name {
        font-size: 11px;
        font-weight: 500;
        color: #3f3f46;
        text-align: center;
        word-break: break-all;
        line-height: 1.3;
        max-width: 100%;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    #ib-toast {
        position: fixed;
        bottom: 24px;
        left: 50%;
        transform: translateX(-50%) translateY(20px);
        background: #18181b;
        color: #fff;
        padding: 8px 18px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 500;
        opacity: 0;
        transition: opacity .2s, transform .2s;
        z-index: 9999;
        pointer-events: none;
        white-space: nowrap;
    }
    #ib-toast.show { opacity: 1; transform: translateX(-50%) translateY(0); }
</style>
<div id="ib-toast"></div>
<script>
window.__ibToastTimer = null;
window.ibShowToast = function(msg) {
    var t = document.getElementById('ib-toast');
    if (!t) return;
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(window.__ibToastTimer);
    window.__ibToastTimer = setTimeout(function() { t.classList.remove('show'); }, 1800);
};
window.ibCopy = function(text, tile) {
    navigator.clipboard.writeText(text).then(function() {
        tile.classList.add('copied');
        setTimeout(function() { tile.classList.remove('copied'); }, 900);
        window.ibShowToast('Copied: ' + text);
    }).catch(function() {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.style.cssText = 'position:fixed;opacity:0;left:-9999px';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        window.ibShowToast('Copied: ' + text);
    });
};
</script>
"""


# ── Component entry point ──────────────────────────────────────────────────────
def content() -> None:
    ui.add_body_html(_COPY_JS)

    # ── Page header ───────────────────────────────────────────────────────────
    with ui.row().classes('w-full items-start justify-between mb-1'):
        with ui.column().classes('gap-0'):
            ui.label('Icon Browser').classes('page-title')
            ui.label(
                f'{len(_TABLER_ICONS):,} Tabler icons + {len(_MATERIAL_ICONS):,} Material icons'
                ' — click any icon to copy its class string.'
            ).classes('text-sm text-muted')
        ui.label('v2.47.0').classes('text-xs text-faint self-center px-2 py-1 rounded').style(
            'background:var(--faint); border:1px solid var(--border)')
    ui.element('div').classes('divider mb-3')

    # ── Usage hint alert ──────────────────────────────────────────────────────
    with ui.element('div').classes('alert alert-info mb-3').style('display:flex; align-items:flex-start; gap:10px'):
        with ui.column().classes('gap-0'):
            ui.label('How to use in NiceGUI').classes('font-semi text-sm')
            ui.label(
                'Tabler: ui.html(\'<i class="ti ti-{name}"></i>\')')
            ui.label(    'Material: ui.icon(\'{name}\')    ')
            ui.label(    'Click any icon to copy its string.').classes('text-sm')

    # ── State ─────────────────────────────────────────────────────────────────
    state = {'tab': 'tabler', 'query': '', 'page': 1}

    # ── Toolbar: tabs + search + count ────────────────────────────────────────
    with ui.row().classes('w-full items-center gap-3 flex-wrap mb-3'):
        with ui.tabs(value='tabler').classes('tabs-bar').props('dense') as tabs:
            ui.tab('tabler',   label='Tabler Icons')
            ui.tab('material', label='Material Icons')

        search = (
            ui.input(placeholder='Search icons…')
            .props('outlined rounded clearable dense')
            .classes('flex-1')
            .style('max-width:380px; min-width:200px')
        )
        count_lbl = ui.label('').classes('text-xs text-muted self-center')

    # ── Icon grid (single html block, replaced on every render) ──────────────
    grid = ui.html('', sanitize=False).classes('w-full')

    # ── Pagination ────────────────────────────────────────────────────────────
    with ui.row().classes('w-full justify-center mt-4'):
        pager = (
            ui.pagination(value=1, min=1, max=1)
            .props('direction-links boundary-links color=primary')
            .classes('pagination')
        )

    # ── Keyboard shortcut: / focuses search ───────────────────────────────────
    ui.keyboard(on_key=lambda e: search.run_method('focus') if e.key == '/' else None)

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _filtered() -> list[str]:
        src = _TABLER_ICONS if state['tab'] == 'tabler' else _MATERIAL_ICONS
        q = state['query']
        return [n for n in src if q in n] if q else src

    def _render() -> None:
        icons = _filtered()
        total = len(icons)
        pages = max(1, -(-total // _PAGE_SIZE))   # ceiling division

        if state['page'] > pages:
            state['page'] = pages

        pager.max = pages
        pager.set_value(state['page'])

        start = (state['page'] - 1) * _PAGE_SIZE
        chunk = icons[start : start + _PAGE_SIZE]

        tab = state['tab']
        tiles = []
        for name in chunk:
            if tab == 'tabler':
                copy_str = f'ti ti-{name}'
                icon_html = f'<i class="ti ti-{name}"></i>'
            else:
                copy_str = name
                icon_html = f'<span class="material-icons">{name}</span>'
            safe_copy = copy_str.replace("'", "\\'")
            safe_name = name.replace("'", "\\'")
            tiles.append(
                f'<div class="ib-tile" onclick="ibCopy(\'{safe_copy}\',this)" title="Copy: {safe_copy}">'
                f'{icon_html}<span class="ib-name">{safe_name}</span></div>'
            )

        end = min(start + _PAGE_SIZE, total)
        count_lbl.set_text(
            f'{total:,} icons' + (f' · {start + 1}–{end}' if pages > 1 else '')
        )
        grid.set_content('<div class="ib-grid-inner">' + ''.join(tiles) + '</div>')

    # ── Event handlers ─────────────────────────────────────────────────────────
    def on_tab(e):
        state['tab'] = e.value
        state['page'] = 1
        _render()

    def on_search(e):
        state['query'] = (e.value or '').strip().lower()
        state['page'] = 1
        _render()

    def on_page(e):
        state['page'] = e.value
        _render()

    tabs.on_value_change(on_tab)
    search.on_value_change(on_search)
    pager.on_value_change(on_page)

    # ── Initial render ─────────────────────────────────────────────────────────
    _render()

