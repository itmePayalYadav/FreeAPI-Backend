from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size_query_param = "page_size"  

    def get_paginated_response(self, data):
        return Response(
            {
                "success": True,
                "message": "Paginated results",
                "pagination": {
                    "current_page": self.page.number,
                    "total_pages": self.page.paginator.num_pages,
                    "total_items": self.page.paginator.count,
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "data": data,
            }
        )
