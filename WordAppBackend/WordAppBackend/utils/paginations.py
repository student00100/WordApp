from rest_framework.pagination import PageNumberPagination


class GlobalPagination(PageNumberPagination):
    # 项目中默认的分页配置
    page_size = 30  # 每页显示条数
    page_size_query_param = 'size'  # 前端发送每页显示的数目
    max_page_size = 1000  # 前端最多能够设置每页的数量
