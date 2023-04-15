class ASCIIPoint:
    def __init__(
        self,
        symbol="",
    ):
        self.symbol = symbol

    def draw(
        self, pane, itar, scalex=1, scaley=1, kickx=0, kicky=0, colorer=lambda x: x
    ):
        # width = len(pane[0])
        # height = len(pane)
        # TODO normalize to width and height as well
        tarx = int((itar.x + kickx) * scalex)
        tary = int((itar.y + kicky) * scaley)

        if self.symbol is not None and self.symbol != "":
            pane[tary][tarx] = colorer(self.symbol)
