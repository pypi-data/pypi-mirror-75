from . import *

client = TVDBClient('csm10495',  'JI9SYINHWL8TNE9X', 'EA66B164E0840041')
config = Config('my_config.json')
config.add_show(client.get_show_info("Last Week Tonight With John Oliver"))
config.add_show(client.get_show_info("90 Day Fiance: The Other Way"))
config.add_show(client.get_show_info("SMothered"))
rss = RSSGenerator(client, config)