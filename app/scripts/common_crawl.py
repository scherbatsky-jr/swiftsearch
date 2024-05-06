import cdx_toolkit

cdx = cdx_toolkit.CDXFetcher(source='cc')
url = 'http://www.skysports.com/'  # Example URL to find captures of
captures = cdx.iter(url, from_ts='202001', to_ts='202002', filter=['status:200'])

for capture in captures:
    print(capture)
    # Process or download the data as needed