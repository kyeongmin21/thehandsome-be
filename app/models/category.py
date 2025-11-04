from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    level = Column(Integer, nullable=False, default=0)  # level 추가
    parent = relationship("Category", remote_side=[id], backref="children")


    # Category 모델 자신과 관계를 맺겠다는 의미
    # 즉, 한 카테고리(Category)가 또 다른 카테고리(Category)를 부모로 가질 수 있음

    #  remote_side=[id]
    # 자기 자신과의 관계에서 “참조되는 컬럼”을 명시, 여기서 id가 부모 테이블의 컬럼이라는 걸 알려줌

    # backref="children": 부모에서 자식 리스트를 자동으로 만들어주는 속성
