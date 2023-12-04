import bot, init
from spacy.matcher import Matcher

client = bot.client
matcher = Matcher(init.nlp.vocab)


def init_matcher():
    """
    Add patterns to matcher based on init. patterns. Patterns are sorted alphabetically by their index so we don't have to worry about order
    """
    for i, pattern in enumerate(init.patterns):
        matcher.add("HelpRequest{}".format(i), [pattern])
