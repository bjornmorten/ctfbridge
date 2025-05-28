from ctfbridge.models.challenge import Attachment, Challenge
from ctfbridge.parsers.base import BaseChallengeParser
from ctfbridge.parsers.helpers.url_classifier import classify_links
from ctfbridge.parsers.helpers.url_extraction import extract_links
from ctfbridge.parsers.registry import register_parser


@register_parser
class AttachmentExtractor(BaseChallengeParser):
    def apply(self, challenge: Challenge) -> Challenge:
        if challenge.attachments or not challenge.description:
            return challenge

        urls = extract_links(challenge.description)
        urls = classify_links(urls)["attachments"]
        challenge.attachments = [
            Attachment(name=url.split("/")[-1].split("?")[0], url=url) for url in urls
        ]
        return challenge
