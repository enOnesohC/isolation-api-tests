from contracts.services.operations.operation_pb2 import OperationType, OperationStatus
from tests.schema.operations import OperationTestType, OperationTestStatus

# ---------- Маппинг для событий (enum -> proto) ----------
OPERATION_TYPE_FROM_EVENT = {
    OperationTestType.TOP_UP: OperationType.OPERATION_TYPE_TOP_UP,
    OperationTestType.PURCHASE: OperationType.OPERATION_TYPE_PURCHASE,
    OperationTestType.CASHBACK: OperationType.OPERATION_TYPE_CASHBACK,
    OperationTestType.TRANSFER: OperationType.OPERATION_TYPE_TRANSFER,
    OperationTestType.REVERSAL: OperationType.OPERATION_TYPE_REVERSAL,
    OperationTestType.BILL_PAYMENT: OperationType.OPERATION_TYPE_BILL_PAYMENT,
    OperationTestType.CASH_WITHDRAWAL: OperationType.OPERATION_TYPE_CASH_WITHDRAWAL,
    OperationTestType.FEE: OperationType.OPERATION_TYPE_FEE,
}

OPERATION_STATUS_FROM_EVENT = {
    OperationTestStatus.IN_PROGRESS: OperationStatus.OPERATION_STATUS_IN_PROGRESS,
    OperationTestStatus.COMPLETED: OperationStatus.OPERATION_STATUS_COMPLETED,
    OperationTestStatus.REVERSED: OperationStatus.OPERATION_STATUS_REVERSED,
    OperationTestStatus.FAILED: OperationStatus.OPERATION_STATUS_FAILED,
}

