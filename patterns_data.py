# Define a list of common words for each category
question_words = ["how", "what", "why", "where", "when"]
action_words = ["find", "get", "seek", "receive", "obtain"]
help_words = ["help", "assistance", "aid", "support"]
need_words = ["need", "require"]
greeting_words = ["hello", "hi", "hey"]
status_words = ["am", "was", "have"]
difficulty_words = ["stuck", "unable", "can't", "cannot"]
understanding_words = ["figure", "understand"]

# Define the patterns using the lists of words
patterns = [
    # Pattern for asking a question
    [
        {"LOWER": {"IN": question_words}},
        {"LOWER": "can"},
        {"LOWER": "i"},
        {"LOWER": {"IN": action_words}},
        {"LOWER": {"IN": ["some", "any"]}, "OP": "?"},
        {"LOWER": {"IN": help_words}},
    ],
    # Pattern for requesting assistance
    [
        {"LOWER": "i"},
        {"LOWER": {"IN": need_words}},
        {"LOWER": {"IN": ["some", "any"]}, "OP": "?"},
        {"LOWER": {"IN": help_words}},
        {"LOWER": "with"},
        {"POS": {"IN": ["NOUN", "VERB"]}},
    ],
    # Pattern for being stuck or unable to do something
    [
        {"LOWER": {"IN": greeting_words}, "OP": "?"},
        {"LOWER": "i"},
        {"LOWER": {"IN": status_words}},
        {"LOWER": {"IN": difficulty_words}},
        {"LOWER": {"IN": understanding_words}, "OP": "?"},
        {"LOWER": "out"},
        {"POS": {"IN": ["NOUN", "VERB"]}, "OP": "?"},
    ],
    [
        {"LOWER": {"IN": ["please", "pls", "plz", "ples", "plis"]}},
        {"LOWER": "help"},
        {"LOWER": "me", "OP": "?"},
    ],
]
