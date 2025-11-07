"""
Test service to demonstrate ATOMIC_REQUESTS transaction rollback.

This service intentionally creates a scenario where:
1. Method 1 creates and saves FAQ #1
2. Method 2 creates and saves FAQ #2
3. Method 3 creates and saves FAQ #3 with duplicate order (fails)

Without explicit @transaction.atomic decorator, ATOMIC_REQUESTS should
roll back ALL database changes when the IntegrityError is raised.
"""

import logging

from apps.appInfo.models.faq import FAQ

logger = logging.getLogger(__name__)


class FAQTestService:
    """Service to test ATOMIC_REQUESTS rollback behavior with nested methods."""

    @staticmethod
    def create_faq_step_1():
        """Step 1: Create first FAQ and save to database."""
        faq1 = FAQ.objects.create(
            question="Test Question 1",
            answer="Test Answer 1",
            order=9001,  # Unique order
        )
        logger.debug("Step 1: Created FAQ #%s with order=%s", faq1.id, faq1.order)

        # Call nested method 2
        FAQTestService.create_faq_step_2()

        return faq1

    @staticmethod
    def create_faq_step_2():
        """Step 2: Create second FAQ and save to database."""
        faq2 = FAQ.objects.create(
            question="Test Question 2",
            answer="Test Answer 2",
            order=9002,  # Unique order
        )
        logger.debug("Step 2: Created FAQ #%s with order=%s", faq2.id, faq2.order)

        # Call nested method 3
        FAQTestService.create_faq_step_3()

        return faq2

    @staticmethod
    def create_faq_step_3():
        """Step 3: Create third FAQ with DUPLICATE order (will fail)."""
        # This will raise IntegrityError because order=9001 already exists from step 1
        faq3 = FAQ.objects.create(
            question="Test Question 3",
            answer="Test Answer 3",
            order=9001,  # DUPLICATE - will trigger IntegrityError
        )
        logger.debug("Step 3: Created FAQ #%s with order=%s", faq3.id, faq3.order)

        return faq3
