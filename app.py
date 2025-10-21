
# -*- coding: utf-8 -*-
"""
=========================================================
项目名称:  物品复活 Revive
文件名称:  app.py
作者:      帅哲（Avid）
版本号:    v1.1
创建日期:  2025-10-01
最后修改:  2025-10-19
=========================================================
文件目的:
    命令行入口程序，支持以下功能：
        1. 添加物品信息
        2. 删除物品信息
        3. 显示物品列表
        4. 查找物品信息
        5. 导出物品列表到 CSV
    可与 GUI 界面 (gui.py) 联动使用。
=========================================================
"""

import argparse
from pathlib import Path
from db import ReviveDB

DEFAULT_DB_PATH = "revive.db"
DEFAULT_EXPORT_FILE = "items.csv"

def ensure_db(path: Path) -> ReviveDB:
    """初始化数据库连接。"""
    return ReviveDB(path)

def cmd_init_db(args):
    """初始化数据库。"""
    db = ensure_db(Path(args.db))
    db.close()
    print(f"✅ 数据库已初始化：{args.db}")

def cmd_add(args):
    """添加物品信息。"""
    db = ensure_db(Path(args.db))
    if not args.name or not args.contact:
        print("⚠️ 名称与联系方式为必填项。")
        return
    item_id = db.add_item(args.name, args.desc or '', args.contact, float(args.price))
    print(f"✅ 已添加物品：ID={item_id}，名称={args.name}")
    db.close()

def cmd_list(args):
    """显示物品列表。"""
    db = ensure_db(Path(args.db))
    rows = db.list_items(limit=args.limit, order_by=args.order, asc=args.asc)
    if not rows:
        print("（空）暂无物品，使用 add 添加吧！")
    else:
        print(f"共 {len(rows)} 条记录：\n" + "-" * 60)
        for r in rows:
            price_str = '赠送' if float(r['price']) == 0 else f"¥{r['price']:.2f}"
            print(f"[{r['id']}] {r['name']} | {price_str} | {r['contact']}\n"
                  f"    描述: {r['description'] or '（无）'}\n"
                  f"    时间: {r['created_at']}\n")
    db.close()

def cmd_find(args):
    """按关键词查找物品。"""
    db = ensure_db(Path(args.db))
    rows = db.search_items(args.q, limit=args.limit)
    if not rows:
        print("未找到匹配项。")
    else:
        print(f"匹配 {len(rows)} 条记录：\n" + "-" * 60)
        for r in rows:
            price_str = '赠送' if float(r['price']) == 0 else f"¥{r['price']:.2f}"
            print(f"[{r['id']}] {r['name']} | {price_str} | {r['contact']}\n"
                  f"    {r['description'] or '（无描述）'}\n"
                  f"    创建时间: {r['created_at']}\n")
    db.close()

def cmd_delete(args):
    """删除指定 ID 的物品。"""
    db = ensure_db(Path(args.db))
    count = db.delete_item(args.id)
    if count:
        print(f"🗑️ 已删除 ID={args.id}")
    else:
        print(f"⚠️ 未找到 ID={args.id}")
    db.close()

def cmd_export(args):
    """导出 CSV。"""
    db = ensure_db(Path(args.db))
    out = Path(args.out or DEFAULT_EXPORT_FILE)
    n = db.export_csv(out)
    print(f"✅ 已导出 {n} 条记录到 {out}")
    db.close()

def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器。"""
    parser = argparse.ArgumentParser(description="物品复活 Revive — 闲置物品管理命令行工具")
    parser.add_argument("--db", default=DEFAULT_DB_PATH, help="数据库文件路径（默认 revive.db）")
    parser.add_argument("--init-db", action="store_true", help="初始化数据库（幂等）")

    sub = parser.add_subparsers(dest="command")

    p_add = sub.add_parser("add", help="添加物品")
    p_add.add_argument("--name", required=True, help="物品名称（必填）")
    p_add.add_argument("--desc", default="", help="物品描述")
    p_add.add_argument("--contact", required=True, help="联系方式（必填）")
    p_add.add_argument("--price", default=0, help="价格（0 表示赠送）")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="显示物品列表")
    p_list.add_argument("--limit", type=int, default=50, help="显示条数")
    p_list.add_argument("--order", choices=["created_at", "price", "id", "name"], default="created_at")
    p_list.add_argument("--asc", action="store_true", help="升序显示")
    p_list.set_defaults(func=cmd_list)

    p_find = sub.add_parser("find", help="查找物品")
    p_find.add_argument("--q", required=True, help="关键词")
    p_find.add_argument("--limit", type=int, default=50)
    p_find.set_defaults(func=cmd_find)

    p_del = sub.add_parser("delete", help="删除物品")
    p_del.add_argument("--id", type=int, required=True, help="物品 ID")
    p_del.set_defaults(func=cmd_delete)

    p_export = sub.add_parser("export", help="导出 CSV")
    p_export.add_argument("--out", default=DEFAULT_EXPORT_FILE)
    p_export.set_defaults(func=cmd_export)

    return parser

def main() -> None:
    """程序入口。"""
    parser = build_parser()
    args = parser.parse_args()
    if args.init_db:
        cmd_init_db(args)
    if getattr(args, "func", None):
        args.func(args)
    elif not args.init_db:
        parser.print_help()

if __name__ == "__main__":
    main()
