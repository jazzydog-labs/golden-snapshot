#!/bin/bash
set -e

API_URL="http://localhost:8000"

echo "🧪 Running smoke tests..."

# Test health endpoint
echo -n "Testing health endpoint... "
health_response=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/health)
if [ "$health_response" == "200" ]; then
    echo "✅ OK"
else
    echo "❌ FAILED (HTTP $health_response)"
    exit 1
fi

# Create a user
echo -n "Creating a user... "
user_response=$(curl -s -L -X POST $API_URL/users/ \
    -H "Content-Type: application/json" \
    -d '{"email": "test@example.com", "name": "Test User", "is_admin": false}')
user_id=$(echo $user_response | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
if [ -n "$user_id" ]; then
    echo "✅ OK (ID: $user_id)"
else
    echo "❌ FAILED"
    echo "Response: $user_response"
    exit 1
fi

# Get the user
echo -n "Getting the user... "
get_user_response=$(curl -s -w "\n%{http_code}" $API_URL/users/$user_id)
http_code=$(echo "$get_user_response" | tail -n1)
if [ "$http_code" == "200" ]; then
    echo "✅ OK"
else
    echo "❌ FAILED (HTTP $http_code)"
    exit 1
fi

# Create a post
echo -n "Creating a post... "
post_response=$(curl -s -L -X POST "$API_URL/posts/?user_id=$user_id" \
    -H "Content-Type: application/json" \
    -d '{"title": "Test Post", "content": "This is a test post", "published": true}')
post_id=$(echo $post_response | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
if [ -n "$post_id" ]; then
    echo "✅ OK (ID: $post_id)"
else
    echo "❌ FAILED"
    echo "Response: $post_response"
    exit 1
fi

# Get the post
echo -n "Getting the post... "
get_post_response=$(curl -s -w "\n%{http_code}" $API_URL/posts/$post_id)
http_code=$(echo "$get_post_response" | tail -n1)
if [ "$http_code" == "200" ]; then
    echo "✅ OK"
else
    echo "❌ FAILED (HTTP $http_code)"
    exit 1
fi

echo "🎉 All smoke tests passed!"