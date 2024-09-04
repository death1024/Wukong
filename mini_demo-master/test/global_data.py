import sqlite3
flag=0
def read_specific_data(label):
    conn = sqlite3.connect('app_data.db')
    cursor = conn.cursor()
    # 查询
    cursor.execute("SELECT value FROM sensor_data WHERE label = ?", (label,))
    value = cursor.fetchone()
    if value:
        print(f"Value for {label}: {value[0]}")
    else:
        print(f"No data found for {label}.")
    # 关闭数据库连接
    conn.close()
    return value[0]

if __name__ == "__main__":
    read_specific_data('AttentionData')
