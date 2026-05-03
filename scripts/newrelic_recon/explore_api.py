#!/usr/bin/env python3
"""New Relic API Exploration Script"""
import requests
import json
import sys
from urllib.parse import urljoin

def test_endpoint(base, path, method="GET", headers=None, data=None, description=""):
    url = urljoin(base, path)
    try:
        h = headers or {}
        if method == "GET":
            r = requests.get(url, headers=h, allow_redirects=False, timeout=10)
        elif method == "POST":
            r = requests.post(url, headers=h, json=data, allow_redirects=False, timeout=10)
        return {
            "url": url, "method": method, "status": r.status_code,
            "content_type": r.headers.get("Content-Type", ""),
            "description": description,
            "response_sample": r.text[:300] if r.status_code != 302 else "",
            "is_idor_candidate": any(c.isdigit() for c in path.split('/')[-1] if c.isdigit()),
        }
    except Exception as e:
        return {"url": url, "error": str(e), "description": description}

if __name__ == "__main__":
    results = []
    paths = [
        ("https://api.newrelic.com", "/v2/accounts.json", "GET", "REST v2: List accounts"),
        ("https://api.newrelic.com", "/v2/accounts/1.json", "GET", "REST v2: Account 1"),  
        ("https://api.newrelic.com", "/v2/applications.json", "GET", "REST v2: Applications"),
        ("https://api.newrelic.com", "/v2/applications/1.json", "GET", "REST v2: Application 1"),
        ("https://api.newrelic.com", "/v2/users.json", "GET", "REST v2: Users"),
        ("https://api.newrelic.com", "/v2/users/1.json", "GET", "REST v2: User 1"),
        ("https://api.newrelic.com", "/v2/alerts_policies.json", "GET", "REST v2: Alert policies"),
        ("https://api.newrelic.com", "/v2/alerts_channels.json", "GET", "REST v2: Alert channels"),
        ("https://api.newrelic.com", "/v2/key_transactions.json", "GET", "REST v2: Key transactions"),
        ("https://api.newrelic.com", "/v2/servers.json", "GET", "REST v2: Servers"),
        ("https://api.newrelic.com", "/v2/labels.json", "GET", "REST v2: Labels"),
        ("https://api.newrelic.com", "/v2/plugins.json", "GET", "REST v2: Plugins"),
        ("https://api.newrelic.com", "/graphql", "POST", "NerdGraph GraphQL"),
        ("https://api.eu.newrelic.com", "/graphql", "POST", "NerdGraph EU"),
        ("https://synthetics.newrelic.com", "/v4/monitors", "GET", "Synthetics monitors"),
        ("https://insights.newrelic.com", "/v1/accounts/1/events", "GET", "Insights events"),
    ]
    
    for base, path, method, desc in paths:
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        data = {"query": "{ actor { accounts { id name } } }"} if method == "POST" else None
        r = test_endpoint(base, path, method, headers=headers, data=data, description=desc)
        print(f"{method} {r['url']} -> {r.get('status', 'ERROR')} | IDOR:{r.get('is_idor_candidate', False)}")
        if r.get('response_sample'):
            print(f"  Response: {r['response_sample'][:200]}")
        results.append(r)
    
    print(f"\nTested {len(results)} endpoints")
