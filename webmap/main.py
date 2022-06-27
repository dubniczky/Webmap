import argparse
from time import perf_counter

from modutils import trimf, unique_list
from crawler import crawl
from url import Url

# Begin performance measure
start_time = perf_counter()

## Init arg parser
parser = argparse.ArgumentParser(
    prog='Webmap',
    description='Website mapping crawler'
)

# Positional args
parser.add_argument('action', help='Action to do on the site. (map, mirror)')
parser.add_argument('url', help='Starting point for the scan.')

# Flags
parser.add_argument(
    "-s",
    "--silent",
    action='store_true',
    help='Do not write any console output.',
)
parser.add_argument(
    "-o",
    "--output",
    default='map.yml',
    dest='output',
    help='File to save detected url list.',
    type=str
)
parser.add_argument(
    "-u",
    "--unlock-domain",
    action='store_true',
    help='Allow search to move to different domain. It\'s advised to use --ignore-domains list to avoid searching commonly embedded websites.',
)
parser.add_argument(
    "--ignore-domains",
    default=None,
    help='Ignore mapping these domains when searching. Useful when using the --unlock-domain flag.',
    type=str
)

# Parse
args = parser.parse_args()

# Start crawler
print('Url:', args.url)
urls, map_count = crawl(Url(args.url))

# Remove duplicates
unique_urls = unique_list( [args.url] + [str(i) for i in urls] )

# Print performance
delta_time = trimf( perf_counter() - start_time )
print('========')
print(f'Scanned completed in: {delta_time}s')
print(f'Scanned sites: {map_count}')
print(f'Mapped endpoints: {len(unique_urls)}')

# Write output
with open(args.output, 'w', encoding='utf8') as f:
    f.write( '\n'.join(unique_urls) )
