def auto_debug(fd):
    for v in fd.vertices:
        v.with_label(f"{v.id} {{\\{{{v.x:.2g},{v.y:.2g}\\}}}}")
    for p in fd.propagators:
        p.with_label(f"{p.id}")
    for leg in fd.legs:
        leg.with_label(f"{leg.id} {{\\{{{leg.x:.2g},{leg.y:.2g}\\}}}}")
