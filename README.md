# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.** It's a Streamlit number-guessing game. The app picks a secret number within a range that depends on the difficulty (Easy 1–20, Normal 1–100, Hard 1–50). The player types guesses, gets a "higher/lower" hint after each one, earns or loses points, and wins when they guess the secret before running out of attempts.

- [x] **Detail which bugs you found.**
  - **Backwards hints:** "Too High" told the player to go HIGHER and "Too Low" told them to go LOWER, so the hints pointed away from the answer.
  - **Couldn't restart:** "New Game" only reset the attempts and secret, not the game status, so after a win/loss the game stayed locked.
  - **String-vs-number comparison:** on even-numbered attempts the secret was compared as text (`"9" > "62"`), so the same guess could flip its hint between attempts.
  - **Scoring glitch:** a wrong "Too High" guess on even attempts secretly *added* points, and the win bonus had an off-by-one.
  - **Minor UI:** the prompt always said "between 1 and 100" even on Easy/Hard, and the "Attempts left" counter started off by one.

- [x] **Explain what fixes you applied.**
  - Corrected the hint direction so "Too High" → Go LOWER and "Too Low" → Go HIGHER.
  - Made `check_guess` always compare numerically (and removed the even-attempt stringify in `app.py`).
  - Made "New Game" reset *all* state (status, score, history, attempts, secret) and use the difficulty's range.
  - Made every wrong guess cost 5 points and fixed the win-bonus off-by-one.
  - Showed the real difficulty range in the prompt and started the attempts counter at 0.
  - Refactored all game logic into `logic_utils.py` and added a `pytest` suite covering the fixes.

## 📸 Demo Walkthrough

A text-based walkthrough of a sample game on **Normal** difficulty (secret = **62**), so a reader can follow the end-to-end behavior without running it:

1. The app starts a new game and picks a hidden secret (62). The sidebar shows "Range: 1 to 100" and "Attempts left: 8". Score starts at **0**.
2. User enters a guess of **40** → game returns **"Too Low" → 📈 Go HIGHER!** (40 is below 62). Score updates to **-5**.
3. User enters a guess of **70** → game returns **"Too High" → 📉 Go LOWER!** (70 is above 62). Score updates to **-10**.
4. User enters a guess of **55** → game returns **"Too Low" → 📈 Go HIGHER!** (still below 62). Score updates to **-15**.
5. User enters a guess of **62** → game returns **"🎉 Correct!"**, balloons appear, and the win bonus is added (100 − 10 × attempt 4 = 60), bringing the final score to **45**.
6. The game ends and shows "You won! The secret was 62." Clicking **New Game 🔁** fully resets the game (new secret, score back to 0, status back to playing) so the player can immediately start again.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
