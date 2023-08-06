# -*- coding:utf-8 -*- 
__author__ = 'denishuang'

def get_user_scope_map(user):
    roles = list(user.saas_roles.all())
    if not roles:
        return
    rsm = {}
    for r in roles:
        rsm.update(r.permissions)
    return rsm