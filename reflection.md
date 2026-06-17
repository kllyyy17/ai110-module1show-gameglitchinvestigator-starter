# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  1. It told me to 'Go LOWER!' when I was supposed to guess higher (the hints were backwards).
  2. I couldn't start over the game — "New Game" didn't reset the game's status.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess of 50 (secret was 62) | 'Go HIGHER!' hint | 'Go LOWER!' hint shown | none |
| Guess of 75 (secret was 76) | 'Go HIGHER!' hint | 'Go LOWER!' hint shown | none |
| Guess of 77 (secret was 76) | 'Go LOWER!' hint | 'Go HIGHER!' hint shown | none |
| Click "New Game" after winning or losing | Fresh game starts, I can guess again | "You already won. Start a new game to play again." message stays, input is locked | none |
| Same guess of 100 on attempt 1, then again on attempt 2 (secret 62) | Same hint both times | Hint flips between attempts (string-vs-number comparison) | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude Code in agent mode, letting it read `app.py` and `logic_utils.py` and edit directly while I reviewed each change. A correct suggestion was diagnosing the backwards hints as swapped high/low messages and fixing `check_guess` so "Too High" points LOWER and "Too Low" points HIGHER, which I verified by running pytest and seeing the direction tests pass for the "secret 62, guess 50" case. A misleading one was that when it moved `check_guess` into `logic_utils.py` it kept the old `except TypeError` branch that compares the secret as text, so the fix looked finished but left the string-vs-number bug in place, which I caught because its tests were marked `xfail` (failing) — we later fixed it for real by always comparing numerically.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was really fixed only when a test that targeted it passed, instead of trusting that the code "looked right." One test I ran was `test_reported_glitch_scenario` in `tests/test_game_logic.py`, which calls `check_guess(50, 62)` and asserts the outcome is "Too Low" with a hint to go HIGHER; it passed after the fix but would have failed before, which proved the backwards-hint bug was gone. AI helped a lot here — Claude generated the pytest file, first using `xfail` markers to flag the bugs that weren't fixed yet, and once I fixed everything the whole suite passed (12 tests), which made it obvious the bugs were truly resolved.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
