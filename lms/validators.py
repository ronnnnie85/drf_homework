import re

from rest_framework.serializers import ValidationError


class VideoURLValidator:
    pattern = re.compile(r"https?://([\w.-]+)/", re.IGNORECASE)
    allowed_hosts = ("youtube.com", "youtu.be", "m.youtube.com")

    message = "Разрешены только ссылки на YouTube (youtube.com или youtu.be)."

    def __call__(self, value):
        if not value:
            return

        url = str(value).strip().lower()

        match = self.pattern.match(url)
        if not match:
            raise ValidationError("Некорректная ссылка.")

        host = match.group(1)
        if host.startswith("www."):
            host = host[4:]

        if host not in self.allowed_hosts:
            raise ValidationError(self.message)
