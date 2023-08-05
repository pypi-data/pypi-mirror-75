from PyQt5.uic import uiparser

# https://stackoverflow.com/a/62629256
uiparser.WidgetStack.topIsLayoutWidget = lambda self: False
