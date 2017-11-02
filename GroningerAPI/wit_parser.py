from wit import Wit

WIT_ACCESS_TOKEN='GE3WFS7X5FGREBMX7WA46XIHMO2ES7WC'

class WitParser:
    def __init__(self):
        self.client = Wit(access_token=WIT_ACCESS_TOKEN)

    def parse(self, message):
        return self.client.message(message)
