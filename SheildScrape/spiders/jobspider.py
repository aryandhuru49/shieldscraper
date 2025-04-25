# import scrapy

# class JobspiderSpider(scrapy.Spider):
#     name = 'jobspider'

#     start_urls = [
#         'https://www.espn.com/soccer/table/_/league/eng.1'
#     ]

#     def parse(self, response):
#         with open("jobs_cleaned.txt", "a", encoding="utf-8") as f:  # Use append mode 'a' instead of 'w'
#             f.write(f"\nScraping from: {response.url}\n" + "="*100 + "\n\n")

#             for job in response.css('article.job.clicky'):
#                 title = job.css('h2 a::text').get(default='').strip()
                
#                 # Extracting and cleaning location
#                 location_raw = job.css('ul.location li').get()
#                 location = location_raw.replace(
#                     '<li>\n        <svg class="icon"><use xlink:href="#icon-pin"></use></svg>\n        ', ''
#                 ).replace('\n      </li>', '').strip() if location_raw else "N/A"

#                 # Extracting and cleaning salary (handling NoneType exception)
#                 salary_raw = job.css('ul.salary li').get()
#                 salary = salary_raw.replace(
#                     '<li>\n      <svg class="icon"><use xlink:href="#icon-salary"></use></svg>\n      ', ''
#                 ).replace('\n    </li>', '').strip() if salary_raw else "N/A"

#                 # Extracting and cleaning description
#                 desc = job.css('div.desc::text').get(default='').strip()

#                 # Extracting and cleaning posted date (handling NoneType exception)
#                 posted_raw = job.css('footer .badge').get()
#                 posted = posted_raw.replace(
#                     '<span class="badge badge-r badge-s badge-icon">\n          <svg class="icon"><use xlink:href="#icon-clock-filled"></use></svg> ', ''
#                 ).replace('\n        </span>', '').strip() if posted_raw else "N/A"


#                 # Writing to file
#                 f.write(f"Job Title: {title}\n")
#                 f.write(f"Location: {location}\n")
#                 f.write(f"Salary: {salary}\n")
#                 f.write(f"Description: {desc}\n")
#                 f.write(f"Posted: {posted}\n")
#                 f.write("\n" + "="*100 + "\n\n")

#                            # Check for the "Next page" button and follow the link if available
#             next_page = response.css('button.ves-control.ves-add.btn.btn-r.btn-primary-inverted.next::attr(data-value)').get()

#             if next_page:
#                 next_page_url = f'https://www.careerjet.com/company/GPAC/jobs?css=&csl=USA&p={next_page}'
#                 # Following the link to the next page and calling parse again
#                 yield response.follow(next_page_url, self.parse)

import scrapy

class JobspiderSpider(scrapy.Spider):
    name = "jobspider"
    allowed_domains = []
    start_urls = ['https://www.espn.com/soccer/table/_/league/']  
  
    
    def parse(self, response):
        
        team_names = response.css('span.hide-mobile a::text').getall()

        
        stats =  response.css("tr.Table__TR.Table__TR--sm.Table__even td.Table__TD span.stat-cell::text").getall()
        
        
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
