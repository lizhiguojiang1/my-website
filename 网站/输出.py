import sqlite3

def query_messages():
    """
    查询 SQLite 数据库中的所有话术
    """
    conn = sqlite3.connect("fraud_messages.db")  # 连接数据库
    cursor = conn.cursor()

    # 执行查询操作
    cursor.execute("SELECT * FROM messages")
    results = cursor.fetchall()

    # 打印查询结果
    for row in results:
        print(row)

    # 关闭连接
    conn.close()

# 调用查询函数
query_messages()