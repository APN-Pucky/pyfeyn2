class ASCIILine:
    def __init__(
        self,
        style,
        begin=" ",
        end=" ",
    ):
        self.begin = begin
        self.end = end
        self.style = style

    def draw(
        self,
        pane,
        isrc,
        itar,
        scalex=1,
        scaley=1,
        kickx=0,
        kicky=0,
        colorer=lambda x: x,
        **kwargs,
    ):
        # width = len(pane[0])
        # height = len(pane)
        # TODO normalize to width and height as well
        srcx = int((isrc.x + kickx) * scalex)
        srcy = int((isrc.y + kicky) * scaley)
        tarx = int((itar.x + kickx) * scalex)
        tary = int((itar.y + kicky) * scaley)

        if abs(srcx - tarx) > abs(srcy - tary):
            for i in range(srcx, tarx, 1 if srcx < tarx else -1):
                v = self.style.next(tarx - srcx, tary - srcy)
                if v is not None:
                    pane[round(srcy + (tary - srcy) * (i - srcx) / (-srcx + tarx))][
                        i
                    ] = colorer(v)
        else:
            for i in range(srcy, tary, 1 if srcy < tary else -1):
                v = self.style.next(tarx - srcx, tary - srcy)
                if v is not None:
                    pane[i][
                        round(srcx + (tarx - srcx) * (i - srcy) / (-srcy + tary))
                    ] = colorer(v)
        # call once to increase the index
        v = self.style.next(tarx - srcx, tary - srcy)

        if v is None:
            return
        if self.begin is not None and self.begin != "":
            pane[srcy][srcx] = colorer(self.begin)
        if self.end is not None and self.end != "":
            pane[tary][tarx] = colorer(self.end)
