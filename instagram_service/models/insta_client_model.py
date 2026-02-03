from django.db import models
import logging

logger = logging.getLogger(__name__)


class InstaClient(models.Model):
    client_id = models.BigIntegerField(unique=True)
    full_name = models.TextField(null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    profile_picture = models.URLField(null=True, blank=True, verbose_name="Profil rasmi URL")
    last_activity = models.DateTimeField(auto_now=True, verbose_name="Oxirgi faollik")
    follower_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan sana")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi?")

    class Meta:
        verbose_name = "Instagram Foydalanuvchisi"
        verbose_name_plural = "Instagram Foydalanuvchilari"
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["is_active"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name}({self.username})"

    @classmethod
    async def create_from_webhook(cls,
                                    user_info: dict,
                                  ):
        user_id: str = user_info.get("id")
        username: str = user_info.get("username")
        name: str = user_info.get("name")
        profile_picture: str = user_info.get("profile_pic")
        follower_count: str = user_info.get("follower_count")
        try:

            # Check if client exists
            client = await cls.objects.filter(client_id=user_id).afirst()

            if client:
                logger.info(f"Client already exists: {username}")
                return client, False
            else:
                # Create new client
                client = await cls.objects.acreate(
                    client_id=user_id,
                    full_name=name,
                    username=username,
                    profile_picture=profile_picture,
                    follower_count=follower_count,

                )
                logger.info(f"Created new client: {username}")
                return client, True

        except Exception as e:
            logger.error(f"Error creating client from webhook: {str(e)}")
