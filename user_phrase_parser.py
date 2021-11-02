class Parser:
    def __init__(self, user_resp) -> None:
        self.user_response = user_resp

    def parse(self) -> str:
        return self.user_response


class ContainsItemsParser(Parser):
    def __init__(self, user_resp: str) -> None:
        super().__init__(user_resp)


class SearchItemParser(Parser):
    def __init__(self, user_resp: str) -> None:
        super().__init__(user_resp)


class AdressParser(Parser):
    def __init__(self, user_resp: str) -> None:
        super().__init__(user_resp)


class TimeParser(Parser):
    def __init__(self, user_resp: str) -> None:
        super().__init__(user_resp)


UserPhraseParserMapping = {
    "ContainsItems": ContainsItemsParser,
    "SearchItem": SearchItemParser,
    "Adress": AdressParser,
    "Time": TimeParser,
}
