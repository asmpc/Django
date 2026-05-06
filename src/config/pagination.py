from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from math import ceil



# class CustomPagination(PageNumberPagination):
#     page_size = 10
#     def get_paginated_response(self, data):
#         return Response({
#             'count': self.page.paginator.count,
#             'pages': ceil(self.page.paginator.count // self.page_size),
#             'page': self.page.number,
#             'results': data,
#         })

class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'  # ?page_size=...
    max_page_size = 50

    def get_paginated_response(self, data):
        page_size = self.get_page_size(self.request)
        return Response({
            'count': self.page.paginator.count,
            'pages': ceil(self.page.paginator.count // self.page_size),
            'current_page': self.page.number,
            'page_size': page_size,
            'results': data,
        })