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
        self.token = None
        
        # APIエンドポイントの設定
        self.api_endpoints = {
            'app_progress': '/api/patent/v1/app_progress',
            'app_progress_simple': '/api/patent/v1/app_progress_simple',
            'divisional_app_info': '/api/patent/v1/divisional_app_info',
            'priority_right_app_info': '/api/patent/v1/priority_right_app_info',
            'applicant_attorney_cd': '/api/patent/v1/applicant_attorney_cd',
            'applicant_attorney_name': '/api/patent/v1/applicant_attorney_name',
            'pub_num': '/api/patent/v1/pub_num',
            'reg_num': '/api/patent/v1/reg_num',
            'app_doc_cont_refusal_reason_decision': '/api/patent/v1/app_doc_cont_refusal_reason_decision',
            'app_doc_cont_refusal_reason': '/api/patent/v1/app_doc_cont_refusal_reason',
            'cite_doc_info': '/api/patent/v1/cite_doc_info',
            'registration_info': '/api/patent/v1/registration_info',
            'jpp_fixed_address': '/api/patent/v1/jpp_fixed_address',
            'pct_app_num': '/api/patent/v1/pct_app_num'
        }
        
        # ファイルダウンロード系のAPI
        self.download_apis = {
            'app_doc_cont_refusal_reason_decision',
            'app_doc_cont_refusal_reason'
        }
    
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
    
    def get_patent_data(self, api_type, search_input):
        if not self.token:
            if not self.get_token():
                return None
        
        if api_type not in self.api_endpoints:
            logger.error(f"Unsupported API type: {api_type}")
            return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Accept': 'application/json'
            }
            
            endpoint = self.api_endpoints[api_type]
            url = f"{self.base_url}{endpoint}/{search_input}"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # ファイルダウンロード系のAPIの場合
            if api_type in self.download_apis:
                return {
                    'success': True,
                    'message': 'ファイルダウンロードAPIの場合、ファイルが返されます。',
                    'content_type': response.headers.get('Content-Type', 'application/zip'),
                    'content_length': response.headers.get('Content-Length', 'unknown'),
                    'api_type': api_type,
                    'search_input': search_input
                }
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Patent data retrieval failed for {api_type}: {str(e)}")
            return None
    
    def get_api_description(self, api_type):
        descriptions = {
            'app_progress': '特許経過情報API - 出願番号に基づき経過情報の一覧を取得',
            'app_progress_simple': 'シンプル特許経過情報API - 優先権情報などを除いた簡易情報',
            'divisional_app_info': '特許分割出願情報API - 分割出願に関する情報',
            'priority_right_app_info': '特許優先基礎出願情報API - 優先権に関する基礎出願情報',
            'applicant_attorney_cd': '特許申請人氏名・名称API - 申請人コードから氏名・名称を取得',
            'applicant_attorney_name': '特許申請人コードAPI - 申請人名称からコードを取得',
            'pub_num': '特許出願公開番号API - 出願番号から公開番号を取得',
            'reg_num': '特許登録番号API - 出願番号から登録番号を取得',
            'app_doc_cont_refusal_reason_decision': '特許発送書類の実体ファイルAPI - 発送書類のZIPファイルダウンロード',
            'app_doc_cont_refusal_reason': '特許拒絶理由通知書API - 拒絶理由通知書のZIPファイルダウンロード',
            'cite_doc_info': '特許引用文献情報取得API - 拒絶理由の引用文献情報',
            'registration_info': '特許登録情報API - 特定の出願番号の登録情報',
            'jpp_fixed_address': '特許J-PlatPat固定アドレスAPI - J-PlatPat固定アドレス情報',
            'pct_app_num': '特許PCT出願の日本国内移行後の出願番号API - PCT出願番号から日本国内移行後の出願番号を取得'
        }
        return descriptions.get(api_type, 'APIの説明がありません')

@csrf_exempt
@require_http_methods(["POST"])
def search_patent(request):
    try:
        data = json.loads(request.body)
        api_type = data.get('api_type', 'app_progress').strip()
        search_input = data.get('search_input', '').strip()
        
        if not search_input:
            return JsonResponse({
                'error': '検索値が入力されていません'
            }, status=400)
        
        # API credentials check
        if not settings.PATENT_API_USERNAME or not settings.PATENT_API_PASSWORD:
            return JsonResponse({
                'error': 'API認証情報が設定されていません'
            }, status=500)
        
        # Create API client and get patent data
        client = PatentAPIClient()
        patent_data = client.get_patent_data(api_type, search_input)
        
        if patent_data is None:
            return JsonResponse({
                'error': f'{client.get_api_description(api_type)}の取得に失敗しました'
            }, status=500)
        
        return JsonResponse({
            'success': True,
            'data': patent_data,
            'api_type': api_type,
            'search_input': search_input,
            'api_description': client.get_api_description(api_type)
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

@csrf_exempt
@require_http_methods(["GET"])
def get_api_list(request):
    """
    利用可能なAPIの一覧を返す
    """
    client = PatentAPIClient()
    api_list = []
    
    for api_type in client.api_endpoints.keys():
        api_list.append({
            'api_type': api_type,
            'description': client.get_api_description(api_type),
            'is_download': api_type in client.download_apis
        })
    
    return JsonResponse({
        'success': True,
        'api_list': api_list
    })
