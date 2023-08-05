from abc import ABC, abstractmethod

class IResourceLock(ABC):
    def __init__(self):
        self._resources = {}

    @abstractmethod
    def reserve_resource(self, resource_id, requesting_entity):
        pass

    @abstractmethod
    def check_and_reserve(self, resource_id, requesting_entity) -> bool:
        pass

    @abstractmethod
    def check_and_unreserve(self, resource_id, requesting_entity) -> bool:
        pass

    @abstractmethod
    def unreserve_resource(self, resource_id):
        pass

    @abstractmethod
    def check_for_lock(self, resource_id):
        pass

    @abstractmethod
    def check_if_reserved(self, resource_id: object, requesting_entity: object) -> bool:
        pass

    @abstractmethod
    def get_active_reservations(self):
        pass