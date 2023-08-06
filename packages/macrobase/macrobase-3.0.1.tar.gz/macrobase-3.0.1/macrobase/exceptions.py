class MacrobaseException(Exception):
    message = 'Macrobase error'


class HookException(MacrobaseException):
    message = 'Hook error'
