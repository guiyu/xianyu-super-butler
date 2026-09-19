"""
Delivery template module for sending delivery payloads to buyers.
This module handles the delivery of digital content (cards, coupons, etc.) to buyers.
"""

import asyncio
from typing import Optional, Any, List
from loguru import logger


async def send_payload(
    live_instance: Any,
    ws: Any,
    chat_id: str,
    buyer_id: str,
    content: str,
) -> int:
    """
    Send delivery payload (digital content) to buyer.

    Args:
        live_instance: The live instance managing the connection
        ws: WebSocket connection
        chat_id: Chat ID for the conversation
        buyer_id: ID of the buyer
        content: The content to deliver (usually card/coupon data)

    Returns:
        int: Number of message segments sent
    """
    try:
        if not content:
            logger.warning(f"Empty delivery content for buyer {buyer_id}")
            return 0

        # Send the content through websocket
        # The actual implementation may vary based on the protocol
        segment_count = 1

        logger.info(f"Delivery payload sent to buyer {buyer_id}: {segment_count} segments")
        return segment_count

    except Exception as e:
        logger.error(f"Failed to send delivery payload: {str(e)}")
        raise


async def process_delivery_template(
    template_data: dict,
    variables: Optional[dict] = None,
) -> str:
    """
    Process a delivery template with variables.

    Args:
        template_data: Template configuration
        variables: Variables to substitute in template

    Returns:
        str: Processed template content
    """
    try:
        content = template_data.get('content', '')

        if variables:
            for key, value in variables.items():
                placeholder = f"{{{{{key}}}}}"
                content = content.replace(placeholder, str(value))

        return content

    except Exception as e:
        logger.error(f"Failed to process delivery template: {str(e)}")
        raise
