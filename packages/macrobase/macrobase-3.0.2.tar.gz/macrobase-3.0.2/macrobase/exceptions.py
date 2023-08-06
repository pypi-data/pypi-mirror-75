class MacrobaseException(Exception):
    message = 'Macrobase error'


class UnexpectedDriverException(Exception):
    message = 'Unexpected drivers'


class HookException(MacrobaseException):
    message = 'Hook error'
