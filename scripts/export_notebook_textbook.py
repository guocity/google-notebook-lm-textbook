#!/usr/bin/env python3
"""Export authorized NotebookLM textbook content through an existing CLI session.

Exports structured JSON and extracted text, NOT the original PDF binary.
Authentication is obtained from a session request and is never written to output.
"""
import argparse
import json
from pathlib import Path
import subprocess
from urllib.parse import parse_qs


def cli(*args):
    result = subprocess.run(['playwright-cli', *args], capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError('playwright-cli failed; check the selected tab and browser session')
    return result.stdout


def decode(raw, rpc):
    for line in raw.splitlines():
        if line.startswith('[['):
            for frame in json.loads(line):
                if frame[0] == 'wrb.fr' and frame[1] == rpc and isinstance(frame[2], str):
                    return json.loads(frame[2])
    raise RuntimeError('No successful RPC payload; authentication or source access may have failed')


def text_runs(value):
    if not isinstance(value, list):
        return
    if (len(value) >= 3 and type(value[0]) is int and type(value[1]) is int
            and isinstance(value[2], list) and value[2] and isinstance(value[2][0], str)):
        yield value[2][0]
    else:
        for child in value:
            yield from text_runs(child)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--request-number', required=True, help='Existing rLM1Ne notebook request number')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--source-id', help='Existing source UUID')
    group.add_argument('--catalog-id', help='Catalog ID; adds this book to the selected notebook')
    parser.add_argument('--catalog', type=Path, default=Path(__file__).resolve().parents[1] / 'textbook-catalog/textbooks-source.json')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    # Request data stays in memory. Never print it: it contains a session token.
    params = parse_qs(cli('request-body', args.request_number).strip())
    request = json.loads(params['f.req'][0])[0][0]
    if request[0] != 'rLM1Ne':
        raise RuntimeError('Choose an rLM1Ne request from the intended notebook tab')
    notebook_query = json.loads(request[1])
    notebook, context = notebook_query[0], notebook_query[2]
    token = params['at'][0]

    def rpc_call(rpc, query):
        payload = {'rpc': rpc, 'query': query, 'token': token}
        code = '''async page => await page.evaluate(async p => {
          const body = new URLSearchParams({
            "f.req": JSON.stringify([[[p.rpc, JSON.stringify(p.query), null, "generic"]]]), at:p.token
          });
          const response = await fetch("/_/LabsTailwindUi/data/batchexecute?rpcids="+p.rpc, {
            method:"POST", headers:{"Content-Type":"application/x-www-form-urlencoded;charset=utf-8"}, body:body.toString()
          });
          return await response.text();
        }, PAYLOAD)'''.replace('PAYLOAD', json.dumps(payload))
        output = cli('run-code', code)
        raw = json.loads(output.split('### Result\n', 1)[1].split('\n### Ran', 1)[0])
        return raw, decode(raw, rpc)

    source_id = args.source_id
    args.output.mkdir(parents=True, exist_ok=True)
    if args.catalog_id:
        book = next(b for b in json.loads(args.catalog.read_text()) if b[0] == args.catalog_id)
        upload = [None] * 16
        upload[10] = 1
        upload[15] = [book[1], book[0], book[2], book[3], book[4], None, book[7], None, book[15]]
        raw, added = rpc_call('izAoDd', [[upload], notebook, context])
        source_id = added[0][0][0][0]
        (args.output / 'add-source.json').write_text(json.dumps(added, ensure_ascii=False, indent=2) + '\n')
    raw, data = rpc_call('hizoJc', [[source_id], [2], context])
    (args.output / 'response.txt').write_text(raw)
    (args.output / 'source.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    if len(data) > 3 and data[3]:
        text = '\n'.join(text_runs(data[3]))
    elif len(data) > 1 and isinstance(data[1], list) and len(data[1]) > 1 and isinstance(data[1][1], str):
        text = data[1][1]
    else:
        raise RuntimeError('Response saved, but this source uses an unhandled content format')
    (args.output / 'textbook.txt').write_text(text + '\n')
    print(json.dumps({'source_id': source_id, 'text_characters': len(text), 'output': str(args.output), 'original_pdf': False}))


if __name__ == '__main__':
    main()
