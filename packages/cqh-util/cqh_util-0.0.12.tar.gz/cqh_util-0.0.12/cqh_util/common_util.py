

def common_generator_paginate(cursor, page_size=10):
    """
    把range(100) 分成10个list
    一般用户导出，因为导出一般是genrator,但是不分页的话，就是n/page_size+n条sql, 现在改成 n/page_size + n/page_size这个样子
    """
    cache = []
    for ele in cursor:
        cache.append(ele)
        if len(cache) >= page_size:
            yield cache[:]
            del cache[:]
    if cache:
        yield cache[:]
