import uuid

import allure
import grpc

from contracts.services.operations.operations_service_pb2_grpc import OperationsServiceStub

from contracts.services.operations.rpc_get_operations_pb2 import (
    GetOperationsRequest,
    GetOperationsResponse
)

from contracts.services.operations.rpc_get_operation_pb2 import (
    GetOperationRequest,
    GetOperationResponse
)

from tests.clients.grpc.client import GRPCTestClient, build_grpc_test_channel
from tests.config import test_settings
from tests.tools.logger import get_test_logger


class OperationsGRPCTestClient(GRPCTestClient):
    """
    gRPC API-клиент тестового слоя для gateway-service.

    Это специализированный клиент, построенный поверх базового
    GRPCTestClient. Он знает gRPC-контракт operations-service и
    protobuf-сообщения, но остаётся тестовым инструментом,
    а не частью бизнес-логики системы.

    Ключевой смысл этого клиента в курсе:
    тест обращается к gateway-service, а gateway-service "под капотом"
    обращается к внешним интеграциям (users / cards / accounts),
    которые в изоляционном контуре подменены мок-сервисами.

    Поэтому входные идентификаторы (user_id / account_id)
    не являются управляющим параметром поведения.
    Управляющая переменная — это сценарий, передаваемый
    через RequestContext и gRPC metadata.
    """

    def __init__(self, channel: grpc.Channel):
        # Базовый gRPC-клиент хранит channel как инфраструктурную зависимость.
        super().__init__(channel)

        # Stub создаётся поверх channel и является прямым отражением
        # protobuf-контракта operations-service.
        #
        # Важно: stub не знает о сценариях, тестах или моках.
        # Он просто реализует gRPC-интерфейс сервиса.
        self.stub = OperationsServiceStub(channel)

    @allure.step("Get operation")
    def get_operation_api(
        self,
        request: GetOperationRequest
    ) -> GetOperationResponse:
        # Низкоуровневый API-метод.
        #
        # Он напрямую вызывает gRPC-метод stub'а и возвращает
        # protobuf-ответ без дополнительной интерпретации.
        #
        # Здесь явно передаётся metadata, сформированная из RequestContext.
        # Это ключевая архитектурная точка:
        # - транспорт (channel) остаётся чистым;
        # - сценарий применяется только там, где он нужен по смыслу.
        return self.stub.GetOperation(
            request,
        )

    @allure.step("Get operations")
    def get_operations_api(
        self,
        request: GetOperationsRequest
    ) -> GetOperationsResponse:
        return self.stub.GetOperations(
            request
        )

    def get_operation(self, operation_id: uuid.UUID) -> GetOperationResponse:
        # Фасадный метод для тестов.
        request = GetOperationRequest(id=str(operation_id))
        return self.get_operation_api(request)

    def get_operations(
            self,
            user_id: uuid.UUID,
            card_id: uuid.UUID | None = None,
            account_id: uuid.UUID | None = None,
    ) -> GetOperationsResponse:
        request = GetOperationsRequest(user_id=str(user_id), card_id=card_id, account_id=account_id)
        return self.get_operations_api(request)


def build_operations_grpc_test_client() -> OperationsGRPCTestClient:
    # Фабрика создания специализированного gRPC-клиента operations-service.
    #
    # Здесь соблюдается тот же архитектурный паттерн,
    # что и в HTTP-части курса:
    # - конфигурация берётся из test_settings;
    # - логгер создаётся единым способом;
    # - channel настраивается централизованно.
    channel = build_grpc_test_channel(
        logger=get_test_logger("OPERATIONS_GRPC_TEST_CLIENT"),
        config=test_settings.operations_grpc_client,
    )
    return OperationsGRPCTestClient(channel=channel)
