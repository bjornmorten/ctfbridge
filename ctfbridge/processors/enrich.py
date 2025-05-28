from ctfbridge.processors.registry import get_all_parsers


class ChallengeEnricher:
    def __init__(self):
        self.parsers = get_all_parsers()

    def parse(self, challenge):
        for parser in self.parsers:
            challenge = parser.apply(challenge)
        return challenge


enricher = ChallengeEnricher()


def enrich_challenge(challenge):
    return enricher.parse(challenge)
