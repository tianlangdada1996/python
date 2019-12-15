from django.utils.safestring import mark_safe


class Pagination:

    def __init__(self, current_page_num, customer_num, get_data=None, page_num_show=7, data_show_number=10):
        self.get_data = get_data
        self.page_num_show = page_num_show
        self.data_show_number = data_show_number
        # print(self.data_show_number)
        # 传进来的current_page_num有可能为None，也有可能不是数字，所以要try一下，所有不是数字的全部变为1，让它显示分页为1的前十条数据
        try:
            self.current_page_num = int(current_page_num)
        except Exception:
            self.current_page_num = 1

        # 计算一下筛选出来的客户信息的数量需要分成几页，用客户总数customer_num和每一页显示的数量data_num_number做一个除法，
        # 得到的a为商 ，b为除数，若有除数需要在商的基础上+1多分一页，如果没有除数直接用商作为分页数就好了
        a, b = divmod(customer_num, self.data_show_number)
        if b:
            self.page_num_count = a + 1
        elif a:
            self.page_num_count = a
        else:
            self.page_num_count = 1

        # 如果获取的page小于1，则让获取的page等于第一页
        if self.current_page_num < 1:
            self.current_page_num = 1

        # 如果获取的page大于总页码数，则让获取的page等于最后一页
        if self.current_page_num > self.page_num_count:
            self.current_page_num = self.page_num_count

        # 为了让选择的页码号在展示的所有页码的中间，需要根据选择的页码号来确定展示所有页码的首和尾
        # 假如展示7个页码，选择第10页，那么展示的页码应该是[7,8,9,10,11,12,13]
        # 所以先算出展示页码数量的一半是多少half_num，再用选择的那个页码数current_page_num减去一半half_num，得到第一个展示的页码，
        # 用current_page_num加上一半half_num，得到最后一个展示的页码，又因为最后要range一下，range顾头不顾腚，再给最后加1
        half_num = page_num_show // 2
        self.start_page_num = self.current_page_num - half_num
        self.end_page_num = self.current_page_num + half_num

        # 如果总页码数比要展示的页码数还小，意思是说数据总共就5页，我设定的展示7页，明显没有7页，那么就让第一个显示的页码是1，
        # 最后显示的页码是总页码数就好了
        if self.page_num_count < self.page_num_show:
            self.start_page_num = 1
            self.end_page_num = self.page_num_count

        # 计算后的最后一页值如果大于了总页数值，则让尾页等于总页数值加1，意思是说数据总共就10页，点第10页经过上面的计算最后一页成了13了，
        # 明显不符合要求，所以超了总页数，就让最后一页等于总页数+1，让显示的第一个页码等于end_page_num减去展示的页码数就好了
        elif self.end_page_num > self.page_num_count:
            self.end_page_num = self.page_num_count
            self.start_page_num = self.end_page_num - self.page_num_show + 1

        # 计算后的第一页比0还小了，就让第一页等于1，然后显示的最后一页等于显示的页码数+1就好了
        elif self.start_page_num < 1:
            self.start_page_num = 1
            self.end_page_num = self.page_num_show

        # 开头和结尾的数已经算好了，利用range生成一个迭代器，for循环就可以拿到每一页的页码号了
        self.page_num_range = range(self.start_page_num, self.end_page_num + 1)

    # 显示数据的开头，比如说每页显示10条数据，第1页是0-9条，第2页数据的开头应该是第10条
    @property
    def start_data_num(self):
        # 用点击的页码号减去1乘上每页展示的数据就是将来要切片的头，比如点击第2页，那切片的起始应该是：(2-1)*10 = 10
        return (self.current_page_num - 1) * self.data_show_number

    # # 显示数据的开头，比如说每页显示10条数据，第1页是0-9条，第2页数据的结尾应该是第19条，但切片不顾腚所以正好是20
    @property
    def end_data_num(self):
        # 用点击的页码号乘上每页展示的数据就是将来要切片的尾，比如点击第2页，那切片的结尾应该是：2*10 = 20(不顾腚)
        return self.current_page_num * self.data_show_number

    def html(self):
        page_html = """
            <nav aria-label="Page navigation example">
            <ul class="pagination">
            """

        # 首页
        self.get_data['page'] = 1
        # get_data为获取的可以改变的get请求的querydict对象，它有一个urlencode方法可以自动拼接请求中的数据
        # 例如：get_data为< QueryDict: {'page': ['1'], 'action': ['qq__contains'], 'cd': ['11']} >
        #       get_data.urlencode()能得到page=1&action=qq_contains&cd=11
        # 所以把get_data中的page替换对应页码，就能得到带着模糊搜索数据的完整get请求，每个页面的a标签路径也就有了
        first_page = f"""
            <li class="page-item">
                <a class="page-link" href="?{self.get_data.urlencode()}" aria-label="Previous">
                    <span aria-hidden="true">首页</span>
                </a>
            </li>
            """
        page_html += first_page

        # 加判断单纯就为了当选择的当前分页为第一页的时候让上一页这个a标签不能点击，加了个disabled类值
        if self.current_page_num == 1:
            self.get_data["page"] = self.current_page_num - 1
            prev_page = f"""
                <li class="page-item disabled">
                <a class="page-link" href="?{self.get_data.urlencode()}" aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                </a>
                </li>
                """
        else:
            self.get_data["page"] = self.current_page_num - 1
            prev_page = f"""
                <li class="page-item">
                <a class="page-link" href="?{self.get_data.urlencode()}" aria-label="Previous">
                    <span aria-hidden="true">&laquo;</span>
                </a>
                </li>
                """
        page_html += prev_page

        # 正式显示的页码
        html = ''
        for page_num in self.page_num_range:
            self.get_data['page'] = page_num
            # 加判断是为了当页码是点击的当前页时，页码的底色变为蓝色，增加active类值
            if page_num == self.current_page_num:
                html += f'''
                    <li class="page-item active"><a class="page-link" href="?{self.get_data.urlencode()}">{page_num}</a></li>
                    '''
            else:
                html += f'''
                    <li class="page-item"><a class="page-link" href="?{self.get_data.urlencode()}">{page_num}</a></li>
                    '''
        page_html += html

        # 加判断单纯就为了当选择的当前分页为最后一页的时候让下一页这个a标签不能点击，加了个disabled类值
        if self.current_page_num == self.page_num_count:
            self.get_data["page"] = self.current_page_num + 1
            next_page = f"""
                <li class="page-item disabled">
                <a class="page-link" href="?{self.get_data.urlencode()}" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                </a>
                </li>
                """
        else:
            self.get_data["page"] = self.current_page_num + 1
            next_page = f"""
                <li class="page-item">
                <a class="page-link" href="?{self.get_data.urlencode()}" aria-label="Next">
                    <span aria-hidden="true">&raquo;</span>
                </a>
                </li>
                """
        page_html += next_page

        # 尾页
        self.get_data["page"] = self.page_num_count
        last_page = f"""
            <li class="page-item">
                <a class="page-link" href="?{self.get_data.urlencode()}" aria-label="Next">
                    <span aria-hidden="true">尾页</span>
                </a>
            </li>
            </ul>
            </nav>
            """
        page_html += last_page

        # mark_safe让字符串变为安全的，否则浏览器显示一堆字符串，这样前端页面拿到字符串可以渲染成标签，使用此方法就是不用再前端页面使用过滤器safe了
        return mark_safe(page_html)
