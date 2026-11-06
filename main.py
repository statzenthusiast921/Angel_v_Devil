import os
from debate.crew import ShoulderDebate
from pathlib import Path
from dotenv import load_dotenv


env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path, override=True)

os.makedirs('output', exist_ok=True)


def show(angel_text, devil_text, header):
    print(f"\n ***** {header} *****")
    print(f"\n ANGEL:\n{angel_text}")
    print(f"\n DEVIL:\n{devil_text}\n")


def get_issue():
    while True:
        issue = input("What's your issue?\n> ").strip()
        if issue:
            return issue
        print("Please describe your issue to get started.")


def run():
    issue = get_issue()

    # ***** Round 1: opening arguments *****
    result = ShoulderDebate().opening_crew().kickoff(inputs={'issue': issue})
    angel_text = result.tasks_output[0].raw
    devil_text = result.tasks_output[1].raw

    transcript = f"ANGEL: {angel_text}\n\nDEVIL: {devil_text}"
    show(angel_text, devil_text, "OPENING ARGUMENTS")

    # ***** Additional rounds: I provide feedback, they respond *****
    round_num = 1
    while True:
        feedback = input(
            "Your feedback for the angel and devil "
            "(or just press Enter when you're ready to decide):\n> "
        ).strip()
        if not feedback:
            break

        round_num += 1
        result = ShoulderDebate().rebuttal_crew().kickoff(inputs={
            'issue': issue,
            'transcript': transcript,
            'feedback': feedback,
        })
        angel_text = result.tasks_output[0].raw
        devil_text = result.tasks_output[1].raw

        transcript += (
            f"\n\nHUMAN: {feedback}"
            f"\n\nANGEL: {angel_text}"
            f"\n\nDEVIL: {devil_text}"
        )
        show(angel_text, devil_text, f"ROUND {round_num}")

    # ***** Your decision *****
    decision = input("\nOkay, it's your call. What do you decide?\n> ").strip()
    transcript += f"\n\nFINAL DECISION (HUMAN): {decision}"

    with open('output/transcript.md', 'w', encoding='utf-8') as f:
        f.write(f"# Issue\n{issue}\n\n# Transcript\n{transcript}\n")

    print("\nDecision made. Transcript saved to output/transcript.md")


if __name__ == "__main__":
    run()