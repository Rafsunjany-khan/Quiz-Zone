def auth_status(request):
    return {
        'logged_in': request.user.is_authenticated
    }
