*GIỚI THIỆU QUA:
- đây là chương trình thu thập dữ liệu các sản phẩm được bán tại thế giới di dộng

*MÔ TẢ MÃ NGUỒN
class TheGioiDiDongSpider(scrapy.Spider):

    ##đây là là một biến đặc biệt , nó phải là biến có giá trị duy nhất trong 1 dự án , và sẽ được dùng để phân biệt các crawler mỗi khi ta crawl dữ liệu
    name = 'thegioididongCrawler'

    # đây là một list các tên miền mà ta crawler được phép thu thập dữ liệu , tại đây em chỉ muốn thu thập duy nhất tại trang thegioididong.com
    allowed_domains = ['thegioididong.com']

    ##đây là một list các link mà crawler sẽ bắt đầu dùng để thu thập
    start_urls = ['https://www.thegioididong.com/']

    #biến đếm số lượng sản phẩm thu được
    COUNT = 0
    
    # đây là hàm mà nhần đầu vào là một response và sẽ phân tích response này để trích xuất ra các phần quan trọng
    def parse(self, response):
        if response.status == 200 and response.css('section.type0 > div::attr(id)').get() == 'normalproduct':
            TheGioiDiDongSpider.COUNT+=1
            print(TheGioiDiDongSpider.COUNT)

            #em tạo một kiểu dữ liệu dạng json , để khi thu thập dữ liệu được về file sẽ dễ đọc hơn và cũng dễ dàng gửi cho người khác dùng hơn nếu dùng ngôn ngữ lập trình khác
            data = {
            
                'link': response.url,
                'category': response.css('ul.breadcrumb > li > a::text')[1].get(),
                'name': response.css('div.rowtop > h1::text').get(),
                'img_url': response.css('div.icon-position > img::attr(src)').getall(),
                'brand': response.css('li.brand > a::text').get(),
                'price':response.css('div.area_price > strong::text').get(),
                'short_desc': '\n'.join([
                    ''.join(c.css('*::text').getall())
                        for c in response.css('article.area_article > h2')]),
            }
            
            ## tại đây em lưu các dữ liệu thu được vào một file là thegioididong.txt
            with open('thegioididong.txt', 'a', encoding='utf8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')
        
        ##tại đây em sẽ lan sang các link khác có trong bài viết để tiếp tục lấy dữ liệu , các link được lan sang phải có dạng bắt đầu bằng https://www.thegioididong.com hoặc '/' 
        yield from response.follow_all(css='a[href^="https://www.thegioididong.com"]::attr(href), a[href^="/"]::attr(href)', callback=self.parse)

*KẾT QUẢ THU ĐƯỢC
- em đã thu được hơn 2000 các sản phẩm từ trang thế giới di động và đã bóc tách ra thành link bài viết, tên sản phẩm , tên thương hiệu , giá bán , mô tả