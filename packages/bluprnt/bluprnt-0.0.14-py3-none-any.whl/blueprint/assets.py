def workspace(**kwargs):
    return "workspaces/{wid}".format(**kwargs)


def configuration(**kwargs):
    return "workspaces/{wid}/configurations/{cid}".format(**kwargs)


def state(**kwargs):
    return "workspaces/{wid}/configurations/{cid}/states/{sid}".format(**kwargs)


def paramSet(**kwargs):
    return "workspaces/{wid}/configurations/{cid}/states/{sid}/paramSets/{psid}".format(**kwargs)
