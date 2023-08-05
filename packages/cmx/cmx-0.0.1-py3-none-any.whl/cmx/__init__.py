from cmx.backends.markdown import CommonMark

cm = CommonMark()


def config(mode=None, target=None):
    global cm

    if mode == "local":
        cm = None
