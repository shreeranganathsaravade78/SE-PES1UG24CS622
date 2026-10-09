import random
from words import WORDS, HINTS
from stats import SessionStats

DIFFICULTIES = {
    "easy": {"lives": 8, "win_points": 3, "hint_penalty": 1},
    "medium": {"lives": 6, "win_points": 5, "hint_penalty": 1},
    "hard": {"lives": 4, "win_points": 8, "hint_penalty": 2},
}


class HangmanGame:
    def __init__(self):
        self.stats = SessionStats()
        self.difficulty = "medium"
        self.score = 0
        self.streak = 0
        self.category = "technology"
        self.secret = ""
        self.guessed = set()
        self.wrong = set()
        self.lives = 6
        self.hint_used = False

    def start_round(self):
        self.secret = random.choice(WORDS[self.category])
        self.guessed.clear()
        self.wrong.clear()
        self.lives = DIFFICULTIES[self.difficulty]["lives"]
        self.hint_used = False

    def masked(self):
        return " ".join(ch if ch in self.guessed else "_" for ch in self.secret)

    def won(self):
        return all(ch in self.guessed for ch in set(self.secret))

    def guess(self, letter):
        if len(letter) != 1 or not letter.isalpha():
            return "Enter one letter."
        if letter in self.guessed or letter in self.wrong:
            return "Already guessed."
        if letter in self.secret:
            self.guessed.add(letter)
            return "Correct."
        self.wrong.add(letter)
        self.lives -= 1
        return "Wrong."

    def use_hint(self):
        if self.hint_used:
            return None
        self.hint_used = True
        penalty = DIFFICULTIES[self.difficulty]["hint_penalty"]
        self.score = max(0, self.score - penalty)
        return HINTS.get(self.secret, "No hint available.")

    def play_round(self):
        self.start_round()
        while self.lives > 0 and not self.won():
            print("\nWord:", self.masked())
            print("Wrong:", " ".join(sorted(self.wrong)) or "-")
            print("Lives:", self.lives, "Score:", self.score, "Streak:", self.streak)
            raw = input("Letter, /hint, or /quit: ").strip().lower()

            if raw == "/quit":
                return False
            if raw == "/hint":
                hint = self.use_hint()
                print("Hint already used." if hint is None else hint)
                continue
            if raw.startswith("/"):
                print("Unknown command.")
                continue

            print(self.guess(raw))

        if self.won():
            self.streak += 1
            win_points = DIFFICULTIES[self.difficulty]["win_points"]
            self.score += win_points + self.streak
            self.stats.record(True, self.streak)
            print("Solved:", self.secret)
            return True

        self.streak = 0
        self.stats.record(False, self.streak)
        print("Out of lives. The word was:", self.secret)
        return True

    def print_session_stats(self):
        print("\n--- Session Statistics ---")
        print("Rounds played:", self.stats.rounds)
        print("Rounds won:", self.stats.wins)
        print("Best streak:", self.stats.best_streak)

    def run(self):
        print("Hangman Challenge")
        print("A session consists of multiple rounds.")

        while True:
            print("\nCategories:", ", ".join(WORDS))
            raw = input("Choose category or q to quit: ").strip().lower()

            if raw == "q":
                self.print_session_stats()
                return
            if raw not in WORDS:
                print("Unknown category.")
                continue

            self.category = raw
            print("\nDifficulties:", ", ".join(DIFFICULTIES))

            while True:
                difficulty = input("Choose difficulty or q to quit: ").strip().lower()

                if difficulty == "q":
                    self.print_session_stats()
                    return
                if difficulty not in DIFFICULTIES:
                    print("Invalid difficulty. Choose easy, medium, or hard.")
                    continue

                self.difficulty = difficulty
                break

            if not self.play_round():
                self.print_session_stats()
                return

            again = input("Another round? [y/n]: ").strip().lower()
            if again != "y":
                print("Final score:", self.score, " Streak:", self.streak)
                self.print_session_stats()
                return


if __name__ == "__main__":
    HangmanGame().run()
