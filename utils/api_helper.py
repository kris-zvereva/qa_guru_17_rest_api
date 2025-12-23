import requests
import allure
import logging
import json


logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s | %(asctime)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def log_request(method: str, url: str, **kwargs):
    request_data = {
        "method": method,
        "url": url,
        "headers": kwargs.get('headers', {}),
    }
    if 'json' in kwargs:
        request_data["body"] = kwargs['json']


    allure.attach(
        body=json.dumps(request_data, indent=2, ensure_ascii=False),
        name="Request",
        attachment_type=allure.attachment_type.JSON
    )

    logger.info(f"{method} | {url}")


def log_response(response: requests.Response):
    try:
        response_body = response.json()
    except:
        response_body = response.text

    response_data = {
        "status_code": response.status_code,
        "headers": dict(response.headers),
        "body": response_body,
        "elapsed_time": f"{response.elapsed.total_seconds():.2f}s"
    }

    allure.attach(
        body=json.dumps(response_data, indent=2, ensure_ascii=False),
        name=f"Response [{response.status_code}]",
        attachment_type=allure.attachment_type.JSON
    )

    logger.info(
        f"Status: {response.status_code} | "
        f"Time: {response.elapsed.total_seconds():.2f}s | "
        f"URL: {response.url}"
    )


def api_request(method: str, url: str, **kwargs) -> requests.Response:
    """
    Универсальная функция для API запросов с автоматическим логированием

    Args:
        method: HTTP метод (GET, POST, PUT, DELETE)
        url: URL запроса
        **kwargs: Дополнительные параметры для requests

    Returns:
        Response объект
    """
    log_request(method, url, **kwargs)
    response = requests.request(method, url, **kwargs)
    log_response(response)

    return response