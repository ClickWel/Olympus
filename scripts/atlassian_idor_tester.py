#!/usr/bin/env python3
"""
Atlassian IDOR Automated Testing Framework
===========================================
Tests Jira, Confluence, Bitbucket, and Trello APIs for Insecure Direct Object
Reference vulnerabilities using a two-token approach.

REQUIRES: Only TWO valid authentication token sets (for two different users).

USAGE:
  # Test Jira IDORs (two user API tokens)
  python3 atlassian_idor_tester.py \
    --target company \
    --jira-user1 "Basic b64encodeduser1" \
    --jira-user2 "Basic b64encodeduser2" \
    --auto-discover

  # Test with specific IDs
  python3 atlassian_idor_tester.py \
    --base-jira https://company.atlassian.net \
    --jira-user1 TOKEN1 --jira-user2 TOKEN2 \
    --issue-key ENG-123 --project-id ENG

  # Multi-product test
  python3 atlassian_idor_tester.py \
    --base-jira https://company.atlassian.net \
    --base-confluence https://company.atlassian.net/wiki \
    --jira-user1 TOKEN1 --jira-user2 TOKEN2 \
    --confluence-user1 TOKEN1 --confluence-user2 TOKEN2 \
    --page-id 123456789

  # Trello test
  python3 atlassian_idor_tester.py \
    --trello-key1 KEY1 --trello-token1 TOKEN1 \
    --trello-key2 KEY2 --trello-token2 TOKEN2 \
    --auto-discover

Author: Hermes Agent | Nous Research
Date: 2026-04-09
"""

import argparse, csv, json, logging, os, sys, time
from dataclasses import dataclass, field, asdict
from urllib.parse import quote

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("[!] 'requests' library required: pip3 install requests")
    sys.exit(1)

@dataclass
class TestResult:
    product: str
    method: str
    endpoint: str
    full_url: str
    status_u1: int
    status_u2: int
    response_u1: str
    response_u2: str
    idor_likely: bool
    severity: str
    notes: str

@dataclass
class IDORTarget:
    product: str
    method: str
    path_template: str
    description: str
    resource_id_param: str
    idor_type: str
    risk_level: str
    discovery_endpoints: list = field(default_factory=list)

# ============================================================
# HIGH-RISK IDOR TEST CASES (curated from OpenAPI specs)
# ============================================================

HIGH_RISK_TEST_CASES = [
    # ---- JIRA CLOUD ----
    IDORTarget("jira","GET","/rest/api/3/issue/{resource_id}",
        "Get issue details by key/ID","resource_id","horizontal","high",
        discovery_endpoints=["/rest/api/3/search?jql=order+by+created+DESC&maxResults=5"]),
    IDORTarget("jira","GET","/rest/api/3/issue/{resource_id}/comment",
        "Get issue comments","resource_id","horizontal","high",
        discovery_endpoints=["/rest/api/3/search?jql=order+by+created+DESC&maxResults=5"]),
    IDORTarget("jira","GET","/rest/api/3/issue/{resource_id}/worklog",
        "Get issue worklog entries","resource_id","horizontal","high",
        discovery_endpoints=["/rest/api/3/search?jql=order+by+created+DESC&maxResults=5"]),
    IDORTarget("jira","GET","/rest/api/3/project/{resource_id}",
        "Get project details","resource_id","horizontal","high",
        discovery_endpoints=["/rest/api/3/project"]),
    IDORTarget("jira","GET","/rest/api/3/project/{resource_id}/role",
        "Get project roles","resource_id","horizontal","high",
        discovery_endpoints=["/rest/api/3/project"]),
    IDORTarget("jira","GET","/rest/api/3/project/{resource_id}/email",
        "Get project email settings","resource_id","horizontal","critical",
        discovery_endpoints=["/rest/api/3/project"]),
    IDORTarget("jira","GET","/rest/api/3/dashboard/{resource_id}",
        "Get dashboard details","resource_id","horizontal","medium",
        discovery_endpoints=["/rest/api/3/dashboard"]),
    IDORTarget("jira","GET","/rest/api/3/filter/{resource_id}",
        "Get saved filter","resource_id","horizontal","medium",
        discovery_endpoints=["/rest/api/3/filter/search"]),
    IDORTarget("jira","GET","/rest/api/3/permissionscheme/{resource_id}",
        "Get permission scheme (CRITICAL - exposes all permissions)","resource_id","horizontal","critical",
        discovery_endpoints=["/rest/api/3/permissionscheme"]),
    IDORTarget("jira","GET","/rest/api/3/attachment/{resource_id}",
        "Get attachment metadata","resource_id","horizontal","high",
        discovery_endpoints=["/rest/api/3/attachment/meta"]),
    IDORTarget("jira","GET","/rest/api/3/attachment/content/{resource_id}",
        "Download attachment content (DATA EXFILTRATION)","resource_id","horizontal","critical",
        discovery_endpoints=[]),
    IDORTarget("jira","GET","/rest/api/3/issue/{resource_id}/remotelink",
        "Get issue remote links (may expose external integrations)","resource_id","horizontal","medium",
        discovery_endpoints=["/rest/api/3/search?jql=order+by+created+DESC&maxResults=5"]),
    IDORTarget("jira","PUT","/rest/api/3/issue/{resource_id}",
        "Modify issue (potential data tampering)","resource_id","horizontal","critical",
        discovery_endpoints=[]),
    IDORTarget("jira","PUT","/rest/api/3/issue/{resource_id}/assignee",
        "Reassign issue","resource_id","horizontal","critical",
        discovery_endpoints=[]),
    IDORTarget("jira","DELETE","/rest/api/3/issue/{resource_id}",
        "Delete issue","resource_id","horizontal","critical",
        discovery_endpoints=[]),
    IDORTarget("jira","GET","/rest/api/3/issue/{resource_id}/editmeta",
        "Get edit metadata (field access info)","resource_id","horizontal","medium",
        discovery_endpoints=["/rest/api/3/search?jql=order+by+created+DESC&maxResults=5"]),

    # ---- CONFLUENCE CLOUD ----
    IDORTarget("confluence","GET","/wiki/rest/api/content/{resource_id}",
        "Get content by ID","resource_id","horizontal","high",
        discovery_endpoints=["/wiki/rest/api/content?limit=5"]),
    IDORTarget("confluence","GET","/wiki/rest/api/content/{resource_id}/child/page",
        "Get child pages","resource_id","horizontal","medium",
        discovery_endpoints=["/wiki/rest/api/content?limit=5"]),
    IDORTarget("confluence","GET","/wiki/rest/api/content/{resource_id}/child/attachment",
        "Get page attachments","resource_id","horizontal","high",
        discovery_endpoints=["/wiki/rest/api/content?limit=5"]),
    IDORTarget("confluence","GET","/wiki/rest/api/content/{resource_id}/comment",
        "Get page comments","resource_id","horizontal","medium",
        discovery_endpoints=["/wiki/rest/api/content?limit=5"]),
    IDORTarget("confluence","GET","/wiki/rest/api/content/{resource_id}/history",
        "Get content history/revisions","resource_id","horizontal","high",
        discovery_endpoints=["/wiki/rest/api/content?limit=5"]),
    IDORTarget("confluence","GET","/wiki/api/v2/pages/{resource_id}",
        "Get page v2","resource_id","horizontal","high",
        discovery_endpoints=["/wiki/api/v2/pages?limit=5"]),
    IDORTarget("confluence","GET","/wiki/api/v2/pages/{resource_id}/properties",
        "Get page properties (hidden data)","resource_id","horizontal","high",
        discovery_endpoints=[]),

    # ---- BITBUCKET CLOUD ----
    IDORTarget("bitbucket","GET","/2.0/repositories/{workspace}/{resource_id}",
        "Get repository details","resource_id","horizontal","high",
        discovery_endpoints=["/2.0/repositories/{workspace}"]),
    IDORTarget("bitbucket","GET","/2.0/repositories/{workspace}/{resource_id}/issues",
        "Get repository issues","resource_id","horizontal","high",
        discovery_endpoints=["/2.0/repositories/{workspace}"]),
    IDORTarget("bitbucket","GET","/2.0/repositories/{workspace}/{resource_id}/pullrequests",
        "Get pull requests","resource_id","horizontal","high",
        discovery_endpoints=["/2.0/repositories/{workspace}"]),
    IDORTarget("bitbucket","GET","/2.0/repositories/{workspace}/{resource_id}/forks",
        "Get repository forks","resource_id","horizontal","medium",
        discovery_endpoints=[]),
    IDORTarget("bitbucket","GET","/2.0/repositories/{workspace}/{resource_id}/permissions-config/groups",
        "Get repo permission groups","resource_id","horizontal","high",
        discovery_endpoints=[]),

    # ---- TRELLO ----
    IDORTarget("trello","GET","/1/boards/{resource_id}",
        "Get board details","resource_id","horizontal","high",
        discovery_endpoints=["/1/members/me/boards"]),
    IDORTarget("trello","GET","/1/boards/{resource_id}/cards",
        "Get all cards on board","resource_id","horizontal","high",
        discovery_endpoints=[]),
    IDORTarget("trello","GET","/1/cards/{resource_id}",
        "Get card details","resource_id","horizontal","high",
        discovery_endpoints=[]),
    IDORTarget("trello","GET","/1/cards/{resource_id}/attachments",
        "Get card attachments","resource_id","horizontal","high",
        discovery_endpoints=[]),
    IDORTarget("trello","GET","/1/cards/{resource_id}/actions",
        "Get card activity log","resource_id","horizontal","medium",
        discovery_endpoints=[]),
    IDORTarget("trello","GET","/1/members/{resource_id}/boards",
        "Get member boards","resource_id","horizontal","high",
        discovery_endpoints=[]),
    IDORTarget("trello","GET","/1/organizations/{resource_id}",
        "Get organization details","resource_id","horizontal","medium",
        discovery_endpoints=["/1/members/me/organizations"]),
    IDORTarget("trello","GET","/1/lists/{resource_id}/cards",
        "Get cards in list","resource_id","horizontal","high",
        discovery_endpoints=[]),
]


class AtlassianIDORTester:
    def __init__(self, config):
        self.config = config
        self.results = []
        self.session = requests.Session()
        retry = Retry(total=3, backoff_factor=1, status_forcelist=[429,500,502,503,504])
        self.session.mount('https://', HTTPAdapter(max_retries=retry))
        self.session.headers.update({'Accept':'application/json','User-Agent':'Atlassian-IDOR-Tester/1.0'})
        self.delay = config.get('delay', 0.5)
        self.last_t = 0

    def _rate_limit(self):
        elapsed = time.time() - self.last_t
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_t = time.time()

    def _detect_product(self, url):
        u = url.lower()
        if 'bitbucket' in u: return 'bitbucket'
        if 'trello' in u: return 'trello'
        if '/wiki' in u or 'confluence' in u: return 'confluence'
        if 'atlassian' in u or 'jira' in u: return 'jira'
        return None

    def _get_auth_headers(self, user_num, product, url):
        headers = {}
        if product == 'jira':
            token = self.config.get(f'jira_user{user_num}', '')
            if token.startswith('Basic ') or token.startswith('Bearer '):
                headers['Authorization'] = token
            else:
                email = self.config.get(f'jira_email{user_num}', '')
                if email:
                    import base64
                    headers['Authorization'] = 'Basic ' + base64.b64encode(f'{email}:{token}'.encode()).decode()
                else:
                    headers['Authorization'] = f'Bearer {token}'
        elif product == 'confluence':
            token = self.config.get(f'confluence_user{user_num}', '')
            if token.startswith('Basic ') or token.startswith('Bearer '):
                headers['Authorization'] = token
            else:
                email = self.config.get(f'confluence_email{user_num}', '')
                if email:
                    import base64
                    headers['Authorization'] = 'Basic ' + base64.b64encode(f'{email}:{token}'.encode()).decode()
                else:
                    headers['Authorization'] = f'Bearer {token}'
        elif product == 'bitbucket':
            token = self.config.get(f'bitbucket_user{user_num}', '')
            if token.startswith('Bearer ') or token.startswith('Basic '):
                headers['Authorization'] = token
            else:
                headers['Authorization'] = f'Bearer {token}'
        elif product == 'trello':
            # Trello uses query params - handled in URL building
            pass
        return headers

    def _build_url(self, base_url, path, resource_id, product):
        full = path.replace('{resource_id}', quote(resource_id))
        full = full.replace('{workspace}', quote(self.config.get('workspace', 'default-workspace')))
        full = full.replace('{commit}', quote(self.config.get('commit', 'HEAD')))
        full = full.replace('{path}', quote(self.config.get('file_path', 'README.md')))
        if '/wiki' in base_url and full.startswith('/wiki'):
            full = full[len('/wiki'):]
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        
        url = f'{base_url}{full}'
        
        # Trello auth via query params
        if product == 'trello':
            key = self.config.get(f'trello_key1', self.config.get(f'trello_key{self._current_user}', ''))
            token = self.config.get(f'trello_token1', self.config.get(f'trello_token{self._current_user}', ''))
            if key and token:
                sep = '&' if '?' in url else '?'
                url += f'{sep}key={key}&token={token}'
        return url

    def _make_request(self, user_num, method, url, body=None):
        self._rate_limit()
        self._current_user = user_num
        
        product = self._detect_product(url)
        headers = self._get_auth_headers(user_num, product, url)
        
        try:
            if method == 'GET':
                r = self.session.get(url, headers=headers, timeout=15)
            elif method == 'POST':
                r = self.session.post(url, json=body, headers=headers, timeout=15)
            elif method == 'PUT':
                r = self.session.put(url, json=body, headers=headers, timeout=15)
            elif method == 'DELETE':
                r = self.session.delete(url, headers=headers, timeout=15)
            elif method == 'PATCH':
                r = self.session.patch(url, json=body, headers=headers, timeout=15)
            else:
                r = self.session.get(url, headers=headers, timeout=15)
            return r.status_code, r.text[:2000]
        except Exception as e:
            return 0, str(e)

    def _analyze(self, target, status_u1, resp_u1, status_u2, resp_u2):
        idor_likely = False
        sev = 'info'
        notes = []
        
        if status_u1 == 200 and status_u2 == 200:
            if resp_u1 != resp_u2:
                idor_likely = True
                sev = target.risk_level
                notes.append('Both users got 200 OK with DIFFERENT data')
                notes.append(f'len(u1)={len(resp_u1)} len(u2)={len(resp_u2)}')
            else:
                notes.append('Both users got identical 200 responses (may be public)')
        elif status_u2 == 200:
            if status_u1 in [401, 403, 0]:
                idor_likely = True
                sev = 'critical'
                notes.append(f'User2 accessed resource despite User1 denied ({status_u1})')
            else:
                idor_likely = True
                sev = target.risk_level
                notes.append('User2 got 200 OK (possible cross-workspace IDOR)')
        elif status_u1 != status_u2:
            idor_likely = True
            sev = target.risk_level
            notes.append(f'Different status codes: U1={status_u1} U2={status_u2}')
        elif status_u1 in [401, 403] and status_u2 in [401, 403]:
            notes.append('Both denied (401/403) - properly secured')
        elif status_u1 == 404 and status_u2 == 404:
            notes.append('Not found for both')
        else:
            notes.append(f'U1:{status_u1} U2:{status_u2} - manual review')
        
        return idor_likely, sev, '; '.join(notes)

    def _base_url_for(self, product):
        mapping = {
            'jira': self.config.get('base_jira', f"https://{self.config.get('target', '')}.atlassian.net" if self.config.get('target') else ''),
            'confluence': self.config.get('base_confluence', f"https://{self.config.get('target', '')}.atlassian.net/wiki" if self.config.get('target') else ''),
            'bitbucket': self.config.get('base_bitbucket', 'https://api.bitbucket.org'),
            'trello': self.config.get('base_trello', 'https://api.trello.com'),
        }
        return mapping.get(product, '')

    def _make_auth_url(self, base, url, user_num, product):
        """Add Trello auth query params directly."""
        if product == 'trello':
            key = self.config.get(f'trello_key{user_num}', '')
            token = self.config.get(f'trello_token{user_num}', '')
            if key and token:
                sep = '&' if '?' in url else '?'
                url += f'{sep}key={key}&token={token}'
        return url

    def discover(self, target, user_num=1):
        base = self._base_url_for(target.product)
        found = []
        for ep in target.discovery_endpoints:
            if not ep: continue
            url = self._base_url_for(target.product)
            full_url = self._build_url(url, ep, '__discover__', target.product)
            status, body = self._make_request(user_num, 'GET', full_url)
            if status != 200: continue
            try:
                data = json.loads(body)
                if target.product == 'jira':
                    if 'issues' in data:
                        for i in data['issues'][:5]:
                            rid = i.get('id') or i.get('key', '')
                            if rid: found.append(rid)
                    elif 'values' in data:
                        for i in data['values'][:10]:
                            rid = i.get('id') or i.get('key', '')
                            if rid: found.append(rid)
                    elif isinstance(data, list):
                        for i in data[:10]:
                            rid = i.get('id') or i.get('key', '')
                            if rid: found.append(rid)
                elif target.product == 'confluence':
                    if 'results' in data:
                        for p in data['results'][:5]:
                            rid = p.get('id', '')
                            if rid: found.append(rid)
                    elif isinstance(data, list):
                        for i in data[:10]:
                            rid = i.get('id', '')
                            if rid: found.append(rid)
                elif target.product == 'bitbucket':
                    if 'values' in data:
                        for r in data['values'][:5]:
                            rid = r.get('slug', '')
                            if rid: found.append(rid)
                    elif isinstance(data, list):
                        for i in data[:10]:
                            rid = i.get('slug', '')
                            if rid: found.append(rid)
                elif target.product == 'trello':
                    if isinstance(data, list):
                        for i in data[:10]:
                            rid = i.get('id') or i.get('shortLink', '')
                            if rid: found.append(rid)
                    elif 'boards' in data:
                        for b in data['boards'][:5]:
                            rid = b.get('id') or b.get('shortLink', '')
                            if rid: found.append(rid)
            except (json.JSONDecodeError, KeyError):
                pass
        return list(dict.fromkeys(found))

    def test(self, target, resource_id):
        base = self._base_url_for(target.product)
        url_template = self._build_url(base, target.path_template, resource_id, target.product)
        
        write_payloads = {'PUT': {'test': 'idor_check'}, 'POST': {'test': 'idor_check'},
                         'PATCH': {'test': 'idor_check'}, 'DELETE': {}}
        payload = write_payloads.get(target.method)
        
        u1_url = self._make_auth_url(base, url_template, 1, target.product)
        u2_url = self._make_auth_url(base, url_template, 2, target.product)
        
        s1, r1 = self._make_request(1, target.method, u1_url, payload)
        s2, r2 = self._make_request(2, target.method, u2_url, payload)
        
        idor, sev, notes = self._analyze(target, s1, r1, s2, r2)
        
        return TestResult(
            product=target.product.upper(), method=target.method,
            endpoint=target.path_template, full_url=url_template,
            status_u1=s1, status_u2=s2, response_u1=r1[:500], response_u2=r2[:500],
            idor_likely=idor, severity=sev, notes=notes
        )

    def run(self):
        import time as tmod
        start = tmod.time()
        
        products = []
        if self.config.get('jira_user1') and self.config.get('jira_user2'): products.append('jira')
        if self.config.get('confluence_user1') and self.config.get('confluence_user2'): products.append('confluence')
        if self.config.get('bitbucket_user1') and self.config.get('bitbucket_user2'): products.append('bitbucket')
        if self.config.get('trello_key1') or self.config.get('trello_token1'): products.append('trello')
        
        if not products:
            print("[!] No valid auth pairs configured.")
            return
        
        cases = [tc for tc in HIGH_RISK_TEST_CASES if tc.product in products]
        resources = self.config.get('resource_ids', [])
        
        if self.config.get('auto_discover', False):
            print("\n[+] Auto-discovery mode active...")
            for tc in cases:
                if tc.discovery_endpoints:
                    found = self.discover(tc, 1)
                    resources.extend(found)
            resources = list(dict.fromkeys(resources))
            print(f"[+] Discovered {len(resources)} resource IDs\n")
        
        if not resources:
            print("[!] No resource IDs. Provide via --issue-key, --project-id, --page-id, etc.")
            print("    Or use --auto-discover")
            return
        
        print(f"\n{'='*70}")
        print(f"  Atlassian IDOR Testing - Products: {', '.join(products)}")
        print(f"  Resources: {len(resources)} | Cases: {len(cases)}")
        print(f"  Time: {tmod.strftime('%Y-%m-%d %H:%M:%S UTC', tmod.gmtime())}")
        print(f"{'='*70}\n")
        
        total = 0
        found_idor = 0
        
        for rid in resources:
            print(f"  --- Testing: {rid} ---")
            for tc in cases:
                result = self.test(tc, rid)
                self.results.append(result)
                total += 1
                icon = "IDOR!" if result.idor_likely else "OK"
                print(f"  [{icon:5s}] {result.product:12s} {result.method} {tc.path_template}")
                print(f"         U1:{result.status_u1} U2:{result.status_u2} | {result.notes[:100]}")
                if result.idor_likely: found_idor += 1
                time.sleep(self.delay)
        
        elapsed = tmod.time() - start
        print(f"\n{'='*70}")
        print(f"  COMPLETE: {total} tests, {found_idor} potential IDORs, {elapsed:.0f}s")
        print(f"{'='*70}")
        
        idor_results = [r for r in self.results if r.idor_likely]
        for i, r in enumerate(idor_results, 1):
            print(f"\n  [{i}] {r.product} {r.method} {r.endpoint}")
            print(f"      Severity: {r.severity.upper()} | U1:{r.status_u1} U2:{r.status_u2}")
            print(f"      URL: {r.full_url}")
            print(f"      {r.notes}")
        
        self._save()
        return self.results

    def _save(self):
        ts = time.strftime('%Y%m%d_%H%M%S', time.gmtime())
        csv_p = f'atlassian_idor_results_{ts}.csv'
        if self.results:
            with open(csv_p, 'w', newline='') as f:
                w = csv.writer(f)
                w.writerow(['Product','Method','Endpoint','URL','Status_U1','Status_U2','IDOR','Severity','Notes'])
                for r in self.results:
                    w.writerow([r.product,r.method,r.endpoint,r.full_url,r.status_u1,r.status_u2,r.idor_likely,r.severity,r.notes])
            print(f"\n[+] CSV: {csv_p}")
        
        json_p = f'atlassian_idor_results_{ts}.json'
        with open(json_p, 'w') as f:
            json.dump([asdict(r) for r in self.results], f, indent=2)
        print(f"[+] JSON: {json_p}")


def parse_args():
    p = argparse.ArgumentParser(description='Atlassian IDOR Testing Framework')
    p.add_argument('--target', help='Atlassian site name (e.g., company)')
    p.add_argument('--base-jira', help='Jira base URL')
    p.add_argument('--base-confluence', help='Confluence base URL')
    p.add_argument('--base-bitbucket', help='Bitbucket base URL')
    p.add_argument('--base-trello', help='Trello base URL')
    p.add_argument('--workspace', help='Bitbucket workspace')
    p.add_argument('--jira-user1', help='Jira auth User 1')
    p.add_argument('--jira-user2', help='Jira auth User 2')
    p.add_argument('--jira-email1', help='Jira email User 1')
    p.add_argument('--jira-email2', help='Jira email User 2')
    p.add_argument('--confluence-user1', help='Confluence auth User 1')
    p.add_argument('--confluence-user2', help='Confluence auth User 2')
    p.add_argument('--confluence-email1', help='Confluence email User 1')
    p.add_argument('--confluence-email2', help='Confluence email User 2')
    p.add_argument('--bitbucket-user1', help='Bitbucket auth User 1')
    p.add_argument('--bitbucket-user2', help='Bitbucket auth User 2')
    p.add_argument('--trello-key1', help='Trello Key User 1')
    p.add_argument('--trello-token1', help='Trello Token User 1')
    p.add_argument('--trello-key2', help='Trello Key User 2')
    p.add_argument('--trello-token2', help='Trello Token User 2')
    p.add_argument('--resource-id')
    p.add_argument('--project-id', help='Jira project ID')
    p.add_argument('--issue-key', help='Jira issue key')
    p.add_argument('--page-id', help='Confluence page ID')
    p.add_argument('--board-id', help='Trello board ID')
    p.add_argument('--card-id', help='Trello card ID')
    p.add_argument('--auto-discover', action='store_true')
    p.add_argument('--dry-run', action='store_true')
    p.add_argument('--product', nargs='+', choices=['jira','confluence','bitbucket','trello'])
    p.add_argument('--delay', type=float, default=0.5)
    p.add_argument('--verbose', '-v', action='store_true')
    return p.parse_args()

def main():
    args = parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                       format='%(asctime)s [%(levelname)s] %(message)s')
    
    config = {
        'target': args.target, 'base_jira': args.base_jira,
        'base_confluence': args.base_confluence, 'base_bitbucket': args.base_bitbucket,
        'base_trello': args.base_trello, 'workspace': args.workspace,
        'jira_user1': args.jira_user1, 'jira_user2': args.jira_user2,
        'jira_email1': args.jira_email1, 'jira_email2': args.jira_email2,
        'confluence_user1': args.confluence_user1, 'confluence_user2': args.confluence_user2,
        'confluence_email1': args.confluence_email1, 'confluence_email2': args.confluence_email2,
        'bitbucket_user1': args.bitbucket_user1, 'bitbucket_user2': args.bitbucket_user2,
        'trello_key1': args.trello_key1, 'trello_token1': args.trello_token1,
        'trello_key2': args.trello_key2, 'trello_token2': args.trello_token2,
        'auto_discover': args.auto_discover, 'delay': args.delay,
    }
    
    rids = []
    for v in [args.resource_id, args.project_id, args.issue_key, args.page_id, args.board_id, args.card_id]:
        if v: rids.extend([x.strip() for x in v.split(',')])
    config['resource_ids'] = rids
    
    if args.dry_run:
        print("\n=== DRY RUN - Test Cases ===\n")
        for tc in HIGH_RISK_TEST_CASES:
            if args.product and tc.product not in args.product: continue
            print(f"  {tc.product.upper():12s} {tc.method:6s} {tc.path_template}")
            print(f"              Risk: {tc.risk_level.upper():8s} | {tc.description}")
        return
    
    has_auth = any([
        config.get('jira_user1') and config.get('jira_user2'),
        config.get('confluence_user1') and config.get('confluence_user2'),
        config.get('bitbucket_user1') and config.get('bitbucket_user2'),
        config.get('trello_key1') or config.get('trello_token1'),
    ])
    if not has_auth:
        print("[!] Auth required. Example: --jira-user1 TOKEN1 --jira-user2 TOKEN2")
        sys.exit(1)
    
    tester = AtlassianIDORTester(config)
    results = tester.run()
    if results:
        if any(r.idor_likely for r in results):
            sys.exit(1)
        sys.exit(0)
    sys.exit(0)

if __name__ == '__main__':
    main()
