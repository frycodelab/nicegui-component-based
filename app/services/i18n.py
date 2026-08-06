"""Lightweight internationalization (i18n).

Language switching happens live, without a page reload, by binding every
translatable element's text to a per-client :class:`LangState` object. When the
selected language changes, NiceGUI's binding system updates all bound elements.
The choice is also persisted to ``app.storage.user`` and to the user's account
row in the database.
"""

from __future__ import annotations

from nicegui import app, binding, ui

DEFAULT_LANGUAGE = 'en'

# Selectable languages: code -> native display name.
LANGUAGES: dict[str, str] = {
    'en': 'English',
    'de': 'Deutsch',
}

# key -> {lang: text}.  Missing translations fall back to English, then the key.
_TRANSLATIONS: dict[str, dict[str, str]] = {
    # Sidebar navigation
    'nav.dashboard':      {'en': 'Dashboard', 'de': 'Dashboard'},
    'nav.shipping':       {'en': 'Shipping', 'de': 'Versand'},
    'nav.production':     {'en': 'Production', 'de': 'Produktion'},
    'nav.orders':         {'en': 'Orders', 'de': 'Aufträge'},
    'nav.pallets':        {'en': 'Pallets', 'de': 'Paletten'},
    'nav.packing':        {'en': 'Packing', 'de': 'Verpackung'},
    'nav.print_demo':     {'en': 'Print Demo', 'de': 'Druckdemo'},
    'nav.icons':          {'en': 'Icons', 'de': 'Symbole'},
    'nav.design_system':  {'en': 'Design System', 'de': 'Designsystem'},
    'nav.users':          {'en': 'Users', 'de': 'Benutzer'},
    'action.collapse':    {'en': 'Collapse', 'de': 'Einklappen'},

    # Mobile burger sheet & About dialog
    'menu.all_sections':  {'en': 'All sections', 'de': 'Alle Bereiche'},
    'menu.about':         {'en': 'About', 'de': 'Über'},
    'menu.menu':          {'en': 'Menu', 'de': 'Menü'},
    'nav.home':           {'en': 'Home', 'de': 'Start'},
    'about.title':        {'en': 'About This App', 'de': 'Über diese App'},
    'about.body':         {'en': 'Built with NiceGUI and Python. A modern, fully responsive web application.',
                           'de': 'Erstellt mit NiceGUI und Python. Eine moderne, vollständig responsive Web-Anwendung.'},
    'about.source':       {'en': 'View source code on GitHub:', 'de': 'Quellcode auf GitHub ansehen:'},
    'about.repo':         {'en': 'GitHub Repository', 'de': 'GitHub-Repository'},
    'action.close':       {'en': 'Close', 'de': 'Schließen'},

    # Account dropdown
    'account.account':    {'en': 'Account', 'de': 'Konto'},
    'account.settings':   {'en': 'Settings', 'de': 'Einstellungen'},
    'account.logout':     {'en': 'Logout', 'de': 'Abmelden'},
    'account.guest':      {'en': 'Guest', 'de': 'Gast'},
    'language.label':     {'en': 'Language', 'de': 'Sprache'},

    # User settings page
    'settings.title':          {'en': 'Account settings', 'de': 'Kontoeinstellungen'},
    'settings.subtitle':       {'en': 'Manage your profile and preferences', 'de': 'Verwalte dein Profil und deine Einstellungen'},
    'settings.profile':        {'en': 'Profile', 'de': 'Profil'},
    'settings.profile_desc':   {'en': 'Update your photo and personal details.', 'de': 'Aktualisiere dein Foto und deine persönlichen Daten.'},
    'settings.preferences_desc':{'en': 'Choose the language used across the app.', 'de': 'Wähle die appweit verwendete Sprache.'},
    'settings.security_desc':  {'en': 'Set a strong, unique password to protect your account.', 'de': 'Lege ein starkes, einzigartiges Passwort zum Schutz deines Kontos fest.'},
    'settings.photo':          {'en': 'Profile photo', 'de': 'Profilbild'},
    'settings.upload_photo':   {'en': 'Upload photo', 'de': 'Foto hochladen'},
    'settings.remove_photo':   {'en': 'Remove', 'de': 'Entfernen'},
    'settings.display_name':   {'en': 'Display name', 'de': 'Anzeigename'},
    'settings.email':          {'en': 'Email', 'de': 'E-Mail'},
    'settings.username':       {'en': 'Username', 'de': 'Benutzername'},
    'settings.role':           {'en': 'Role', 'de': 'Rolle'},
    'settings.save':           {'en': 'Save changes', 'de': 'Änderungen speichern'},
    'settings.saved':          {'en': 'Profile updated.', 'de': 'Profil aktualisiert.'},
    'settings.preferences':    {'en': 'Preferences', 'de': 'Einstellungen'},
    'settings.security':       {'en': 'Security', 'de': 'Sicherheit'},
    'settings.change_password':{'en': 'Change password', 'de': 'Passwort ändern'},
    'settings.new_password':   {'en': 'New password', 'de': 'Neues Passwort'},
    'settings.confirm_password':{'en': 'Confirm password', 'de': 'Passwort bestätigen'},
    'settings.update_password':{'en': 'Update password', 'de': 'Passwort aktualisieren'},
    'settings.password_updated':{'en': 'Password updated.', 'de': 'Passwort aktualisiert.'},
    'settings.invalid_email':  {'en': 'Please enter a valid email address.', 'de': 'Bitte eine gültige E-Mail-Adresse eingeben.'},
    'settings.language_saved': {'en': 'Language updated.', 'de': 'Sprache aktualisiert.'},
    'settings.image_too_large':{'en': 'Image is too large (max 2 MB).', 'de': 'Bild ist zu groß (max. 2 MB).'},
    'settings.password_not_met':{'en': 'Password does not meet the requirements.', 'de': 'Passwort erfüllt die Anforderungen nicht.'},

    # Avatar dropzone
    'dropzone.title':          {'en': 'Drag & drop an image here', 'de': 'Bild hierher ziehen & ablegen'},
    'dropzone.hint':           {'en': 'or click to browse · PNG, JPG up to 2 MB', 'de': 'oder klicken zum Auswählen · PNG, JPG bis 2 MB'},

    # Password requirements
    'password.req.length':     {'en': '{min}\u2013{max} characters', 'de': '{min}\u2013{max} Zeichen'},
    'password.req.upper':      {'en': 'At least one uppercase letter', 'de': 'Mindestens ein Großbuchstabe'},
    'password.req.lower':      {'en': 'At least one lowercase letter', 'de': 'Mindestens ein Kleinbuchstabe'},
    'password.req.number':     {'en': 'At least one number', 'de': 'Mindestens eine Zahl'},
    'password.req.special':    {'en': 'At least one special character', 'de': 'Mindestens ein Sonderzeichen'},
    'password.match':          {'en': 'Passwords match', 'de': 'Passwörter stimmen überein'},

    # Dashboard view
    'dashboard.title':          {'en': 'Dashboard', 'de': 'Dashboard'},
    'dashboard.subtitle':       {'en': 'Live overview · refreshes on demand', 'de': 'Live-Übersicht · aktualisiert bei Bedarf'},
    'dashboard.refresh':        {'en': 'Refresh', 'de': 'Aktualisieren'},
    'dashboard.kpi.orders':     {'en': 'Total Orders', 'de': 'Aufträge gesamt'},
    'dashboard.kpi.revenue':    {'en': 'Revenue total', 'de': 'Umsatz gesamt'},
    'dashboard.kpi.shipments':  {'en': 'Active Shipments', 'de': 'Aktive Sendungen'},
    'dashboard.kpi.throughput': {'en': 'Production Rate', 'de': 'Produktionsrate'},
    'dashboard.revenue_trend':  {'en': 'Revenue Trend', 'de': 'Umsatzverlauf'},
    'dashboard.order_status':   {'en': 'Order Status', 'de': 'Auftragsstatus'},
    'dashboard.daily_orders':   {'en': 'Daily Orders', 'de': 'Tägliche Aufträge'},
    'dashboard.throughput':     {'en': 'Production Throughput', 'de': 'Produktionsdurchsatz'},

    # Shipping view
    'shipping.title':     {'en': 'Shipping', 'de': 'Versand'},
    'shipping.subtitle':  {'en': 'Manage outbound shipments and carrier assignments.', 'de': 'Ausgehende Sendungen und Frachtführerzuordnungen verwalten.'},
    'shipping.add':       {'en': '+ Add Shipment', 'de': '+ Sendung hinzufügen'},

    # Production view
    'production.title':     {'en': 'Production', 'de': 'Produktion'},
    'production.subtitle':  {'en': 'Monitor line status, work orders and throughput.', 'de': 'Linienstatus, Arbeitsaufträge und Durchsatz überwachen.'},
    'production.add':       {'en': '+ New Work Order', 'de': '+ Neuer Arbeitsauftrag'},

    # Orders view
    'orders.title':     {'en': 'Orders', 'de': 'Aufträge'},
    'orders.subtitle':  {'en': 'Track and manage incoming customer orders.', 'de': 'Eingehende Kundenaufträge verfolgen und verwalten.'},
    'orders.add':       {'en': '+ New Order', 'de': '+ Neuer Auftrag'},

    # Pallets view
    'pallets.title':     {'en': 'Pallets', 'de': 'Paletten'},
    'pallets.subtitle':  {'en': 'Track pallet inventory, locations and capacity utilisation.', 'de': 'Palettenbestand, Standorte und Kapazitätsauslastung verfolgen.'},
    'pallets.add':       {'en': '+ Register Pallet', 'de': '+ Palette registrieren'},

    # Packing view
    'packing.title':     {'en': 'Packings', 'de': 'Verpackungen'},
    'packing.subtitle':  {'en': 'Manage packing jobs across all stages.', 'de': 'Verpackungsaufträge über alle Phasen hinweg verwalten.'},
    'packing.add':       {'en': '+ New Job', 'de': '+ Neuer Auftrag'},

    # Icons view
    'icons.title':     {'en': 'Icon Browser', 'de': 'Symbol-Browser'},
    'icons.subtitle':  {'en': '{tabler} Tabler icons + {material} Material icons — click any icon to copy its class string.', 'de': '{tabler} Tabler-Symbole + {material} Material-Symbole — auf ein Symbol klicken, um seine Klasse zu kopieren.'},

    # Design System view
    'design_system.title':     {'en': 'Design System', 'de': 'Designsystem'},
    'design_system.subtitle':  {'en': 'Every CSS component & utility token at a glance.', 'de': 'Alle CSS-Komponenten & Utility-Token auf einen Blick.'},

    # Print Demo view
    'print_demo.title':     {'en': 'Print Demo', 'de': 'Druckdemo'},
    'print_demo.subtitle':  {'en': 'Live examples of every print_component mode — click any card to open the print dialog.', 'de': 'Live-Beispiele für jeden print_component-Modus — auf eine Karte klicken, um den Druckdialog zu öffnen.'},

    # App Settings stub view
    'appsettings.welcome':  {'en': 'Welcome to the Settings', 'de': 'Willkommen bei den Einstellungen'},
    'appsettings.label':    {'en': 'Settings', 'de': 'Einstellungen'},

    # Application settings: logging
    'appsettings.title':        {'en': 'App Settings', 'de': 'App-Einstellungen'},
    'appsettings.subtitle':     {'en': 'Configure application-wide behaviour.', 'de': 'Appweites Verhalten konfigurieren.'},
    'appsettings.logging':      {'en': 'Logging', 'de': 'Protokollierung'},
    'appsettings.logging_desc': {'en': 'Choose how much detail is written to the rolling log files.', 'de': 'Lege fest, wie detailliert in die rollierenden Protokolldateien geschrieben wird.'},
    'appsettings.log_level':    {'en': 'Log level', 'de': 'Protokollebene'},
    'appsettings.log_file':     {'en': 'Log file', 'de': 'Protokolldatei'},
    'appsettings.level_saved':  {'en': 'Log level set to {level}.', 'de': 'Protokollebene auf {level} gesetzt.'},
    'appsettings.admin_only':   {'en': 'Application settings are available to administrators only.', 'de': 'App-Einstellungen sind nur für Administratoren verfügbar.'},

    # Audit log view
    'audit.title':        {'en': 'Audit Log', 'de': 'Audit-Protokoll'},
    'audit.subtitle':     {'en': 'A chronological record of who did what across the app.', 'de': 'Chronologische Aufzeichnung, wer was in der App getan hat.'},
    'audit.admin_only':   {'en': 'The audit log is available to administrators only.', 'de': 'Das Audit-Protokoll ist nur für Administratoren verfügbar.'},
    'audit.empty':        {'en': 'No activity recorded yet.', 'de': 'Noch keine Aktivität aufgezeichnet.'},
    'audit.showing':      {'en': 'Showing {shown} of {total} entries', 'de': 'Zeige {shown} von {total} Einträgen'},
    'audit.col.time':     {'en': 'Time (UTC)', 'de': 'Zeit (UTC)'},
    'audit.col.user':     {'en': 'User', 'de': 'Benutzer'},
    'audit.col.action':   {'en': 'Action', 'de': 'Aktion'},
    'audit.col.details':  {'en': 'Details', 'de': 'Details'},
    'audit.col.ip':       {'en': 'IP', 'de': 'IP'},
    'audit.filter.all':   {'en': 'All actions', 'de': 'Alle Aktionen'},
    'audit.clear':        {'en': 'Clear log', 'de': 'Protokoll leeren'},
    'audit.clear_title':  {'en': 'Clear audit log', 'de': 'Audit-Protokoll leeren'},
    'audit.clear_confirm':{'en': 'This permanently deletes all audit entries. Continue?', 'de': 'Dadurch werden alle Audit-Einträge dauerhaft gelöscht. Fortfahren?'},
    'audit.cleared':      {'en': 'Audit log cleared ({n} entries removed).', 'de': 'Audit-Protokoll geleert ({n} Einträge entfernt).'},

    # Audit log action labels
    'audit.action.login':             {'en': 'Signed in', 'de': 'Angemeldet'},
    'audit.action.login_failed':      {'en': 'Failed sign-in', 'de': 'Fehlgeschlagene Anmeldung'},
    'audit.action.logout':            {'en': 'Signed out', 'de': 'Abgemeldet'},
    'audit.action.password_changed':  {'en': 'Changed password', 'de': 'Passwort geändert'},
    'audit.action.password_reset':    {'en': 'Reset password', 'de': 'Passwort zurückgesetzt'},
    'audit.action.user_created':      {'en': 'Created user', 'de': 'Benutzer erstellt'},
    'audit.action.user_deleted':      {'en': 'Deleted user', 'de': 'Benutzer gelöscht'},
    'audit.action.role_changed':      {'en': 'Changed role', 'de': 'Rolle geändert'},
    'audit.action.user_activated':    {'en': 'Activated user', 'de': 'Benutzer aktiviert'},
    'audit.action.user_deactivated':  {'en': 'Deactivated user', 'de': 'Benutzer deaktiviert'},
    'audit.action.profile_updated':   {'en': 'Updated profile', 'de': 'Profil aktualisiert'},
    'audit.action.language_changed':  {'en': 'Changed language', 'de': 'Sprache geändert'},

    # Common actions & words
    'common.export':      {'en': 'Export', 'de': 'Exportieren'},
    'common.refresh':     {'en': 'Refresh', 'de': 'Aktualisieren'},
    'common.view_all':    {'en': 'View all', 'de': 'Alle anzeigen'},
    'common.cancel':      {'en': 'Cancel', 'de': 'Abbrechen'},
    'common.create':      {'en': 'Create', 'de': 'Erstellen'},
    'common.delete':      {'en': 'Delete', 'de': 'Löschen'},
    'common.move':        {'en': 'Move', 'de': 'Verschieben'},
    'common.inspect':     {'en': 'Inspect', 'de': 'Prüfen'},
    'common.customer':    {'en': 'Customer', 'de': 'Kunde'},
    'common.product':     {'en': 'Product', 'de': 'Produkt'},
    'common.status':      {'en': 'Status', 'de': 'Status'},
    'common.date':        {'en': 'Date', 'de': 'Datum'},
    'common.total':       {'en': 'Total', 'de': 'Gesamt'},

    # Shared status labels
    'status.pending':     {'en': 'Pending', 'de': 'Ausstehend'},
    'status.in_transit':  {'en': 'In Transit', 'de': 'Unterwegs'},
    'status.delivered':   {'en': 'Delivered', 'de': 'Zugestellt'},
    'status.cancelled':   {'en': 'Cancelled', 'de': 'Storniert'},
    'status.running':     {'en': 'Running', 'de': 'Läuft'},
    'status.paused':      {'en': 'Paused', 'de': 'Pausiert'},
    'status.error':       {'en': 'Error', 'de': 'Fehler'},
    'status.open':        {'en': 'Open', 'de': 'Offen'},
    'status.processing':  {'en': 'Processing', 'de': 'In Bearbeitung'},
    'status.fulfilled':   {'en': 'Fulfilled', 'de': 'Erfüllt'},
    'status.on_hold':     {'en': 'On Hold', 'de': 'Wartend'},
    'status.available':   {'en': 'Available', 'de': 'Verfügbar'},
    'status.in_use':      {'en': 'In Use', 'de': 'In Benutzung'},
    'status.damaged':     {'en': 'Damaged', 'de': 'Beschädigt'},
    'status.active':      {'en': 'Active', 'de': 'Aktiv'},
    'status.inactive':    {'en': 'Inactive', 'de': 'Inaktiv'},

    # Dashboard extras
    'dashboard.last_30_days':  {'en': 'Last 30 days', 'de': 'Letzte 30 Tage'},
    'dashboard.this_month':    {'en': 'This month', 'de': 'Diesen Monat'},
    'dashboard.last_7_days':   {'en': 'Last 7 days', 'de': 'Letzte 7 Tage'},
    'dashboard.last_24h':      {'en': 'Last 24 h', 'de': 'Letzte 24 Std.'},
    'dashboard.refreshed':     {'en': 'Dashboard refreshed', 'de': 'Dashboard aktualisiert'},
    'dashboard.vs_yesterday':  {'en': 'vs yesterday', 'de': 'ggü. gestern'},
    'dashboard.series.revenue':   {'en': 'Revenue', 'de': 'Umsatz'},
    'dashboard.series.forecast':  {'en': 'Forecast', 'de': 'Prognose'},
    'dashboard.series.completed': {'en': 'Completed', 'de': 'Abgeschlossen'},
    'dashboard.series.returned':  {'en': 'Returned', 'de': 'Retouren'},
    'dashboard.series.actual':    {'en': 'Actual', 'de': 'Ist'},
    'dashboard.series.target':    {'en': 'Target', 'de': 'Ziel'},

    # Shipping view details
    'shipping.kpi.shipments':  {'en': 'Shipments', 'de': 'Sendungen'},
    'shipping.sub.this_week':  {'en': 'this week', 'de': 'diese Woche'},
    'shipping.sub.active':     {'en': 'currently active', 'de': 'aktuell aktiv'},
    'shipping.sub.completed':  {'en': 'completed', 'de': 'abgeschlossen'},
    'shipping.sub.awaiting':   {'en': 'awaiting pickup', 'de': 'wartet auf Abholung'},
    'shipping.search':         {'en': 'Search shipments…', 'de': 'Sendungen suchen…'},
    'shipping.col.id':         {'en': 'Shipment ID', 'de': 'Sendungs-ID'},
    'shipping.col.destination':{'en': 'Destination', 'de': 'Ziel'},
    'shipping.col.carrier':    {'en': 'Carrier', 'de': 'Frachtführer'},
    'shipping.col.eta':        {'en': 'ETA', 'de': 'Voraussichtlich'},
    'shipping.col.weight':     {'en': 'Weight (kg)', 'de': 'Gewicht (kg)'},
    'shipping.export_started': {'en': 'Export started', 'de': 'Export gestartet'},
    'shipping.added_title':    {'en': 'Shipment added', 'de': 'Sendung hinzugefügt'},

    # Production view details
    'production.kpi.active_lines': {'en': 'Active Lines', 'de': 'Aktive Linien'},
    'production.kpi.units_today':  {'en': 'Units Today', 'de': 'Einheiten heute'},
    'production.kpi.efficiency':   {'en': 'Efficiency', 'de': 'Effizienz'},
    'production.kpi.shifts':       {'en': 'Shifts', 'de': 'Schichten'},
    'production.kpi.alerts':       {'en': 'Alerts', 'de': 'Warnungen'},
    'production.sub.running':      {'en': 'currently running', 'de': 'aktuell aktiv'},
    'production.sub.of_target':    {'en': 'of {n} target', 'de': 'von {n} Ziel'},
    'production.sub.vs_target':    {'en': 'vs daily target', 'de': 'ggü. Tagesziel'},
    'production.sub.shifts':       {'en': 'Morning / Afternoon / Night', 'de': 'Früh / Spät / Nacht'},
    'production.sub.errors':       {'en': 'lines in error state', 'de': 'Linien im Fehlerzustand'},
    'production.line_status':      {'en': 'Line Status', 'de': 'Linienstatus'},
    'production.lines_count':      {'en': '{n} production lines', 'de': '{n} Produktionslinien'},
    'production.col.line':         {'en': 'Line', 'de': 'Linie'},
    'production.col.shift':        {'en': 'Shift', 'de': 'Schicht'},
    'production.col.progress':     {'en': 'Progress', 'de': 'Fortschritt'},
    'production.col.actual_target':{'en': 'Actual / Target', 'de': 'Ist / Ziel'},
    'production.throughput_today': {'en': 'Throughput Today', 'de': 'Durchsatz heute'},
    'production.units_per_hour':   {'en': 'Units per hour — running lines only', 'de': 'Einheiten pro Stunde — nur laufende Linien'},
    'production.refreshed':        {'en': 'Line data refreshed', 'de': 'Liniendaten aktualisiert'},
    'production.wo_soon':          {'en': 'Work order form coming soon', 'de': 'Arbeitsauftragsformular folgt bald'},
    'production.shift.morning':    {'en': 'Morning', 'de': 'Früh'},
    'production.shift.afternoon':  {'en': 'Afternoon', 'de': 'Spät'},
    'production.shift.night':      {'en': 'Night', 'de': 'Nacht'},

    # Orders view details
    'orders.kpi.total':       {'en': 'Total Orders', 'de': 'Aufträge gesamt'},
    'orders.kpi.revenue':     {'en': 'Revenue', 'de': 'Umsatz'},
    'orders.kpi.fulfilled':   {'en': 'Fulfilled', 'de': 'Erfüllt'},
    'orders.kpi.processing':  {'en': 'Processing', 'de': 'In Bearbeitung'},
    'orders.kpi.cancelled':   {'en': 'Cancelled', 'de': 'Storniert'},
    'orders.sub.this_week':   {'en': 'this week', 'de': 'diese Woche'},
    'orders.sub.completed':   {'en': 'completed', 'de': 'abgeschlossen'},
    'orders.sub.in_progress': {'en': 'in progress', 'de': 'in Bearbeitung'},
    'orders.status_breakdown':{'en': 'Status Breakdown', 'de': 'Statusaufteilung'},
    'orders.orders_revenue':  {'en': 'Orders & Revenue — This Week', 'de': 'Aufträge & Umsatz — Diese Woche'},
    'orders.recent':          {'en': 'Recent Orders', 'de': 'Letzte Aufträge'},
    'orders.shown':           {'en': '{n} orders shown', 'de': '{n} Aufträge angezeigt'},
    'orders.loading_all':     {'en': 'Loading full order list…', 'de': 'Vollständige Auftragsliste wird geladen…'},
    'orders.col.id':          {'en': 'Order ID', 'de': 'Auftrags-ID'},
    'orders.col.qty':         {'en': 'Qty', 'de': 'Menge'},
    'orders.legend.orders':   {'en': 'Orders', 'de': 'Aufträge'},
    'orders.legend.revenue':  {'en': 'Revenue', 'de': 'Umsatz'},
    'orders.new_order':       {'en': 'New Order', 'de': 'Neuer Auftrag'},
    'orders.priority':        {'en': 'Priority', 'de': 'Priorität'},
    'orders.quantity':        {'en': 'Quantity', 'de': 'Menge'},
    'orders.create_order':    {'en': 'Create Order', 'de': 'Auftrag erstellen'},
    'orders.created':         {'en': 'Order created successfully', 'de': 'Auftrag erfolgreich erstellt'},
    'orders.created_title':   {'en': 'Order Created', 'de': 'Auftrag erstellt'},
    'orders.priority.normal': {'en': 'Normal', 'de': 'Normal'},
    'orders.priority.high':   {'en': 'High', 'de': 'Hoch'},
    'orders.priority.urgent': {'en': 'Urgent', 'de': 'Dringend'},

    # Pallets view details
    'pallets.kpi.total':       {'en': 'Total', 'de': 'Gesamt'},
    'pallets.kpi.available':   {'en': 'Available', 'de': 'Verfügbar'},
    'pallets.kpi.in_use':      {'en': 'In Use', 'de': 'In Benutzung'},
    'pallets.kpi.in_transit':  {'en': 'In Transit', 'de': 'Unterwegs'},
    'pallets.kpi.damaged':     {'en': 'Damaged', 'de': 'Beschädigt'},
    'pallets.kpi.utilisation': {'en': 'Utilisation', 'de': 'Auslastung'},
    'pallets.sub.registered':  {'en': 'registered', 'de': 'registriert'},
    'pallets.sub.ready':       {'en': 'ready to use', 'de': 'einsatzbereit'},
    'pallets.sub.loaded':      {'en': 'currently loaded', 'de': 'aktuell beladen'},
    'pallets.sub.moving':      {'en': 'on the move', 'de': 'unterwegs'},
    'pallets.sub.inspection':  {'en': 'needs inspection', 'de': 'muss geprüft werden'},
    'pallets.sub.fleet':       {'en': 'fleet avg load', 'de': 'ø Flottenauslastung'},
    'pallets.inventory':       {'en': 'Pallet Inventory', 'de': 'Palettenbestand'},
    'pallets.registered_count':{'en': '{n} pallets registered', 'de': '{n} Paletten registriert'},
    'pallets.load_capacity':   {'en': 'Load capacity', 'de': 'Ladekapazität'},
    'pallets.by_location':     {'en': 'By Location', 'de': 'Nach Standort'},
    'pallets.locations_count': {'en': '{n} locations', 'de': '{n} Standorte'},
    'pallets.col.location':    {'en': 'Location', 'de': 'Standort'},
    'pallets.col.pallets':     {'en': 'Pallets', 'de': 'Paletten'},
    'pallets.col.total_load':  {'en': 'Total Load', 'de': 'Gesamtlast'},
    'pallets.col.utilisation': {'en': 'Utilisation', 'de': 'Auslastung'},
    'pallets.move_scheduled':  {'en': '{id} move scheduled', 'de': '{id} Verschiebung geplant'},
    'pallets.inspect_queued':  {'en': '{id} inspection queued', 'de': '{id} Prüfung eingereiht'},
    'pallets.reg_soon':        {'en': 'Registration form coming soon', 'de': 'Registrierungsformular folgt bald'},

    # Packings view details
    'packing.total_jobs':    {'en': 'TOTAL JOBS', 'de': 'AUFTRÄGE GESAMT'},
    'packing.units_to_pack': {'en': '{n} units to pack', 'de': '{n} Einheiten zu verpacken'},
    'packing.col.pending':     {'en': 'Pending', 'de': 'Ausstehend'},
    'packing.col.in_progress': {'en': 'In Progress', 'de': 'In Bearbeitung'},
    'packing.col.packed':      {'en': 'Packed', 'de': 'Verpackt'},
    'packing.pct_of_jobs':   {'en': '{n} % of jobs', 'de': '{n} % der Aufträge'},
    'packing.due':           {'en': 'Due {date}', 'de': 'Fällig {date}'},
    'packing.units':         {'en': '{n} units', 'de': '{n} Einheiten'},
    'packing.action.start':       {'en': 'Start', 'de': 'Starten'},
    'packing.action.mark_packed': {'en': 'Mark Packed', 'de': 'Als verpackt markieren'},
    'packing.action.dispatch':    {'en': 'Dispatch', 'de': 'Versenden'},
    'packing.status.started':     {'en': 'Started', 'de': 'Gestartet'},
    'packing.status.packed':      {'en': 'Packed', 'de': 'Verpackt'},
    'packing.status.dispatched':  {'en': 'Dispatched', 'de': 'Versendet'},
    'packing.notify.started':     {'en': '{id} — started', 'de': '{id} — gestartet'},
    'packing.notify.packed':      {'en': '{id} — packed', 'de': '{id} — verpackt'},
    'packing.notify.dispatched':  {'en': '{id} — dispatched', 'de': '{id} — versendet'},
    'packing.job_soon':      {'en': 'New job form coming soon', 'de': 'Neues Auftragsformular folgt bald'},

    # Users admin view
    'users.title':            {'en': 'User management', 'de': 'Benutzerverwaltung'},
    'users.subtitle':         {'en': 'Manage users and roles (admin only)', 'de': 'Benutzer und Rollen verwalten (nur Admin)'},
    'users.access_denied':    {'en': 'Access denied', 'de': 'Zugriff verweigert'},
    'users.admin_only':       {'en': 'This page is for administrators only.', 'de': 'Diese Seite ist nur für Administratoren.'},
    'users.col.user':         {'en': 'User', 'de': 'Benutzer'},
    'users.col.role':         {'en': 'Role', 'de': 'Rolle'},
    'users.col.status':       {'en': 'Status', 'de': 'Status'},
    'users.col.actions':      {'en': 'Actions', 'de': 'Aktionen'},
    'users.pw_pending':       {'en': 'Password change pending', 'de': 'Passwortänderung ausstehend'},
    'users.role.admin':       {'en': 'Admin', 'de': 'Admin'},
    'users.role.user':        {'en': 'User', 'de': 'Benutzer'},
    'users.tip.reset':        {'en': 'Reset password', 'de': 'Passwort zurücksetzen'},
    'users.tip.switch_role':  {'en': 'Switch role', 'de': 'Rolle wechseln'},
    'users.tip.deactivate':   {'en': 'Deactivate', 'de': 'Deaktivieren'},
    'users.tip.activate':     {'en': 'Activate', 'de': 'Aktivieren'},
    'users.tip.delete':       {'en': 'Delete', 'de': 'Löschen'},
    'users.create':           {'en': 'Create user', 'de': 'Benutzer erstellen'},
    'users.create_new':       {'en': 'Create new user', 'de': 'Neuen Benutzer erstellen'},
    'users.initial_pw':       {'en': 'Initial password: "{pw}" — must be changed on first login.', 'de': 'Anfangspasswort: „{pw}" — muss bei der ersten Anmeldung geändert werden.'},
    'users.enter_username':   {'en': 'Please enter a username.', 'de': 'Bitte einen Benutzernamen eingeben.'},
    'users.exists':           {'en': 'User "{name}" already exists.', 'de': 'Benutzer „{name}" existiert bereits.'},
    'users.created':          {'en': 'User "{name}" created.', 'de': 'Benutzer „{name}" erstellt.'},
    'users.deleted':          {'en': 'User "{name}" deleted.', 'de': 'Benutzer „{name}" gelöscht.'},
    'users.pw_reset':         {'en': 'Password reset to "{pw}".', 'de': 'Passwort auf „{pw}" zurückgesetzt.'},
    'users.not_possible':     {'en': 'Not possible', 'de': 'Nicht möglich'},
    'users.delete_confirm':   {'en': 'Really delete user "{name}"? This cannot be undone.', 'de': 'Benutzer „{name}" wirklich löschen? Dies kann nicht rückgängig gemacht werden.'},
    'users.delete_title':     {'en': 'Delete user', 'de': 'Benutzer löschen'},

    # Print Demo view details
    'print_demo.html_title':   {'en': 'HTML Print', 'de': 'HTML-Druck'},
    'print_demo.html_desc':    {'en': 'Pass any HTML string — headings, paragraphs, lists, tables. Great for quick text reports.', 'de': 'Beliebige HTML-Zeichenkette übergeben — Überschriften, Absätze, Listen, Tabellen. Ideal für schnelle Textberichte.'},
    'print_demo.image_title':  {'en': 'Image Print', 'de': 'Bilddruck'},
    'print_demo.image_desc':   {'en': 'Pass a plain base64 string (PNG, JPEG, SVG). The print view centres it on the page with an optional caption.', 'de': 'Einfache base64-Zeichenkette übergeben (PNG, JPEG, SVG). Die Druckansicht zentriert es auf der Seite mit optionaler Beschriftung.'},
    'print_demo.page_title':   {'en': 'Structured Page', 'de': 'Strukturierte Seite'},
    'print_demo.page_desc':    {'en': 'Combine a title, subtitle, and any mix of HTML and image sections into one print-ready document.', 'de': 'Titel, Untertitel und beliebige HTML- und Bildabschnitte zu einem druckfertigen Dokument kombinieren.'},
    'print_demo.preview':      {'en': 'Preview', 'de': 'Vorschau'},
    'print_demo.btn_html':     {'en': 'Print HTML report', 'de': 'HTML-Bericht drucken'},
    'print_demo.btn_image':    {'en': 'Print chart image', 'de': 'Diagrammbild drucken'},
    'print_demo.btn_page':     {'en': 'Print full report', 'de': 'Vollständigen Bericht drucken'},

    # Icons view details
    'icons.how_to':        {'en': 'How to use in NiceGUI', 'de': 'Verwendung in NiceGUI'},
    'icons.click_copy':    {'en': 'Click any icon to copy its string.', 'de': 'Auf ein Symbol klicken, um seine Zeichenkette zu kopieren.'},
    'icons.search':        {'en': 'Search icons…', 'de': 'Symbole suchen…'},
    'icons.tab_tabler':    {'en': 'Tabler Icons', 'de': 'Tabler-Symbole'},
    'icons.tab_material':  {'en': 'Material Icons', 'de': 'Material-Symbole'},

    # Mobile notice
    'mobile.detected':   {'en': 'Mobile Device Detected', 'de': 'Mobilgerät erkannt'},
    'mobile.not_optimized': {'en': 'You are visiting on a mobile device. This application is not optimized for mobile use.', 'de': 'Sie besuchen die Seite mit einem Mobilgerät. Diese Anwendung ist nicht für die mobile Nutzung optimiert.'},
    'mobile.visit_github': {'en': 'Visit us on GitHub', 'de': 'Besuchen Sie uns auf GitHub'},

    # Design System section titles
    'ds.typography':   {'en': '1 · Typography', 'de': '1 · Typografie'},
    'ds.buttons':      {'en': '2 · Buttons', 'de': '2 · Schaltflächen'},
    'ds.cards':        {'en': '3 · Cards & Panels', 'de': '3 · Karten & Panels'},
    'ds.badges':       {'en': '4 · Badges', 'de': '4 · Badges'},
    'ds.status_dots':  {'en': '5 · Status Dots', 'de': '5 · Statuspunkte'},
    'ds.alerts':       {'en': '6 · Alerts', 'de': '6 · Hinweise'},
    'ds.notifications':{'en': '7 · Notifications', 'de': '7 · Benachrichtigungen'},
    'ds.inputs':       {'en': '8 · Inputs', 'de': '8 · Eingabefelder'},
    'ds.input_groups': {'en': '9 · Input Groups', 'de': '9 · Eingabegruppen'},
    'ds.select':       {'en': '10 · Select', 'de': '10 · Auswahl'},
    'ds.progress':     {'en': '11 · Progress', 'de': '11 · Fortschritt'},
    'ds.dialog':       {'en': '12 · Dialog', 'de': '12 · Dialog'},
    'ds.tooltip':      {'en': '13 · Tooltip & Popover', 'de': '13 · Tooltip & Popover'},
    'ds.toggles':      {'en': '14 · Toggles, Checkboxes & Radio', 'de': '14 · Schalter, Kontrollkästchen & Radio'},
    'ds.tabs':         {'en': '15 · Tabs', 'de': '15 · Tabs'},
}


class LangState:
    """Per-client holder whose ``lang`` drives all bound translatable elements."""

    lang = binding.BindableProperty()

    def __init__(self, lang: str) -> None:
        self.lang = lang


def _state() -> LangState:
    state = app.storage.client.get('lang_state')
    if state is None:
        state = LangState(app.storage.user.get('language', DEFAULT_LANGUAGE))
        app.storage.client['lang_state'] = state
    return state


def register_view_refresh(refresh) -> None:
    """Register the active sub-page's ``@ui.refreshable`` refresh callback.

    Views built with plain ``t(...)`` strings (rather than :func:`bind`) wrap their
    body in an ``@ui.refreshable`` and register its ``.refresh`` here so the active
    view rebuilds live when the language changes — without a page reload.  Only the
    currently visible view is tracked; navigating to another view overwrites it.
    """
    app.storage.client['lang_view_refresh'] = refresh


def current_language() -> str:
    return _state().lang


def t(key: str, lang: str | None = None) -> str:
    """Translate ``key`` into ``lang`` (defaults to the current language)."""
    lang = lang or current_language()
    entry = _TRANSLATIONS.get(key, {})
    return entry.get(lang) or entry.get(DEFAULT_LANGUAGE) or key


def bind(element, key: str):
    """Bind an element's text to the current language so it updates live."""
    element.bind_text_from(_state(), 'lang', backward=lambda lang, k=key: t(k, lang))
    return element


def bind_format(element, key: str, **fmt):
    """Bind an element's text to a translated, ``str.format``-ed key so it updates live."""
    element.bind_text_from(_state(), 'lang', backward=lambda lang: t(key, lang).format(**fmt))
    return element


def bind_language_name(element):
    """Bind an element's text to the current language's display name (e.g. 'Deutsch')."""
    element.bind_text_from(_state(), 'lang', backward=lambda lang: LANGUAGES.get(lang, lang))
    return element


def set_language(code: str) -> None:
    """Switch language live and persist it to the session and the account."""
    if code not in LANGUAGES:
        return
    app.storage.user['language'] = code
    _state().lang = code  # triggers all bound elements to re-render

    # Re-render the active view (built with plain t(...) strings) live.
    refresh = app.storage.client.get('lang_view_refresh')
    if refresh is not None:
        try:
            refresh()
        except Exception:
            pass

    user_id = app.storage.user.get('user_id')
    if user_id is not None:
        # Lazy import avoids a circular dependency at module load time.
        from core.database import get_session
        from services.user_service import UserService
        with get_session() as session:
            UserService(session).set_language(user_id, code)
