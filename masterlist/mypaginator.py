from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class MyPaginator:
    query_set = ''
    items_per_page = 0
    page = 0
    count = 0

    def __init__(self, query_set, items_per_page, page):
        self.query_set = query_set
        self.items_per_page = items_per_page
        self.page = page

    def get_paginated_result(self):
        paginated_result = ''
        paginator = Paginator(self.query_set, self.items_per_page)
        page = self.page

        try:
            paginated_result = paginator.page(page)
        except PageNotAnInteger:
            paginated_result = paginator.page(1)
        except EmptyPage:
            paginated_result = paginator.page(paginator.num_pages)

        self.count = paginator.count
        return paginated_result

    def get_result_count(self):
        return self.count

    class Meta:
        ordering = ['-date_modified']
