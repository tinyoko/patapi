from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
import json
import requests
import logging

logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'patent_search/index.html')

class PatentAPIClient:
    def __init__(self):
        self.base_url = settings.PATENT_API_BASE_URL
        self.username = settings.PATENT_API_USERNAME
        self.password = settings.PATENT_API_PASSWORD
        self.token_url = settings.PATENT_API_TOKEN_URL
        self.data_url = settings.PATENT_API_DATA_URL
        self.token = None
    
    def get_token(self):
        try:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'grant_type': 'password',
                'username': self.username,
                'password': self.password
            }
            
            response = requests.post(self.token_url, data=data, headers=headers)
            response.raise_for_status()
            
            token_data = response.json()
            self.token = token_data.get('access_token')
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Token acquisition failed: {str(e)}")
            return False
    
    def get_patent_data(self, application_number):
        if not self.token:
            if not self.get_token():
                return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Accept': 'application/json'
            }
            
            url = f"{self.data_url}/{application_number}"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Patent data retrieval failed: {str(e)}")
            return None

@csrf_exempt
@require_http_methods(["POST"])
def search_patent(request):
    try:
        data = json.loads(request.body)
        application_number = data.get('application_number', '').strip()
        
        if not application_number:
            return JsonResponse({
                'error': '出願番号が入力されていません'
            }, status=400)
        
        # API credentials check
        if not settings.PATENT_API_USERNAME or not settings.PATENT_API_PASSWORD:
            return JsonResponse({
                'error': 'API認証情報が設定されていません'
            }, status=500)
        
        # Create API client and get patent data
        client = PatentAPIClient()
        patent_data = client.get_patent_data(application_number)
        
        if patent_data is None:
            return JsonResponse({
                'error': '特許情報の取得に失敗しました'
            }, status=500)
        
        return JsonResponse({
            'success': True,
            'data': patent_data
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'error': '不正なJSONデータです'
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({
            'error': '予期しないエラーが発生しました'
        }, status=500)
