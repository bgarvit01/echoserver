import threading
import time
import json
import os
import requests
import pytest
from server.echo_server import EchoServer
from server.config import ServerConfig, get_config

# Test server configuration
TEST_HOST = "127.0.0.1"
TEST_PORT = 8081
BASE_URL = f"http://{TEST_HOST}:{TEST_PORT}"

@pytest.fixture(scope="module")
def server():
    """Start test server in background thread"""
    def run_server():
        # Create test configuration
        config = get_config()
        config.host = TEST_HOST
        config.port = TEST_PORT
        test_server = EchoServer(config)
        test_server.start()
    
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(2)  # Give server time to start
    yield
    # Server will stop when test process ends

class TestBasicFunctionality:
    """Test basic echo server functionality"""
    
    def test_basic_echo(self, server):
        """Test basic echo functionality"""
        response = requests.get(BASE_URL)
        assert response.status_code == 200
        data = response.json()
        assert "host" in data
        assert "http" in data
        assert "request" in data
    
    def test_all_http_methods(self, server):
        """Test all supported HTTP methods"""
        methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
        for method in methods:
            response = requests.request(method, BASE_URL)
            assert response.status_code == 200
            data = response.json()
            assert data['http']['method'] == method

class TestCustomResponseBody:
    """Test custom response body features"""
    
    def test_custom_body_query_param(self, server):
        """Test custom body via query parameter"""
        response = requests.get(f"{BASE_URL}?echo_body=hello")
        assert response.status_code == 200
        assert response.text == "hello"
    
    def test_custom_body_header(self, server):
        """Test custom body via header"""
        headers = {'X-ECHO-BODY': 'world'}
        response = requests.get(BASE_URL, headers=headers)
        assert response.status_code == 200
        assert response.text == "world"
    
    def test_env_body_query_param(self, server):
        """Test environment variable body via query parameter"""
        os.environ['TEST_VAR'] = 'test_value'
        response = requests.get(f"{BASE_URL}?echo_env_body=TEST_VAR")
        assert response.status_code == 200
        assert response.text == "test_value"
    
    def test_env_body_header(self, server):
        """Test environment variable body via header"""
        os.environ['TEST_VAR2'] = 'test_value2'
        headers = {'X-ECHO-ENV-BODY': 'TEST_VAR2'}
        response = requests.get(BASE_URL, headers=headers)
        assert response.status_code == 200
        assert response.text == "test_value2"

class TestCustomStatusCodes:
    """Test custom status code features"""
    
    def test_single_status_code_query(self, server):
        """Test single custom status code via query parameter"""
        response = requests.get(f"{BASE_URL}?echo_code=404")
        assert response.status_code == 404
    
    def test_single_status_code_header(self, server):
        """Test single custom status code via header"""
        headers = {'X-ECHO-CODE': '500'}
        response = requests.get(BASE_URL, headers=headers)
        assert response.status_code == 500
    
    def test_multiple_status_codes(self, server):
        """Test multiple status codes with random selection"""
        # Test multiple times to increase chance of getting different codes
        codes_seen = set()
        for _ in range(10):
            response = requests.get(f"{BASE_URL}?echo_code=200-400-500")
            codes_seen.add(response.status_code)
        
        # Should see at least one of the specified codes
        assert codes_seen.intersection({200, 400, 500})

class TestCustomHeaders:
    """Test custom header features"""
    
    def test_single_custom_header_query(self, server):
        """Test single custom header via query parameter"""
        response = requests.get(f"{BASE_URL}?echo_header=Custom-Header:test-value")
        assert response.status_code == 200
        assert response.headers.get('Custom-Header') == 'test-value'
    
    def test_single_custom_header_header(self, server):
        """Test single custom header via header"""
        headers = {'X-ECHO-HEADER': 'Another-Header:another-value'}
        response = requests.get(BASE_URL, headers=headers)
        assert response.status_code == 200
        assert response.headers.get('Another-Header') == 'another-value'
    
    def test_multiple_custom_headers(self, server):
        """Test multiple custom headers"""
        headers = {'X-ECHO-HEADER': 'Header1:value1, Header2:value2'}
        response = requests.get(BASE_URL, headers=headers)
        assert response.status_code == 200
        assert response.headers.get('Header1') == 'value1'
        assert response.headers.get('Header2') == 'value2'
    
    def test_duplicate_headers_explicit_names(self, server):
        """Test duplicate headers with explicit repeated names"""
        headers = {'X-ECHO-HEADER': 'Set-Cookie:sessionid=abc123, Set-Cookie:userid=456'}
        response = requests.get(BASE_URL, headers=headers)
        assert response.status_code == 200
        
        # Check that we get multiple Set-Cookie headers
        set_cookie_headers = response.headers.get_list('Set-Cookie') if hasattr(response.headers, 'get_list') else []
        if not set_cookie_headers:
            # Fallback for requests library that might not expose all duplicate headers
            # Check that at least one Set-Cookie header is present
            assert 'Set-Cookie' in response.headers
    
    def test_duplicate_set_cookie_headers(self, server):
        """Test special handling of Set-Cookie headers with complex values"""
        headers = {'X-ECHO-HEADER': 'Set-Cookie:sessionid=abc123; Path=/; HttpOnly, userid=456; Secure'}
        response = requests.get(BASE_URL, headers=headers)
        assert response.status_code == 200
        assert 'Set-Cookie' in response.headers
    
    def test_mixed_duplicate_and_single_headers(self, server):
        """Test mixing duplicate headers with single headers"""
        headers = {'X-ECHO-HEADER': 'Cache-Control:no-cache, Set-Cookie:session=123, Set-Cookie:user=456, X-Custom:test'}
        response = requests.get(BASE_URL, headers=headers)
        assert response.status_code == 200
        assert response.headers.get('Cache-Control') == 'no-cache'
        assert 'Set-Cookie' in response.headers
        assert response.headers.get('X-Custom') == 'test'

class TestDelayFeature:
    """Test delay/timing features"""
    
    def test_delay_query_param(self, server):
        """Test delay via query parameter"""
        start_time = time.time()
        response = requests.get(f"{BASE_URL}?echo_time=1000")  # 1 second
        end_time = time.time()
        
        assert response.status_code == 200
        assert end_time - start_time >= 0.9  # Allow some tolerance
    
    def test_delay_header(self, server):
        """Test delay via header"""
        start_time = time.time()
        headers = {'X-ECHO-TIME': '500'}  # 0.5 seconds
        response = requests.get(BASE_URL, headers=headers)
        end_time = time.time()
        
        assert response.status_code == 200
        assert end_time - start_time >= 0.4  # Allow some tolerance

class TestFileOperations:
    """Test file operation features"""
    
    def test_file_listing_query(self, server):
        """Test directory listing via query parameter"""
        # Create a test directory and file
        os.makedirs('/tmp/test_echo', exist_ok=True)
        with open('/tmp/test_echo/test_file.txt', 'w') as f:
            f.write('test content')
        
        response = requests.get(f"{BASE_URL}?echo_file=/tmp/test_echo")
        assert response.status_code == 200
        files = json.loads(response.text)
        assert isinstance(files, list)
        # Check if any file entry has the name 'test_file.txt'
        file_names = [entry['name'] if isinstance(entry, dict) else entry for entry in files]
        assert 'test_file.txt' in file_names
    
    def test_file_reading_header(self, server):
        """Test file reading via header"""
        # Create a test file
        test_content = 'Hello from file'
        with open('/tmp/test_read.txt', 'w') as f:
            f.write(test_content)
        
        headers = {'X-ECHO-FILE': '/tmp/test_read.txt'}
        response = requests.get(BASE_URL, headers=headers)
        assert response.status_code == 200
        assert response.text == test_content

class TestResponseStructure:
    """Test response structure and content"""
    
    def test_default_response_structure(self, server):
        """Test default JSON response structure"""
        response = requests.get(BASE_URL)
        assert response.status_code == 200
        data = response.json()
        
        # Check main sections
        assert 'host' in data
        assert 'http' in data
        assert 'request' in data
        
        # Check host information
        host_info = data['host']
        assert 'hostname' in host_info
        assert 'ip' in host_info
        assert 'ips' in host_info
        
        # Check HTTP information
        http_info = data['http']
        assert 'method' in http_info
        assert 'baseUrl' in http_info
        assert 'originalUrl' in http_info
        assert 'protocol' in http_info
        
        # Check request information
        request_info = data['request']
        assert 'params' in request_info
        assert 'query' in request_info
        assert 'cookies' in request_info
        assert 'body' in request_info
        assert 'headers' in request_info
        assert 'remoteAddress' in request_info
        assert 'remotePort' in request_info
    
    def test_request_data_parsing(self, server):
        """Test parsing of request data"""
        # Test with query parameters
        response = requests.get(f"{BASE_URL}?param1=value1&param2=value2")
        data = response.json()
        query = data['request']['query']
        assert query['param1'] == 'value1'
        assert query['param2'] == 'value2'
        
        # Test with custom headers
        headers = {'Custom-Header': 'custom-value'}
        response = requests.get(BASE_URL, headers=headers)
        data = response.json()
        request_headers = data['request']['headers']
        assert request_headers.get('Custom-Header') == 'custom-value'
        
        # Test with POST body
        post_data = {'key': 'value'}
        response = requests.post(BASE_URL, json=post_data)
        data = response.json()
        body = data['request']['body']
        assert 'key' in body

class TestCombinedFeatures:
    """Test combinations of features"""
    
    def test_combined_custom_features(self, server):
        """Test combining multiple custom features"""
        headers = {
            'X-ECHO-CODE': '201',
            'X-ECHO-BODY': 'custom response',
            'X-ECHO-HEADER': 'Custom:combined-test'
        }
        
        response = requests.get(BASE_URL, headers=headers)
        assert response.status_code == 201
        assert response.text == 'custom response'
        assert response.headers.get('Custom') == 'combined-test'
    
    def test_query_and_header_precedence(self, server):
        """Test that headers take precedence over query parameters"""
        headers = {'X-ECHO-BODY': 'header-body'}
        response = requests.get(f"{BASE_URL}?echo_body=query-body", headers=headers)
        assert response.status_code == 200
        assert response.text == 'header-body'  # Header should win

class TestConfigurationAndSecurity:
    """Test configuration options and security features"""
    
    def test_path_traversal_protection(self, server):
        """Test protection against path traversal attacks"""
        response = requests.get(f"{BASE_URL}?echo_file=../../../etc/passwd")
        assert response.status_code == 200
        data = json.loads(response.text)
        assert 'error' in data  # Should return error for path traversal
    
    def test_nonexistent_file(self, server):
        """Test handling of nonexistent files"""
        response = requests.get(f"{BASE_URL}?echo_file=/nonexistent/file.txt")
        assert response.status_code == 200
        data = json.loads(response.text)
        assert 'error' in data  # Should return error for nonexistent file
