# GA4 — key events (Admin checklist)

After deployment, events appear in **GA4 → Admin → Data display → Events** (and Realtime). Mark the ones that match your business goals as **key events** (formerly “conversions”).

## Recommended key events

| Event | Why |
|--------|-----|
| `lead_submitted` | Strong intent / lead capture success |
| `tool_used` | Engagement with a free tool |
| `tool_result_shown` | Completed tool value moment |
| `cta_click` | Intent toward pricing / main site |
| `plan_select` | Plan interest on landing (main site) |
| `contact_form_submit` | Contact form submitted (main site) |
| `qr_downloaded` | WhatsApp tool — high intent |
| `result_copied` | WhatsApp tool — engagement |
| `tool_card_click` | Nav from free-tools hub into a tool |
| `header_cta_click` | Plans CTA from tool headers |

## Optional derived events (Admin, no code)

Use **Create event** from an existing event (e.g. `page_view` or `tool_result_shown`) only when you need a *narrow* definition for Ads or reports. **Do not** modify the built-in `page_view` event globally (Google warns this breaks normal pageview collection).

Examples:

- `tool_completed_presence` ← `tool_result_shown` where parameter `tool_name` = `presence_score`
- `pricing_cta_from_tool` ← `cta_click` where `location` = `tool_funnel`

## Parameters to use in reports / audiences

Common custom dimensions worth registering (GA4 → Admin → Custom definitions):

- `tool_name`
- `language` / `language_to`
- `location` / `section` (on `cta_click`, `nav_click`, etc.)
- `plan` (on `plan_select`, `payback_result_shown`)

## Verification

1. Open the site with `?_dbg=1` and use **DebugView** (if configured) or **Realtime**.
2. Run through: home → free tools → one tool → result → CTA.
3. Confirm event names and parameters match expectations.

Repo guard: `bash scripts/check-html-ga.sh` ensures every HTML entry page includes gtag + `assets/js/analytics.js`.
