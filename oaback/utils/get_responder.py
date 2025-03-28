def get_responder(request):
    user = request.user
    if user.has_role("admin"):
        responder = None
    if user.has_role("manager"):
        responder= user.get_admin_users()
    else:
        responder = user.department.leader
    return responder