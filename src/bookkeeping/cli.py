import typer
from src.bookkeeping.models import Transaction
from src.bookkeeping.decorators import timer, retry
from datetime import datetime

app = typer.Typer()
#创建Typer应用实例，用于注册命令
transaction: list[Transaction] = []    
# 用于存储记账记录的列表
@app.command()
def add(amount: float, category: str, note: str):
    # 添加一条记账记录
    record = Transaction(
        id=len(transaction) + 1,
        amount=amount,
        category=category,
        note=note,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    transaction.append(record)
    #将记录存入内存列表
    typer.echo(f"添加成功: {record}")

@app.command()
@timer
def totalsum():
    # 计算总金额
    total = sum(item.amount for item in transaction)
    typer.echo(f"总金额: {total}")


@app.command()
def list_records():
    # 列出所有记账记录
    for item in transaction:
        typer.echo(f"ID: {item.id}, 金额: {item.amount}, 分类: {item.category}, 备注: {item.note}, 创建时间: {item.created_at}, 更新时间: {item.updated_at}")

if __name__ == "__main__":
    app()
    transaction.append(Transaction(id=1, amount=100.0, category="Food", note="Lunch", created_at=datetime.now(), updated_at=datetime.now()))