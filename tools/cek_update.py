import json,sys
d=json.load(open(sys.argv[1]))['data']; loc=open(sys.argv[2]).read()
m=d['meta']
print(d['id'],d['status'],d['link'],'| warnings',d.get('_content_warnings'),'| edit_mode',repr(m.get('_elementor_edit_mode')),'| elementor_data',len(m.get('_elementor_data') or ''),'| identik',d['content']==loc)
