# Telegram Topics Workspace Setup for Army Team

This guide sets up an `Army HQ` Telegram group with **Topics** enabled, so each department has its own thread and Hermes can route replies correctly.

> ⚠️ One Telegram bot token can only have **one live consumer** at a time. Each army profile uses its own bot token; do not share tokens across profiles.

---

## Step 1 — Create the Army HQ group

1. Open Telegram.
2. Tap **New Group**.
3. Name it `Army HQ`.
4. Add the `army-hq` bot during creation (you can add the other department bots later).

```
+----------------------------------+
|  New Group                       |
|  Group name: [ Army HQ       ]   |
|                                  |
|  Add members:                    |
|    [ army-hq bot    ] [+]        |
|    [ yourself       ] [+]        |
|                                  |
|  [       Create Group        ]   |
+----------------------------------+
```

---

## Step 2 — Enable Topics

1. Open the group.
2. Tap the group name → **Edit**.
3. Turn **Topics** **ON**.

Telegram converts the group to a **supergroup**.

```
+----------------------------------+
|  Army HQ  ⚙️                     |
|  Edit                            |
|    Group Type: Public/Private    |
|    Topics: [ ON  ]               |
|    Permissions...                |
+----------------------------------+
```

> If you do not see the Topics toggle, the group is already a supergroup or too small. Try creating a new group first.

---

## Step 3 — Disable bot Group Privacy

The bot must be able to read messages in **all** topics.

1. Message **@BotFather**.
2. Send `/mybots`.
3. Select the `army-hq` bot.
4. Choose **Group Privacy** → **Disable**.

```
+----------------------------------+
|  @BotFather                      |
|  /mybots                         |
|  -> army-hq                      |
|     -> Bot Settings              |
|        -> Group Privacy          |
|           [ Turn OFF / Disable ] |
+----------------------------------+
```

Repeat this for `army-marketing-head`, `army-dev-head`, and `army-research-head` bots.

---

## Step 4 — Create work topics

Create these topics inside `Army HQ`:

- `#general`
- `#marketing`
- `#dev`
- `#research`
- `#ceo-delegation`

```
+----------------------------------+
|  Army HQ 🎖️                      |
|  Topics:                         |
|    #general                      |
|    #marketing                    |
|    #dev                          |
|    #research                     |
|    #ceo-delegation               |
|                                  |
|  [ + New Topic ]                 |
+----------------------------------+
```

---

## Step 5 — Use topics as workspaces

When you post in a topic, Hermes scopes its reply to the same `message_thread_id`. This keeps each department's context clean.

Example in `#ceo-delegation`:

```
You: /army-ceo-delegate launch Q3 rebrand

Hermes (in #ceo-delegation):
  1. Created kanban task → army-research-head
  2. Created kanban task → army-marketing-head
  3. Created kanban task → army-dev-head
  4. Dispatched all three in parallel
```

```
+----------------------------------+
|  #ceo-delegation                 |
|  You: /army-ceo-delegate ...     |
|  Hermes: ✅ Task created ...      |
|          ✅ Dispatched ...        |
+----------------------------------+
```

---

## Step 6 — Verify topic isolation

Hermes uses **two separate memory layers**:

| Layer | Scope | Example |
|---|---|---|
| **User profile memory** (`USER.md`) | Cross-chat, cross-topic | Your name, preferences, "I have a cat named TestCat" |
| **Session transcript** | Per topic | "Meeting codename Alpha-7" discussed only in `#test-isolation` |

To verify that **session context is isolated per topic**, test with *session-only* information:

1. In `#test-isolation`, send:
   > 今次會議代號係 Alpha-7，記住佢。
2. In `#general`, send:
   > 今次會議代號係咩？

Expected result:

- `#test-isolation` remembers `Alpha-7`.
- `#general` does **not** know the codename — it only sees its own thread.

If you test with personal facts like "I have a cat named TestCat", Hermes may still answer in `#general` because that fact is stored in your user profile memory. That is intentional.

---

## Step 7 — Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Bot does not respond in group | Group Privacy is still ON | Disable it in @BotFather |
| No Topics toggle in group info | Group is not a supergroup | Recreate the group, then enable Topics |
| Replies land in `#general` instead of the source topic | `message_thread_id` missing | Make sure the bot is added as a member of the topic and Group Privacy is OFF |
| Two profiles fight over the same bot token | Token shared | Create one bot per profile via @BotFather |
| Gateway stuck at "Connecting to Telegram" | DNS-over-HTTPS fallback discovery hangs | The profile config already hard-codes fallback IPs; make sure `HERMES_TELEGRAM_DISABLE_FALLBACK_IPS=1` is set in `.env` |

---

## Next step

Type `/army-ceo-delegate` in `#ceo-delegation` to start delegating.
