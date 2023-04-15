import scrapy
import urllib import parse

class ZhaPianSpider(scrapy.Spider):
    name = 'zhapian'
    allowed_domains = ['c.tieba.baidu.com']
    start_urls = ['http://c.tieba.baidu.com/f?ie=utf-8&kw=%E9%98%B2%E8%AF%88%E9%AA%97&fr=search']

    def parse(self, response):
        # use css-classname as the nvigation mark
        url_list = response.css('.j_th_tit::attr(herf)').extract()
        for url in url_list:
            print(url)
            yield scrapy.Request(url=parse.urljoin(response.url, url), callback=self.parse_detail)
        next_url = response.css('.next.pagination-item::attr(herf)').extract()[0]
        if next_url:
            yield scrapy.Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        title = response.css('.core_title_txt.pull-left.text-overflow::text').extract()
        authors = response.css('.p_author_name.j_user_card::text').extract()
        contents_list = response.css('.d_post_content.j_d_post_content').extract()
        content_list = self.get_content(contents_list)
        pass

    def get_content(self, contents):
        contents_list = []
        for content in contents:
            req = ";\">(.*)</div>"
            result = re.findall(req, content)[0]
            contents_list.append(result)
        return contents_list

    def get_send_time_and_floor(self, response):
        bbs_send_time_and_floor_list = response.css('.post-tail-wrap span[class=tail-info]::text').extract()
        i = 0
        bbs_sendtime_list=[]
        bbs_floor_list=[]
        for lz in bbs_send_time_and_floor_list:
            if lz == "lz":
                bbs_send_time_and_floor_list.remove(lz)

        for bbs_send_time_and_floor in bbs_send_time_and_floor_list:
            if i%2 == 0:
                bbs_floor_list.append(bbs_send_time_and_floor)
            if i%2 == 1:
                bbs_sendtime_list.append(bbs_send_time_and_floor)
            i += 1

        return bbs_sendtime_list, bbs_floor_list


