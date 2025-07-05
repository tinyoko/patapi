"""
OPD-API utilities for document retrieval and XML parsing
"""
import requests
import logging
from lxml import etree
from bs4 import BeautifulSoup
from django.conf import settings
import zipfile
import io
import re

logger = logging.getLogger(__name__)

class OPDAPIClient:
    """OPD-API client for document retrieval and parsing"""
    
    def __init__(self):
        self.base_url = settings.OPD_API_BASE_URL
        self.doc_list_url = settings.OPD_API_DOC_LIST_URL
        self.doc_content_url = settings.OPD_API_DOC_CONTENT_URL
        self.username = settings.PATENT_API_USERNAME
        self.password = settings.PATENT_API_PASSWORD
        self.token_url = settings.PATENT_API_TOKEN_URL
        self.token = None
    
    def get_token(self):
        """Get authentication token"""
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
    
    def get_document_list(self, application_number):
        """Get document list for a patent application"""
        if not self.token:
            if not self.get_token():
                return None
        
        try:
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Accept': 'application/json'
            }
            
            # DOCDB形式に変換（例：2014192333 → JP.2014192333.A）
            docdb_number = f"JP.{application_number}.A"
            url = f"https://ip-data.jpo.go.jp/opdapi/patent/v1/global_doc_list/{docdb_number}"
            logger.info(f"Accessing OPD API URL: {url}")
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Document list retrieval failed: {str(e)}")
            return None
    
    def get_jp_document_content(self, application_number, document_id=None):
        """Get Japanese document content (XML format)"""
        if not self.token:
            if not self.get_token():
                return None
        
        try:
            # 書類IDが指定されていない場合、書類一覧から最初のものを取得
            if not document_id:
                doc_list = self.get_document_list(application_number)
                if not doc_list or not doc_list.get('data'):
                    logger.error("No document list found for JP document content")
                    return None
                
                # 最初の書類IDを使用（実際の実装では適切な書類を選択）
                documents = doc_list.get('data', [])
                if not documents:
                    logger.error("No documents found in the list")
                    return None
                
                document_id = documents[0].get('documentId', 'default')
            
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Accept': 'application/zip'  # ZIP file containing XML
            }
            
            # DOCDB形式に変換してURLパスに含める
            docdb_number = f"JP.{application_number}.A"
            url = f"https://ip-data.jpo.go.jp/opdapi/patent/v1/jp_doc_cont/{docdb_number}/{document_id}"
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.content
        except requests.exceptions.RequestException as e:
            logger.error(f"JP document content retrieval failed: {str(e)}")
            return None


class PatentXMLParser:
    """Parser for patent XML documents"""
    
    @staticmethod
    def extract_text_from_zip(zip_content):
        """Extract text content from ZIP file containing XML documents"""
        try:
            extracted_texts = {}
            
            with zipfile.ZipFile(io.BytesIO(zip_content), 'r') as zip_file:
                for filename in zip_file.namelist():
                    if filename.endswith('.xml'):
                        xml_content = zip_file.read(filename)
                        text_content = PatentXMLParser.parse_patent_xml(xml_content)
                        extracted_texts[filename] = text_content
            
            return extracted_texts
        except Exception as e:
            logger.error(f"ZIP extraction failed: {str(e)}")
            return {}
    
    @staticmethod
    def parse_patent_xml(xml_content):
        """Parse patent XML and extract Japanese text content"""
        try:
            # Parse XML using lxml
            root = etree.fromstring(xml_content)
            
            # Extract different sections
            result = {
                'title': PatentXMLParser._extract_title(root),
                'abstract': PatentXMLParser._extract_abstract(root),
                'claims': PatentXMLParser._extract_claims(root),
                'description': PatentXMLParser._extract_description(root),
                'technical_field': PatentXMLParser._extract_technical_field(root),
                'background_art': PatentXMLParser._extract_background_art(root),
                'disclosure': PatentXMLParser._extract_disclosure(root),
                'brief_description': PatentXMLParser._extract_brief_description(root),
                'detailed_description': PatentXMLParser._extract_detailed_description(root)
            }
            
            return result
        except Exception as e:
            logger.error(f"XML parsing failed: {str(e)}")
            return {}
    
    @staticmethod
    def _extract_title(root):
        """Extract patent title"""
        titles = []
        # Common XML paths for patent titles
        title_paths = [
            './/invention-title',
            './/title-of-invention',
            './/title',
            './/発明の名称'
        ]
        
        for path in title_paths:
            elements = root.xpath(path)
            for element in elements:
                text = PatentXMLParser._get_text_content(element)
                if text:
                    titles.append(text)
        
        return titles
    
    @staticmethod
    def _extract_abstract(root):
        """Extract abstract"""
        abstracts = []
        abstract_paths = [
            './/abstract',
            './/要約',
            './/summary'
        ]
        
        for path in abstract_paths:
            elements = root.xpath(path)
            for element in elements:
                text = PatentXMLParser._get_text_content(element)
                if text:
                    abstracts.append(text)
        
        return abstracts
    
    @staticmethod
    def _extract_claims(root):
        """Extract patent claims"""
        claims = []
        claim_paths = [
            './/claims//claim',
            './/特許請求の範囲//請求項',
            './/claim-text'
        ]
        
        for path in claim_paths:
            elements = root.xpath(path)
            for i, element in enumerate(elements, 1):
                text = PatentXMLParser._get_text_content(element)
                if text:
                    claims.append(f"請求項{i}: {text}")
        
        return claims
    
    @staticmethod
    def _extract_description(root):
        """Extract detailed description"""
        descriptions = []
        desc_paths = [
            './/detailed-description',
            './/description',
            './/発明の詳細な説明',
            './/明細書'
        ]
        
        for path in desc_paths:
            elements = root.xpath(path)
            for element in elements:
                text = PatentXMLParser._get_text_content(element)
                if text:
                    descriptions.append(text)
        
        return descriptions
    
    @staticmethod
    def _extract_technical_field(root):
        """Extract technical field"""
        fields = []
        field_paths = [
            './/technical-field',
            './/技術分野',
            './/field-of-invention'
        ]
        
        for path in field_paths:
            elements = root.xpath(path)
            for element in elements:
                text = PatentXMLParser._get_text_content(element)
                if text:
                    fields.append(text)
        
        return fields
    
    @staticmethod
    def _extract_background_art(root):
        """Extract background art"""
        backgrounds = []
        bg_paths = [
            './/background-art',
            './/背景技術',
            './/prior-art'
        ]
        
        for path in bg_paths:
            elements = root.xpath(path)
            for element in elements:
                text = PatentXMLParser._get_text_content(element)
                if text:
                    backgrounds.append(text)
        
        return backgrounds
    
    @staticmethod
    def _extract_disclosure(root):
        """Extract disclosure of invention"""
        disclosures = []
        disc_paths = [
            './/disclosure',
            './/発明の開示',
            './/invention-disclosure'
        ]
        
        for path in disc_paths:
            elements = root.xpath(path)
            for element in elements:
                text = PatentXMLParser._get_text_content(element)
                if text:
                    disclosures.append(text)
        
        return disclosures
    
    @staticmethod
    def _extract_brief_description(root):
        """Extract brief description of drawings"""
        brief_descs = []
        brief_paths = [
            './/brief-description-of-drawings',
            './/図面の簡単な説明',
            './/brief-description'
        ]
        
        for path in brief_paths:
            elements = root.xpath(path)
            for element in elements:
                text = PatentXMLParser._get_text_content(element)
                if text:
                    brief_descs.append(text)
        
        return brief_descs
    
    @staticmethod
    def _extract_detailed_description(root):
        """Extract detailed description of preferred embodiments"""
        detailed_descs = []
        detailed_paths = [
            './/detailed-description-of-preferred-embodiments',
            './/発明を実施するための最良の形態',
            './/detailed-description'
        ]
        
        for path in detailed_paths:
            elements = root.xpath(path)
            for element in elements:
                text = PatentXMLParser._get_text_content(element)
                if text:
                    detailed_descs.append(text)
        
        return detailed_descs
    
    @staticmethod
    def _get_text_content(element):
        """Extract text content from XML element, handling mixed content"""
        if element is None:
            return ""
        
        # Use BeautifulSoup for better text extraction
        soup = BeautifulSoup(etree.tostring(element, encoding='unicode'), 'xml')
        text = soup.get_text(separator=' ', strip=True)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    @staticmethod
    def format_extracted_text(parsed_data):
        """Format extracted text data for display"""
        formatted_sections = []
        
        section_mapping = {
            'title': '発明の名称',
            'abstract': '要約',
            'claims': '特許請求の範囲',
            'technical_field': '技術分野',
            'background_art': '背景技術',
            'disclosure': '発明の開示',
            'brief_description': '図面の簡単な説明',
            'detailed_description': '発明の詳細な説明',
            'description': '明細書'
        }
        
        for key, title in section_mapping.items():
            if key in parsed_data and parsed_data[key]:
                content = parsed_data[key]
                if isinstance(content, list):
                    content = '\n'.join(content)
                
                if content.strip():
                    formatted_sections.append({
                        'title': title,
                        'content': content
                    })
        
        return formatted_sections