#用来定义记账一条记录长什么样。使用Pydantic做数据校验+类型注解，保证输入的数据格式合法
#每条账单包含：id，金额amount、分类category、备注note、创建时间created_at、更新时间updated_at、是否删除is_deleted
from pydantic import BaseModel
from datetime import datetime
from pydantic import field_validator

class Transaction(BaseModel):
    id: int | None
    amount: float
    category: str
    note: str
    created_at: datetime
    updated_at: datetime

@field_validator("amount")
def amount_must_positive(cls, v: float):
    if v < 0:
        raise ValueError("金额不能为负数")
    return v