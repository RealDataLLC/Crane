"""
Downloads pdf from zotero
Takes like 20 secs to download
"""
from pyzotero import zotero
library_id, library_type, api_key = 2283423, 'group', "5dz3PnolHLlJLgYNPfp6NYB2"
zot = zotero.Zotero(library_id, library_type, api_key)
items = zot.top(limit=5)
# we've retrieved the latest five top-level items in our library
# we can print each item's item type and ID
#for item in items:
#    print('Item: %s | Key: %s' % (item['data']['itemType'], item['data']['key']))

#searching by tag
first_ten = zot.items(tag = "Wind Power", limit=10)
for item in first_ten:
    print(item)

#downloading pdf by ID
#zot.dump("N28JG232", filename = "ex.pdf")