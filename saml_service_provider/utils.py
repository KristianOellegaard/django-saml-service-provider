def prepare_from_django_request(request):
    return {
        'http_host': request.META['HTTP_HOST'],
        'script_name': request.META['PATH_INFO'],
        'server_port': request.META.get('HTTP_X_FORWARDED_PORT', request.META['SERVER_PORT']),
        'get_data': request.GET.copy(),
        'post_data': request.POST.copy()
    }