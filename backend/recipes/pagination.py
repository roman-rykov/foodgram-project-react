from rest_framework import pagination


class SizedPageNumberPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'
    max_page_size = 36
