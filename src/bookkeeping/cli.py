import typer
from src.bookkeeping.models import Transaction
from src.bookkeeping.decorators import timer
from src.bookkeeping.storage import (
    init_db, add_transaction, get_all_transactions, 
    delete_transaction, get_month_total, update_transaction,
    get_filter_transactions)

from datetime import datetime

app = typer.Typer()
#创建Typer应用实例，用于注册命令

@app.command()
def add(
    category: str = typer.Argument(..., help="记账类别"),
    note: str = typer.Argument(..., help="备注信息")
):
    #添加金额非负数处理
    while True:
        raw_input = typer.prompt("请输入金额")
        try:
            amount = float(raw_input)
        except ValueError:
            typer.echo("输入无效，请输入一个数字。")
            continue

        if amount <= 0:
            typer.echo("金额必须大于0，请重新输入。")
            continue
        break
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
    typer.echo(f"添加成功: {new_id}")
    typer.echo(record)

@app.command()
@timer
def totalsum():
    # 计算总金额
    records = get_all_transactions()
    total = sum(record.amount for record in records)
    typer.echo(f"总金额: {total:.2f}")


@app.command()
def delete(tid: int):
    """根据ID删除记账记录，带确认弹窗"""
    confirm = typer.confirm(f"确认删除ID为{tid}的记录吗？", default=False)
    if not confirm:
        typer.echo("已取消删除")
        return
    try:
        delete_transaction(tid)
        typer.echo(f"删除成功: 记录ID {tid}")
    except ValueError as e:
        typer.echo(f"删除失败：{e}")


@app.command()
def month(year_month: str):
    # 计算指定月份的总金额
    try:
        total = get_month_total(year_month)
        typer.echo(f"{year_month} 总金额: {total:.2f}")
    except ValueError as e:
        typer.echo(f"查询失败: {e}")
    


@app.command(name="list")
def list_records(
    category: str | None = typer.Option(None, "--category", "-c", help="按分类筛选，例：餐饮"),
    page: int = typer.Option(1, "--page", "-p", min=1, help="页码，从1开始"),
    page_size: int = typer.Option(5, "--size", "-s", min=1, help="每页展示条数")
):
    """查看记账记录，支持分类筛选 + 分页"""
    records = get_filter_transactions(category=category)
    if not records:
        typer.echo("没有记账记录。")
        return

    start = (page - 1) * page_size
    end = start + page_size
    page_data = records[start:end]

    typer.echo(f"\n第 {page} 页，每页 {page_size} 条，共 {len(records)} 条记录")
    for record in page_data:
        typer.echo(record.model_dump())

@app.command()
def updated_at(
    tid: int = typer.Argument(..., help='要修改的ID'),
    amount: float | None = typer.Option(None, "--mount", "-a", help="金额"),
    category: str | None = typer.Option(None, "--category", "-c", help="新分类"),
    note: str | None = typer.Option(None, "--note", "-n", help="新备注")  
):
    if amount is not None and amount <= 0:
        typer.echo("金额必须大于0！")
        raise typer.Exit(code=1)
    try:
        updated_record = update_transaction(
            tid=tid,
            new_amount=amount,
            new_category=category,
            new_note=note
        )
        typer.echo("更新成功！")
        typer.echo(updated_record.model_dump())
    except ValueError as e:
        typer.echo(f"更新失败: {e}")

if __name__ == "__main__":
    init_db()  # 初始化数据库
    app()
    