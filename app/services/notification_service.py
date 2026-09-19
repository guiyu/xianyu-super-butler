"""
Notification testing service for validating notification channels.
"""

from typing import Optional, Dict, Any
from loguru import logger
import time


class NotificationTestError(Exception):
    """Exception raised when notification testing fails."""

    def __init__(self, message: str, retry_after: Optional[int] = None):
        super().__init__(message)
        self.message = message
        self.retry_after = retry_after


class RateLimiter:
    """Simple rate limiter for notification tests."""

    def __init__(self, requests: int = 5, period: int = 60):
        self.requests = requests
        self.period = period
        self.calls = []

    def is_allowed(self, key: str = "default") -> bool:
        """Check if a request is allowed."""
        now = time.time()
        # Remove old calls outside the period
        self.calls = [call for call in self.calls if now - call[1] < self.period]

        # Count calls for this key
        key_calls = [call for call in self.calls if call[0] == key]

        if len(key_calls) < self.requests:
            self.calls.append((key, now))
            return True

        return False

    def get_retry_after(self, key: str = "default") -> Optional[int]:
        """Get retry-after time in seconds."""
        now = time.time()
        key_calls = [call for call in self.calls if call[0] == key]

        if key_calls:
            oldest_call = min(call[1] for call in key_calls)
            retry_after = int(oldest_call + self.period - now) + 1
            return max(1, retry_after)

        return None


notification_test_rate_limiter = RateLimiter(requests=5, period=60)


class NotificationTestService:
    """Service for testing notification channels."""

    def __init__(self, db_manager, sender=None, limiter=None):
        self.db_manager = db_manager
        self.sender = sender
        self.limiter = limiter or notification_test_rate_limiter

    async def test_notification(
        self,
        channel_type: str,
        config: Dict[str, Any],
        user_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Test a notification channel configuration.

        Args:
            channel_type: Type of notification channel
            config: Channel configuration
            user_id: Optional user ID for rate limiting

        Returns:
            Dict with test results

        Raises:
            NotificationTestError: If test fails
        """
        try:
            # Check rate limit
            if not self.limiter.is_allowed(user_id or "default"):
                retry_after = self.limiter.get_retry_after(user_id or "default")
                raise NotificationTestError(
                    "Too many test requests. Please try again later.",
                    retry_after=retry_after,
                )

            # Validate channel type
            if not channel_type:
                raise NotificationTestError("Channel type is required")

            logger.info(f"Testing notification channel: {channel_type}")

            # If sender is available, use it to test
            if self.sender:
                try:
                    await self.sender.test_channel(channel_type, config)
                except Exception as e:
                    raise NotificationTestError(f"Channel test failed: {str(e)}")

            logger.info(f"Notification test passed for {channel_type}")

            return {
                "success": True,
                "message": "Notification test passed",
                "channel_type": channel_type,
            }

        except NotificationTestError:
            raise
        except Exception as e:
            logger.error(f"Notification test error: {str(e)}")
            raise NotificationTestError(f"Unexpected error: {str(e)}")
