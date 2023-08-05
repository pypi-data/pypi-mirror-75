import logging
from cooplock.IResourceLock import IResourceLock

class ResourceLock(IResourceLock):
    def __init__(self):
        super().__init__()

    def reserve_resource(self, resource_id, requesting_entity):
        if self._resources.get(resource_id, None) is None or self._resources.get(resource_id, None) == requesting_entity:
            self._resources[resource_id] = requesting_entity
        else:
            raise Exception(f"resource {resource_id} is already reserved by {self._resources[resource_id]}. Must un-reserve prior to reserving")

    def check_and_reserve(self, resource_id, requesting_entity) -> bool:
        resource_check = self.check_for_lock(resource_id)
        logging.debug(f"Reserve with Lock Check for resource: {resource_id} by {requesting_entity} -> Result:{resource_check}")
        if resource_check is None or resource_check == requesting_entity:
            self.reserve_resource(resource_id, requesting_entity)
            return True
        else:
            return False

    def check_and_unreserve(self, resource_id, requesting_entity) -> bool:
        resource_check = self.check_for_lock(resource_id)
        logging.debug(f"Un-reserve with Lock Check for resource: {resource_id} by {requesting_entity} -> Result:{resource_check}")
        if resource_check == requesting_entity:
            self.unreserve_resource(resource_id)
            return True
        else:
            return False

    def unreserve_resource(self, resource_id):
        if self._resources.get(resource_id, None) is not None:
            self._resources[resource_id] = None

    def check_for_lock(self, resource_id):
        return self._resources.get(resource_id, None)

    def check_if_reserved(self, resource_id: object, requesting_entity: object) -> bool:
        locked = self.check_for_lock(resource_id)
        if locked == requesting_entity:
            return True
        else:
            return False

    def get_active_reservations(self):
        return {key: value for key, value in self._resources.items() if value}
    
if __name__ == "__main__":
    locker = ResourceLock()
    
    res = "1"
    req = "2"
    
    locker.reserve_resource(res, req)