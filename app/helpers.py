def make_pagination_links(response, page_num, page_size, items_len):

    if page_num > 1:
        response["pagination"]["prev"] = page_num - 1
    else:
        response["pagination"]["prev"] = None

    if page_num * page_size >= items_len:
        response["pagination"]["next"] = None
    else:
        response["pagination"]["next"] = page_num + 1
