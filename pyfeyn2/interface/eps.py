import re

from feynml import FeynmanDiagram, FeynML, Head, Leg, Meta, Propagator, Vertex

# TODO move this to feynml interface module

# MadGraph
def eps_to_feynml(filename: str, Nincoming=2):
    """Read Feynman diagram from eps file"""

    # read full file into string list
    lines = ""
    with open(filename, "r") as f:
        lines = "".join(f.readlines())
    # drop all before "%%PageFonts: Helvetica"
    # print(lines)
    reg = re.search(r".*%%PageFonts: Helvetica(.*)%%trailer.*", lines, flags=re.DOTALL)
    # print(reg.group(1))
    diags = reg.group(1).split("diagram")
    # print(diags)
    diagrams = []
    idd = 0
    for d in diags:
        vertices = []
        lines = []
        legs = []
        props = []
        ll = d.split("\n")
        for i, l in enumerate(ll):
            match = re.search(
                r"([0-9\.]+)\s([0-9\.]+)\s([0-9\.]+)\s([0-9\.]+)\s([0-9\.]+)?\s?F([a-zA-Z]+).*",
                l,
                flags=re.DOTALL,
            )
            match2 = (
                re.search(r"\((.+)\)\s+show.*", ll[i + 2]) if i + 2 < len(ll) else None
            )
            match3 = (
                re.search(r"\(([0-9]+)\)\s+show.*", ll[i + 4])
                if i + 4 < len(ll)
                else None
            )
            if match:
                x1, y1, x2, y2 = (
                    round(float(match.group(1)), 5),
                    round(float(match.group(2)), 5),
                    round(float(match.group(3)), 5),
                    round(float(match.group(4)), 5),
                )
                line = match.group(6)
                idd += 1
                id1 = idd
                for v in vertices:
                    if x1 == v.x and y1 == v.y:
                        id1 = v.id
                        v1 = v
                        break
                if id1 == idd:
                    vertices.append(v1 := Vertex(id=id1, x=x1, y=y1))
                idd += 1
                id2 = idd
                for v in vertices:
                    if x2 == v.x and y2 == v.y:
                        id2 = v.id
                        v2 = v
                        break
                if id2 == idd:
                    vertices.append(v2 := Vertex(id=id2, x=x2, y=y2))
                idd += 1
                plabel = None
                num = None
                if match2:
                    plabel = match2.group(1)
                    if plabel == "a":
                        plabel = "gamma"
                    if plabel == "z":
                        plabel = "Z0"
                if match3:
                    num = int(match3.group(1))
                lines.append([idd, v1, v2, line, "prop", plabel, num])
        for l1 in lines:
            inc = True
            exl = True
            for l2 in lines:
                if l1 != l2:
                    if l1[1] == l2[1] or l1[1] == l2[2]:
                        inc = False
                    if l1[2] == l2[1] or l1[2] == l2[2]:
                        exl = False
            if inc:
                l1[4] = "incoming" if l1[6] <= Nincoming else "outgoing"
                if l1[4] == "outgoing":
                    if l1[3] == "fermion":
                        l1[3] = "anti fermion"
                legs.append(
                    Leg(
                        id=l1[0],
                        x=l1[1].x,
                        y=l1[1].y,
                        target=l1[2].id,
                        sense=l1[4],
                        type=l1[3],
                        name=l1[5],
                    )
                )
                vertices.remove(l1[1])
            elif exl:
                l1[4] = "incoming" if l1[6] <= Nincoming else "outgoing"
                if l1[4] == "incoming":
                    if l1[3] == "fermion":
                        l1[3] = "anti fermion"
                legs.append(
                    Leg(
                        id=l1[0],
                        x=l1[2].x,
                        y=l1[2].y,
                        target=l1[1].id,
                        sense=l1[4],
                        type=l1[3],
                        name=l1[5],
                    )
                )
                vertices.remove(l1[2])
            elif not inc and not exl:
                props.append(
                    Propagator(
                        id=l1[0], source=l1[1], target=l1[2], type=l1[3], name=l1[5]
                    )
                )
            elif inc and exl:
                raise Exception("Unknown sense, seems stray")
            else:
                raise Exception("Unknown line case")
        diagrams.append(FeynmanDiagram().add(*vertices, *legs, *props))

    fml = FeynML(
        head=Head(
            metas=[
                Meta(name="pyfeyn2", content="test"),
                Meta(name="description", content="Simple single test diagram"),
            ],
        ),
        diagrams=diagrams,
    )
    return fml
