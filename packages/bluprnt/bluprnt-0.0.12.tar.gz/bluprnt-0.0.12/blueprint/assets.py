def account(**kwargs):
    return "accounts/{aid}".format(**kwargs)


def configuration(**kwargs):
    return "accounts/{aid}/configurations/{cid}".format(**kwargs)


def workspace(**kwargs):
    return "accounts/{aid}/configurations/{cid}/workspaces/{wid}".format(**kwargs)


def paramSet(**kwargs):
    return "accounts/{aid}/configurations/{cid}/workspaces/{wid}/paramSets/{psid}".format(**kwargs)
