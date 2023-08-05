def account(aid):
    return ["accounts", aid]

def configuration(aid, cid):
    return ["accounts", aid, "configurations", cid]

def workspace(aid, cid, wid):
    return ["accounts", aid, "configurations", cid, "workspaces", wid]

def plain_params(aid, cid, wid):
    return ["accounts", aid, "configurations", cid, "workspaces", wid, "params", "plain"]

def encrypted_params(aid, cid, wid):
    return ["accounts", aid, "configurations", cid, "workspaces", wid, "params", "encrypted"]