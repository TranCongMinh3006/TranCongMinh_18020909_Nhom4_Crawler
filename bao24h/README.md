* GIỚI THIỆU QUA
	- đây là chương trình thu thập dữ liệu các bài báo được viết tại trang báo 24h.com.vn

* MÔ TẢ MÃ NGUỒN
	- em đã tạo class Bao24hCrawler :


	class Bao24hCrawler(scrapy.Spider):

	#đây là là một biến đặc biệt , nó phải là biến có giá trị duy nhất trong 1 dự án , và sẽ được dùng để phân biệt các crawler mỗi khi ta crawl dữ liệu
    name = 'bao24h'

    # đây là một list các tên miền mà ta crawler được phép thu thập dữ liệu , tại đây em chỉ muốn thu thập duy nhất tại trang 24h.com.vn
    allowed_domains = ['24h.com.vn']

    #đây là một list các link mà crawler sẽ bắt đầu dùng để thu thập
    start_urls =    ['https://www.24h.com.vn/']

    #đây là một biến dùng để đếm số bài báo mà em đã thu được
    count = 0

    # đây là hàm mà nhần đầu vào là một response và sẽ phân tích response này để trích xuất ra các phần quan trọng
    def parse(self, response):

    	#đây là điểu kiện để kiển tra xem response trả về có đúng dạng là bài báo hay không
        if response.status == 200 and response.css('meta[property="og:type"]::attr("content")').get() == 'article':
            
            # mỗi lần phân tích một response thì biến count sẽ tăng thêm 1 và in ra màn hình để ta biết ta đã thu thập được bao nhiêu bài rồi
            Bao24hCrawler.count += 1
            print(Bao24hCrawler.count)
			
			#em tạo một kiểu dữ liệu dạng json , để khi thu thập dữ liệu được về file sẽ dễ đọc hơn và cũng dễ dàng gửi cho người khác dùng hơn nếu dùng ngôn ngữ lập trình khác
            data = {
                'link': response.url,
                'title': response.css('h1.clrTit.bld.tuht_show::text').get(),
                'description': response.css('h2.ctTp.tuht_show::text').get(),
                'content': '\n'.join([
                    ''.join(c.css('*::text').getall())
                        for c in response.css('article[id="article_body" ] > p')
                ]),
                'category': response.css('a.brmItem.bld span::text').get(),
                'date': response.css('div.updTm.updTmD.mrT5::text').get(),
                'keywords': [
                    k.strip() for k in response.css('meta[name="keywords"]::attr("content")').get().split(',')
                ],

            }
			
			# tại đây em lưu các dữ liệu thu được vào một file là bao24.txt
            with open('bao24h.txt', 'a', encoding='utf8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')

		#tại đây em sẽ lan sang các link khác có trong bài viết để tiếp tục lấy dữ liệu , các link được lan sang phải có dạng bắt đầu bằng https://www.24h.com.vn/ hoặc '/' 
        yield from response.follow_all(css='a[href^="https://www.24h.com.vn/"]::attr(href), a[href^="/"]::attr(href)', callback=self.parse)


* KẾT QUẢ THU ĐƯỢC:
em đã thu được hơn 5000 bài báo từ trang báo 24h và chọn lọc ra được theo dạnh tiêu đề , mô tả , link bài viết , nội dung, keywords, loại bài báo