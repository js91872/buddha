#!/usr/bin/env python3
"""Run an installed official EPUBCheck jar and bind its result to this EPUB's hash."""
from pathlib import Path
import argparse,subprocess,json,hashlib,os,shutil
R=Path(__file__).resolve().parents[1];Q=R/'publishing/quality-assurance'
a=argparse.ArgumentParser();a.add_argument('--jar',default=os.environ.get('EPUBCHECK_JAR'));args=a.parse_args()
jar=Path(args.jar) if args.jar else None
if jar is None or not jar.is_file():raise SystemExit('Pass --jar /absolute/path/to/epubcheck.jar or set EPUBCHECK_JAR')
p=R/'release/the-light-of-buddha-volume-1.epub'
cmd=['java','-jar',str(jar.resolve()),str(p),'--json',str(Q/'epubcheck-detailed.json')]
result=subprocess.run(cmd,text=True,capture_output=True)
(Q/'epubcheck.log').write_text('$ '+' '.join(cmd)+'\n'+result.stdout+result.stderr+'\nExit: '+str(result.returncode)+'\n')
version=subprocess.run(['java','-jar',str(jar.resolve()),'--version'],text=True,capture_output=True)
report={'command':cmd,'exit_code':result.returncode,'version':(version.stdout+version.stderr).strip(),'epub_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'jar_sha256':hashlib.sha256(jar.read_bytes()).hexdigest(),'pass':result.returncode==0}
details=Q/'epubcheck-detailed.json'
if details.exists():
 checker=json.loads(details.read_text()).get('checker',{})
 report['messages']={name:checker.get(name) for name in ['nFatal','nError','nWarning','nUsage']}
(Q/'epubcheck-result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2));raise SystemExit(result.returncode)
