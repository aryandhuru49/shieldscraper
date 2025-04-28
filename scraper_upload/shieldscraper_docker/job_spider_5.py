import scrapy

class JobSpider5(scrapy.Spider):
    name = "jobspider5"
    allowed_domains = []

    def __init__(self, start_url=None, output_file=None, *args, **kwargs):
        super(JobSpider5, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.output_file = output_file

    def parse(self, response):
        team_names = response.css('span.hide-mobile a::text').getall()
        stats = response.css("tr.Table__TR.Table__TR--sm.Table__even td.Table__TD span.stat-cell::text").getall()

        for i in range(0, len(stats), 8):
            team_stats = stats[i:i+8]
            team_data = {
                'team': team_names[i // 8],
                'GP': team_stats[0],
                'W': team_stats[1],
                'D': team_stats[2],
                'L': team_stats[3],
                'F': team_stats[4],
                'A': team_stats[5],
                'GD': team_stats[6],
                'P': team_stats[7]
            }
            yield team_data
