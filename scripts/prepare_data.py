#!/usr/bin/env python3
"""Build the compact RetailReach audience index from the original UCI XLSX.

Usage: python scripts/prepare_data.py "/path/to/Online Retail.xlsx"
Uses only the Python standard library.
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from xml.etree.ElementTree import fromstring, iterparse
from zipfile import ZipFile

NS = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
SHEET = 'xl/worksheets/sheet1.xml'
SHARED = 'xl/sharedStrings.xml'
ROOT = Path(__file__).resolve().parents[1]


def shared_strings(archive):
    root = fromstring(archive.read(SHARED))
    return [''.join(node.itertext()) for node in root.findall('m:si', NS)]


def rows(archive, strings):
    with archive.open(SHEET) as stream:
        for _, row in iterparse(stream, events=('end',)):
            if not row.tag.endswith('}row'):
                continue
            result = {}
            for cell in row:
                if not cell.tag.endswith('}c'):
                    continue
                match = re.match(r'[A-Z]+', cell.attrib.get('r', ''))
                if not match:
                    continue
                value = cell.find('m:v', NS)
                if value is not None:
                    raw = value.text or ''
                    if cell.attrib.get('t') == 's':
                        raw = strings[int(raw)]
                    result[match.group(0)] = raw
            row.clear()
            if result:
                yield result


def eligible(record):
    invoice = record.get('A', '').strip()
    stock = record.get('B', '').strip()
    description = record.get('C', '').strip()
    country = record.get('H', '').strip()
    customer = record.get('G', '').strip()
    try:
        qty = float(record.get('D', '0') or 0)
        price = float(record.get('F', '0') or 0)
        customer_id = str(int(float(customer)))
    except (ValueError, TypeError):
        return None
    if (not stock or not description or not country or not customer
            or invoice.upper().startswith('C') or qty <= 0 or price <= 0):
        return None
    return stock, description, customer_id, country


def main(source):
    source = Path(source)
    with ZipFile(source) as archive:
        strings = shared_strings(archive)
        buyers = defaultdict(set)
        valid_lines = 0
        all_customers = set()
        for record in rows(archive, strings):
            item = eligible(record)
            if item is None:
                continue
            stock, description, customer_id, _ = item
            buyers[(stock, description)].add(customer_id)
            all_customers.add(customer_id)
            valid_lines += 1
        ranked = sorted(buyers.items(), key=lambda pair: (-len(pair[1]), pair[0][1]))[:24]
        products = [
            {'id': stock, 'name': description, 'buyers': sorted(custs, key=int)}
            for (stock, description), custs in ranked
        ]
        selected = {p['id']: i for i, p in enumerate(products)}
        cohorts = defaultdict(lambda: defaultdict(set))
        for record in rows(archive, strings):
            item = eligible(record)
            if item is None:
                continue
            stock, _, customer_id, country = item
            if stock not in selected:
                continue
            try:
                year = '2010' if float(record['E']) < 40544 else '2011'
            except (KeyError, ValueError):
                continue
            cohorts[(country, year)][selected[stock]].add(customer_id)

    cohort_rows = [
        {'country': country, 'year': year,
         'sets': {str(i): sorted(ids, key=int) for i, ids in sets.items()}}
        for (country, year), sets in sorted(cohorts.items())
    ]
    output = {
        'source': 'UCI Online Retail (CC BY 4.0)',
        'products': products,
        'cohorts': cohort_rows,
        'metadata': {
            'validLines': valid_lines,
            'customers': len(all_customers),
            'productCount': len(products),
            'dateRange': '2010-12-01 to 2011-12-09',
            'filters': 'Completed sales only: cancellation invoices, returns, nonpositive prices/quantities, and missing customer IDs excluded.'
        }
    }
    output_path = ROOT / 'data' / 'retailreach-data.json'
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(output, separators=(',', ':'), ensure_ascii=False), encoding='utf-8')
    print(f'Wrote {output_path} ({output_path.stat().st_size:,} bytes; '
          f'{valid_lines:,} eligible lines; {len(all_customers):,} identified customers)')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('Usage: python scripts/prepare_data.py /path/to/Online_Retail.xlsx')
    main(sys.argv[1])
