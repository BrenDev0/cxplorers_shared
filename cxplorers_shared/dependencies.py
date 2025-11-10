from cxplorers_shared.domain.services.encryption_service_base import EncryptionServiceBase
from cxplorers_shared.infrastructure.services.encryption_service import EncryptionService

def get_ecrytpion_service() -> EncryptionServiceBase:
    return EncryptionService()