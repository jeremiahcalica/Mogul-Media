# Optional: run each client's autopilot inside the client's Claude project

In Loom 1, the brief is written in a new chat **inside the client's project** (e.g. "Mason L."), so Claude also has that project's files.

The main routine runs outside the projects:
- It writes the same brief, and reads the Client Brain and feedback ledger from Drive and Claude Docs instead.
- A routine can't be attached to a project from here.

If you want every brief chat to sit in its project, add one scheduled task per client from the project itself. Repeat for each client you want this for:

1. Open the client's project, e.g. "Mason L.".
2. In the right-hand panel, open **Scheduled › Add**.
3. Set it to run daily at 9:52 PM. Any time after the main routine works.
4. Paste this prompt, with the client's schedule name (Mason, Josh C, Keval, …):

```
/longform-batch-autopilot

One client: Mason. This is an unattended scheduled run inside the client's project: never stop to ask; decide, note it, keep going. Skip Step 1.0 (don't message the schedule chat).

Jeremiah authorizes these writes, and only these: create this week's post-call topic brief Claude Doc if it doesn't exist yet; copy last week's longform doc into his My Drive as this week's if it doesn't exist yet, and edit only that copy; append to "Longform Autopilot — Run Log". Everything else is read-only.

Use this project's files (Client Brain, feedback ledger, voice notes) for names and sensitivities only, never as a source of quotes.

End with a summary of at most 4 lines.
```

If you add these, the main routine still runs. It skips whatever the project task already made, because each run first checks what exists.
