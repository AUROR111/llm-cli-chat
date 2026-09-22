import typer
from src.bookkeeping.models import Transaction
from src.bookkeeping.decorators import timer, retry
from src.bookkeeping.storage import init_db, add_transaction, get_all_transactions, delete_transaction, get_month_total
from datetime import datetime

app = typer.Typer()
init_db()
#创建Typer应用实例，用于注册命令

@app.command()
def add(amount: float, category: str, note: str):
    # 添加一条记账记录
    record = Transaction(
        id=None,
        amount=amount,
        category=category,
        note=note,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    new_id = add_transaction(record)
    #将记录存入内存列表
    typer.echo(f"添加成功: {record}")

@app.command()
@timer
def totalsum():
    # 计算总金额
    records = get_all_transactions()
    total = sum(record.amount for record in records)
    typer.echo(f"总金额: {total}")
@app.command() 
def delete(tid:int):
    # 删除一条记账记录
    delete_transaction(tid)
    typer.echo(f"删除成功: 记录ID {tid}")
@app.command()
def month(year_month: str):
    # 计算指定月份的总金额
    total = get_month_total(year_month)
    typer.echo(f"{year_month} 总金额: {total}")


@app.command()
def list():
    # 列出所有记账记录
    records = get_all_transactions()
    for record in records:
        typer.echo(record.model_dump())

if __name__ == "__main__":
    app()
    