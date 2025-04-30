from ctfbridge.services import AttachmentService


class DemoAttachmentService(AttachmentService):
    """
    Service for handling file downloads for attachments.
    """

    def __init__(self, client):
        super().__init__(client)