import scrapy


class NewsspiderSpider(scrapy.Spider):
    name = "newsSpider"
    allowed_domains = ["abcnews.go.com"]
    start_urls = ["https://abcnews.go.com/Business"]

    def parse(self, response):
        news = response.css("section.ContentRoll__Item")
        for new in news:
            new_url = new.css("h2 a::attr(href)").get()
            yield response.follow(new_url, callback=self.parse_new_page)
            
    def parse_new_page(self, response):
        contents = response.css("div.xvlfx  p.EkqkG")
        full_content = ""
        for content in contents:
            full_content += "".join(content.css("::text").getall()) + " "
        yield {
            "title" : response.css("h1.vMjAx span::text").get(),
            "description" : response.css("p.jxTEW  span::text").get(),
            "author": response.css("div.TQPvQ span")[1].css("::text").get(),
            "content": full_content
        }
        
           
        
        
