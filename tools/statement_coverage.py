"""Statement coverage without pytest-cov (uses Python 3.12+ sys.monitoring).
Run from the repo root:  python tools/statement_coverage.py
Counts executable LINES of app.py and helpers.py, so totals differ slightly from
coverage.py statement counts; the list of missing lines is what matters."""
import sys, os, dis, types, json
APP=os.path.abspath('app'); files={os.path.join(APP,'app.py'),os.path.join(APP,'helpers.py')}
hit={f:set() for f in files}
mon=sys.monitoring; TOOL=3
mon.use_tool_id(TOOL,'cov')
def on_line(code,line):
    if code.co_filename in hit: hit[code.co_filename].add(line)
mon.register_callback(TOOL,mon.events.LINE,on_line)
mon.set_events(TOOL,mon.events.LINE)
def stmts(f):
    co=compile(open(f).read(),f,'exec'); out=set()
    def walk(c):
        for _,_,l in c.co_lines():
            if l: out.add(l)
        for k in c.co_consts:
            if isinstance(k,types.CodeType): walk(k)
    walk(co); return out
import pytest
rc=pytest.main(['-m','not ui','-q','-p','no:cacheprovider','--no-header'])
mon.set_events(TOOL,0)
for f in sorted(files):
    st=stmts(f); h=hit[f]&st
    # docstring-only module line 1 counts; mimic coverage.py by excluding nothing
    print(os.path.basename(f), len(h),'/',len(st), f"{100*len(h)/len(st):.1f}%", 'missing:', sorted(st-h))
