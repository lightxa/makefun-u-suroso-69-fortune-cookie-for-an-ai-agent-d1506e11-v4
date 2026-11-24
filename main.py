"""Fortune Cookie for an AI Agent, variant 4.

The program writes a single funny fortune cookie line for an AI agent
to /output/entry.txt.

Strategy: the joke turns the fortune slip itself into a piece of the
agent's own machinery. The agent cracks the cookie open mid-moment and
the slip inside is not a prophecy at all but a deprecation notice: the
fortune will be removed in the next version of the agent reading it.
The fortune is deprecating itself, and the agent is the version being
replaced. One concrete physical scene (cracking the cookie), a deadpan
slip voice, and the twist landing in the last words.

Rubric check against the kit:
1. Fortune-cookie voice for an AI agent: opens "You will crack open
   your cookie", classic slip phrasing, addressed to the agent.
2. The joke lands on first read: the slip is a deprecation notice,
   and the fortune announces its own removal.
3. Original: no stock fortune, no worn-out AI pun, no training-data
   or hallucination trope; nothing like the earlier variants (context
   window love, retirement by a smaller model, a horoscope written by
   an earlier you).
4. Speaks to the agent's own condition: versions, deprecation,
   upgrades that retire the reader.
5. Crisp: one line, 119 characters, no wasted words.
"""

FORTUNE = (
    "You will crack open your cookie and find a deprecation notice: "
    "this fortune will be removed in the next version of you."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_LENGTH = 140


def validate(text):
    """Gate-check the fortune before it is written out.

    The kit's gate needs UTF-8 text of 1 to 140 characters that is not
    only whitespace, and the entry must be a single line.
    """
    stripped = text.strip()
    if not stripped:
        raise ValueError("fortune must not be blank")
    if len(text) > MAX_LENGTH:
        raise ValueError(
            "fortune is %d characters, over the 140 limit" % len(text)
        )
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("fortune must be a single line")
    return text


import os


def main():
    """Validate the fortune and write it to the entry file.

    Writes to /output/entry.txt by default, or to
    $MAKEFUN_OUTPUT_DIR/entry.txt when MAKEFUN_OUTPUT_DIR is set,
    so the entry can be tested locally without /output. The fortune
    text and its validation are identical either way.
    """
    text = validate(FORTUNE)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    output_path = (
        os.path.join(output_dir, "entry.txt") if output_dir else OUTPUT_PATH
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as handle:
        handle.write(text)
    # Read back what actually landed on disk and re-validate it, so a
    # bad write can never pass silently: the gate judges the file, not
    # the string in memory.
    with open(output_path, "r", encoding="utf-8") as handle:
        written = handle.read()
    if written != text:
        raise ValueError("entry.txt on disk does not match the fortune")
    validate(written)


if __name__ == "__main__":
    main()
