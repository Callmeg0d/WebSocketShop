from sqlalchemy import insert, select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.reviews.models import Reviews
from app.users.models import Users


class ReviewsDAO(BaseDAO):
    model = Reviews

    @classmethod
    async def add_review(cls, user_id: int, product_id: int, rating: int, feedback: str):
        async with async_session_maker() as session:
            await session.execute(
                insert(Reviews).values(
                    user_id=user_id,
                    product_id=product_id,
                    rating=rating,
                    feedback=feedback,
                )
            )
            await session.commit()

    @classmethod
    async def get_reviews_by_product_id(cls, product_id: int):
        async with async_session_maker() as session:
            result = await session.execute(
                select(Reviews, Users.email)
                .join(Users, Reviews.user_id == Users.id)
                .where(Reviews.product_id == product_id)
            )
            reviews = []
            for row in result.fetchall():
                if row:
                    review, user_email = row
                    if review:
                        reviews.append({
                            "user_email": user_email if user_email else "Анонимный пользователь",
                            "rating": review.rating,
                            "feedback": review.feedback
                        })

            return reviews
