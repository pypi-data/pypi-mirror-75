from flask import request


class AppEngineHeader:
    @property
    def user_ip(self):
        return request.headers.get("X-Appengine-User-Ip")

    @property
    def cloudscheduler(self):
        return request.headers.get("X-Cloudscheduler")

    @property
    def tasks_queue_name(self):
        return request.headers.get("X-Appengine-Queuename")

    @property
    def tasks_execution_count(self):
        return int(request.headers.get("X-AppEngine-TaskExecutionCount", -1))

    def _is_internal_ip(self):
        return self.user_ip in ("0.1.0.1", "0.1.0.2",)

    def is_cloudscheduler_request(self, ip_check=True):
        if ip_check and not self._is_internal_ip():
            return False
        value = self.cloudscheduler
        if not isinstance(value, str):
            return False
        return str.lower() == "true"

    def is_tasks_request(self, ip_check=True):
        if ip_check and not self._is_internal_ip():
            return False
        return self.tasks_queue_name is not None


GaeHeader = AppEngineHeader()
