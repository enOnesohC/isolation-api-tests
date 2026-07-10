import uuid
import allure
from httpx import Response, QueryParams
from tests.clients.http.client import HTTPTestClient, build_http_test_client
from tests.config import test_settings
from tests.schema.operations import (
    GetOperationsQueryTestSchema,
    GetOperationResponseTestSchema,
    GetOperationsResponseTestSchema
)
from tests.tools.logger import get_test_logger
from tests.tools.routes import APITestRoutes


class OperationsHTTPTestClient(HTTPTestClient):
    """
    HTTP API-клиент тестового слоя для Operations-service.

    Это специализированный клиент, построенный поверх HTTPTestClient.
    Он знает HTTP-контракт Operations-service (пути и ответы), но остаётся
    тестовым инструментом, а не частью бизнес-логики системы.

    Ключевой смысл этого клиента в курсе:
    тест обращается к gateway-service, а Operations-service "под капотом"
    обращается к внешним интеграциям (users/cards/accounts),
    которые в изоляционном контуре подменены мок-сервисами.

    Поэтому входные идентификаторы (user_id / account_id) в этих вызовах
    не являются управляющим параметром поведения — поведение определяется
    сценарным контекстом (RequestContext -> x-test-scenario).
    """

    @allure.step("Get operation")
    def get_operation_api(
        self,
        operation_id: uuid.UUID
    ) -> Response:
        return self.get(
            f"{APITestRoutes.OPERATIONS}/{operation_id}"
        )

    @allure.step("Get operations")
    def get_operations_api(
        self,
        query: GetOperationsQueryTestSchema
    ) -> Response:
        return self.get(APITestRoutes.OPERATIONS,
            params=QueryParams(**query.model_dump(by_alias=True, exclude_none=True)))


    def get_operation(self, operation_id) -> GetOperationResponseTestSchema:
        response = self.get_operations_api(operation_id)
        response.raise_for_status()

        return GetOperationResponseTestSchema.model_validate_json(response.text)


    def get_operations(self, user_id: str, card_id: str, account_id:str) -> GetOperationsResponseTestSchema:
        request = GetOperationsQueryTestSchema(
            user_id=user_id,
            card_id=card_id,
            account_id=account_id
        )
        response = self.get_operations_api(request)
        response.raise_for_status()

        return GetOperationsResponseTestSchema.model_validate_json(response.text)


def build_operations_http_test_client() -> OperationsHTTPTestClient:
    client = build_http_test_client(
        logger=get_test_logger("OPERATIONS_HTTP_TEST_CLIENT"),
        config=test_settings.operations_http_client,
    )
    return OperationsHTTPTestClient(client=client)
