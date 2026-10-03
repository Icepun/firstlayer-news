# First Layer: main menu announcements

The **Workshop News** column on the right of the main menu is driven by a single file on the server. Adding, changing or removing an announcement **does not need a game update**: just change the file.

```
https://news.vitrumgames.com/first-layer/announcements.json
```

## How it works

- When the main menu opens, the game instantly shows **the last copy saved on the device**. If there is none, it shows the copy bundled with the game. It then downloads the file from the server; if the file is valid, the menu refreshes with a soft transition and the new copy is saved.
- If there is no internet, the server is down or the file is broken, players see **the last valid copy**. No error is shown.
- A change reaches players within **5–10 minutes** (server cache). Players who are already in the menu see it the next time they open it.
- Order: the **pinned** announcement comes first, then the newest by date. The first announcement appears in the large card with an image; the next two appear as short rows.
- Announcements the player hasn't opened show an orange **NEW** badge. On a player's very first launch nothing counts as new.

## Setup

This repository publishes the file with GitHub Pages, on our own domain:

- It is free, keeps a change history and the file can be edited in the browser.
- **A broken file never goes live.** Every commit is checked automatically; if the check fails, the previous valid version stays online.
- Because the game uses our own domain, moving the hosting later only needs a DNS change, not a game update.

Settings (if it ever needs to be rebuilt):

1. **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. **Settings → Pages → Custom domain:** `news.vitrumgames.com`, with **Enforce HTTPS** on.
3. A **CNAME** record for `news` in the Hostinger DNS → `icepun.github.io`.
4. In Unity, run **Tools → Printing Sim → Main Menu → Check Live Announcements**. The Console should say `Announcements OK`.

## Adding or changing an announcement

1. On GitHub, open `site/first-layer/announcements.json` and click the pencil icon (Edit).
2. Make your changes, then click **Commit changes**.
3. Check the **Actions** tab:
   - **Green check:** live within 1–2 minutes.
   - **Red cross:** the file has an error and the previous version stays live. Open the run to see what is wrong.
4. Optionally, run **Check Live Announcements** in Unity to see what players see right now.

To check the file locally: `python tools/validate.py site/first-layer/announcements.json`

## Fields

| Field | Required | Description |
| --- | --- | --- |
| `id` | yes | Unique and **permanent** ID. The NEW badge depends on it. Use a new `id` for a new announcement; keep the same `id` when you fix one. |
| `title` | yes | Title. Up to 2 lines on the card (about 45 characters). |
| `summary` | | Short text on the card and in the rows (about 120 characters). |
| `body` | | Full text shown by "Read". Use `\n\n` for paragraphs and `• ` for bullets. |
| `category` | | Small orange label, e.g. `Update`, `Event`, `Roadmap`. |
| `date` | | Format `2026-10-04`. Shown as `OCT 4, 2026` on the card and used for ordering. |
| `pinned` | | If `true`, the announcement is always first, in the large card. |
| `image` | | Image URL starting with `https://`. Recommended 16:9, 1280×720, at most 4 MB. It is downloaded and stored on the device. Without it, the game's default image is used. |
| `link` | | Link starting with `https://`, shown as a button when the announcement is opened. |
| `linkLabel` | | Text of the link button, e.g. `Join our Discord`. |
| `start` / `end` | | Publishing window (UTC), e.g. `2026-10-10` or `2026-10-10T18:00:00Z`. An `end` with only a date lasts until the end of that day. The announcement appears and disappears on its own. |
| `minVersion` / `maxVersion` | | Game versions that see the announcement, e.g. `"maxVersion": "0.1.9"` for an update notice to older versions. |
| `tr` / `pl` | | Translations of `category`, `title`, `summary`, `body` and `linkLabel`. Empty fields fall back to English. The game picks them by the player's language. |

Formatting tags (`<b>` etc.) are not applied; they show as plain text. Unknown fields are ignored. The game reads up to 12 announcements.

## Example

```json
{
  "schema": 1,
  "announcements": [
    {
      "id": "printathon-2026-10",
      "pinned": true,
      "date": "2026-10-10",
      "start": "2026-10-10",
      "end": "2026-10-12",
      "category": "Event",
      "title": "Print-a-thon weekend",
      "summary": "Share your best print on Discord this weekend. The community picks a favourite.",
      "body": "Post a screenshot of your best print in #showcase.\n\nWe will feature the winner here next week.",
      "image": "https://news.vitrumgames.com/first-layer/images/printathon.jpg",
      "link": "https://discord.gg/ANR3mNuerB",
      "linkLabel": "Join our Discord"
    }
  ]
}
```

Images can live in this repository too: `site/first-layer/images/` → `https://news.vitrumgames.com/first-layer/images/...`

## Tips

- **Remove:** delete the announcement from the list, or give it an `end` date.
- **Schedule:** set a future `start` date. The announcement appears on its own when the day comes.
- **Bundled copy:** before a new build, sync `Assets/6_SO/UI/Announcements_Default.json` in the game project with this file. **Tools → Printing Sim → Main Menu → Check Bundled Announcements** checks it.
