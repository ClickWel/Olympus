#!/bin/bash
echo "=== Deep API Scan: New Relic ==="
echo ""
echo "--- Checking login endpoint ---"
curl -s -I "https://login.newrelic.com" -w "\nHTTP_CODE: %{http_code}\n" 2>/dev/null | head -30
echo ""
echo "--- Checking login newrelic.com/install-newrelic/router ---"
curl -s -o /dev/null -w "HTTP_CODE: %{http_code} REDIRECT: %{redirect_url}\n" "https://login.newrelic.com/install-newrelic/router" 2>/dev/null
echo ""
echo "--- Checking social login endpoint (US) ---"
curl -s -o /dev/null -w "HTTP_CODE: %{http_code} REDIRECT: %{redirect_url}\n" "https://one.newrelic.com/install-newrelic/router" 2>/dev/null
echo ""
echo "--- Trying to register via insights-collector (data leak?) ---"  
curl -s -X POST "https://insights-collector.newrelic.com/v1/accounts/1/events" \
  -H "Content-Type: application/json" \
  -H "Api-Key: test" \
  -d '[{"eventType":"test","name":"test"}]' \
  -w "\nHTTP_CODE: %{http_code}\n" 2>/dev/null
echo ""
echo "--- Checking for public GraphQL introspection ---"
curl -s -X POST "https://api.newrelic.com/graphql" \
  -H "Content-Type: application/json" \
  -d '{"query":"{__schema {types {name fields {name}}}}"}' \
  -w "\nHTTP_CODE: %{http_code}\n" 2>/dev/null
echo ""
echo "--- Checking license key endpoint ---"
curl -s -X POST "https://insights-collector.newrelic.com/v1/accounts/1202289/events" \
  -H "Content-Type: application/json" \
  -d '[{"eventType":"test","name":"recon_test"}]' \
  -w "\nHTTP_CODE: %{http_code}\n" 2>/dev/null
echo ""
echo "--- Checking agent connect endpoint ---"
curl -s -X POST "https://collector.newrelic.com/agent_listener/invoke_raw_method" \
  -H "Content-Type: application/json" \
  -d '{"method":"get_redirect_host","protocol_version":15}' \
  -w "\nHTTP_CODE: %{http_code}\n" 2>/dev/null
echo ""
echo "--- Checking EU API endpoint ---"
curl -s -o /dev/null -w "HTTP_CODE: %{http_code}\n" "https://api.eu.newrelic.com/v2/applications.json" 2>/dev/null
