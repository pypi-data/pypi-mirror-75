api_version = 2.13
context_path = 'caas'
my_user_path = '/user/myUser'
list_servers = '/server/server'
get_server = '/server/server/{0}'
list_network_domains = '/network/networkDomain'
list_tags = '/tag/tag'
list_datacenters = '/infrastructure/datacenter'
list_geos = '/infrastructure/geographicRegion'
list_os_image = '/image/osImage/'
list_customer_image = '/image/customerImage/'

known_geos = ['africa', 'asiapacific', 'australia', 'canada', 'europe', 'indonesia', 'israel', 'northamerica']

api_urls = {'africa': 'https://afapi.opsourcecloud.net',
            'asiapacific': 'https://apapi.opsourcecloud.net',
            'australia': 'https://auapi.opsourcecloud.net',
            'canada': 'https://api-canada.dimensiondata.com',
            'europe': 'https://euapi.opsourcecloud.net',
            'indonesia': 'https://idapi.opsourcecloud.net',
            'israel': 'https://ilapi.opsourcecloud.net',
            'northamerica': 'https://api.opsourcecloud.net'}
