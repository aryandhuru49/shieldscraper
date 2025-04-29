import scrapy

class JobSpider5(scrapy.Spider):
    name = "jobspider5"
    allowed_domains = []

    def __init__(self, start_url=None, output_file=None, *args, **kwargs):
        super(JobSpider5, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.output_file = output_file

    def parse(self, response):

        title = response.css(".Table__Title::text").get()
        if not title:
            title = "unknown_league"
        formatted_title = title.replace(" ", "_")

        self.formatted_title = formatted_title
    
        team_names = response.css('span.hide-mobile a::text').getall()
        stats = response.css("tr.Table__TR.Table__TR--sm.Table__even td.Table__TD span.stat-cell::text").getall()

        for i in range(0, len(stats), 8):
            team_stats = stats[i:i+8]
            team_data = {
                'Team': team_names[i // 8],
                'Games Played': team_stats[0],
                'Wins': team_stats[1],
                'Draws': team_stats[2],
                'Losses': team_stats[3],
                'Goals For': team_stats[4],
                'Goals Against': team_stats[5],
                'Goal Difference': team_stats[6],
                'Points': team_stats[7],
                'Title': formatted_title
            }
            yield team_data
