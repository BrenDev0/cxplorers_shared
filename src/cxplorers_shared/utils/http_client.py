import httpx
import ssl
import os
from typing import Dict, Any, Optional

class SecureHTTPClient:
    """
    Secure HTTP client for service-to-service communication with mTLS.
    
    Usage:
        client = SecureHTTPClient("gateway")
        response = await client.call_service("https://company-service:8001/data")
    """
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.ssl_context = self._setup_ssl()
    
    def _setup_ssl(self) -> ssl.SSLContext:
        """Setup SSL context with mTLS."""
        ssl_context = ssl.create_default_context()
        
        # Load service certificate and key
        cert_file = os.getenv('SERVICE_SSL_CERT', f'/app/certs/{self.service_name}.crt')
        key_file = os.getenv('SERVICE_SSL_KEY', f'/app/certs/{self.service_name}.key')
        ca_file = os.getenv('SERVICE_SSL_CA', '/app/certs/ca.crt')
        
        if os.path.exists(cert_file) and os.path.exists(key_file):
            ssl_context.load_cert_chain(certfile=cert_file, keyfile=key_file)
        else:
            raise FileNotFoundError(f"Certificate files not found: {cert_file}, {key_file}")
        
        # Trust the CA
        if os.path.exists(ca_file):
            ssl_context.load_verify_locations(cafile=ca_file)
        else:
            raise FileNotFoundError(f"CA certificate not found: {ca_file}")
        
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        return ssl_context
    
    async def call_service(
        self, 
        url: str, 
        data: Optional[Dict[str, Any]] = None,
        method: str = "GET",
        timeout: float = 30.0
    ) -> Dict[str, Any]:
        """
        Make a secure call to another service.
        
        Args:
            url: The service URL to call
            data: Data to send (for POST/PUT requests)
            method: HTTP method (GET, POST, PUT, DELETE)
            timeout: Request timeout in seconds
            
        Returns:
            Response JSON as dictionary
        """
        async with httpx.AsyncClient(verify=self.ssl_context) as client:
            try:
                if method.upper() == "POST":
                    response = await client.post(url, json=data, timeout=timeout)
                elif method.upper() == "PUT":
                    response = await client.put(url, json=data, timeout=timeout)
                elif method.upper() == "DELETE":
                    response = await client.delete(url, timeout=timeout)
                elif method.uppser() =="PATCH":
                    response = await client.put(url, json=data, timeout=timeout)
                else:  # GET
                    response = await client.get(url, timeout=timeout)

                response.raise_for_status()
                return response.json()
                
            except httpx.ConnectError as e:
                return {"error": f"Cannot connect to {url}: {str(e)}"}
            except httpx.HTTPStatusError as e:
                return {"error": f"HTTP error {e.response.status_code}: {e.response.text}"}
            except Exception as e:
                return {"error": f"Request failed: {str(e)}"}