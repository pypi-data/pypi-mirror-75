import math
import json
from itertools import chain


class Page(object):
    def __init__(self, items, current_page, per_page, max_page, count):
        # 分页后的记录集
        self.items = items
        # 当前页
        self.current_page = current_page
        # 每页记录数
        self.per_page = per_page
        # 总页数
        self.max_page = max_page
        # 总记录数
        self.count = count

    def params(self, response_data=None):
        """
        分页数据
        :param response_data:
        :return:
        """
        if not response_data:
            response_data = {}
        response_data['current_page'] = self.current_page
        response_data['per_page'] = self.per_page
        response_data['max_page'] = self.max_page
        response_data['count'] = self.count
        return response_data


def paginator(flask_request, items, items_additional=None) -> Page:
    """
    分页器
    :param request: {current_page, page_size}
    :param items: 记录集
    :param items_additional: None 附加记录集
    :return:
    """
    request_data = flask_request.get_json(silent=True)
    # request_data = json.loads(request.body.decode('utf-8'))

    # 接收前端分页参数
    # 当前页
    current_page = request_data.get('current_page', 1)
    # 每页记录数
    page_size = request_data.get('page_size', 10)
    # 总记录数
    # items_ids = items.values_list('uuid')
    items_count = items.count()
    # 附加记录集
    if items_additional:
        # items_additional_ids = items_additional.values_list('uuid')
        items_count += items_additional.count()
        items = list(chain(items, items_additional))

    # 总页数
    items_max_page = int(math.ceil(items_count / page_size))

    if int(current_page) <= int(items_max_page):
        start_page_index = (current_page - 1) * page_size
    else:
        start_page_index = 0

    # 记录集分页
    items_page = items[start_page_index: start_page_index + page_size]

    # 分页对象
    return Page(
        items=items_page,
        current_page=current_page,
        per_page=page_size,
        max_page=items_max_page,
        count=items_count,
    )
