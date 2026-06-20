# AI Usage & Design Write-up

I used AI to help me get started with the project structure, Flask setup, and some of the basic API and test code. It saved time on the boilerplate, but I made the decisions around how the system should work.

One decision I made was keeping events and ledger entries separate. Events are the raw actions coming into the system, while the ledger is the source of truth for all point transactions. This made it easier to handle duplicate events and keep a clear history of point movements.

For the rules engine, I chose a simple configuration-based approach instead of storing rules in the database. Since this is a small assignment, it felt like the simplest solution without adding unnecessary complexity.

I also used an append-only ledger rather than storing a balance directly. Calculating the balance from ledger entries may be slightly slower, but it provides a complete audit trail and makes it easier to trust the numbers.

One place where I had to correct the AI output was during API testing. The AI initially suggested using curl commands in PowerShell, but I ran into issues with JSON escaping and quotation marks. Instead of spending time debugging the command syntax, I switched to PowerShell's Invoke-RestMethod, which handled the JSON payloads more reliably. This made it easier to test the APIs and verify the responses.
