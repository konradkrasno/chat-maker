class Parser:
    def __init__(self, user_resp) -> None:
        self.user_response = user_resp

    def parse(self) -> str:
        return self.user_response


class ContainsItemsParser(Parser):
    def __init__(self, user_resp: str) -> None:
        super().__init__(user_resp)

    def __repr__(self):
        return "ContainsItemsParser"


class SearchItemParser(Parser):
    def __init__(self, user_resp: str) -> None:
        super().__init__(user_resp)

    def __repr__(self):
        return "SearchItemParser"


class AddressParser(Parser):
    def __init__(self, user_resp: str) -> None:
        super().__init__(user_resp)

    def __repr__(self):
        return "AddressParser"


class TimeParser(Parser):
    def __init__(self, user_resp: str) -> None:
        super().__init__(user_resp)

    def __repr__(self):
        return "TimeParser"


UserPhraseParserMapping = {
    "ContainsItems": ContainsItemsParser,
    "SearchItem": SearchItemParser,
    "Address": AddressParser,
    "Time": TimeParser,
}
