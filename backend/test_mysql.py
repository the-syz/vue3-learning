import os
import pymysql
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取数据库配置参数
DB_USERNAME = os.getenv('DB_USERNAME', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', '3306'))
DB_NAME = os.getenv('DB_NAME', 'vue3_project')

print(f"尝试连接到MySQL数据库：")
print(f"主机: {DB_HOST}")
print(f"端口: {DB_PORT}")
print(f"用户名: {DB_USERNAME}")
print(f"密码: {'*' * len(DB_PASSWORD) if DB_PASSWORD else '空'}")
print(f"数据库名: {DB_NAME}")

# 尝试建立连接
try:
    conn = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        db=DB_NAME,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("\n数据库连接成功!")
    
    # 测试查询
    try:
        with conn.cursor() as cursor:
            # 查询用户表
            sql = "SELECT * FROM accounts LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
            if result:
                print("\n查询用户表成功，示例数据:")
                print(f"用户名: {result['username']}")
                print(f"账户类型: {result['account_type']}")
            else:
                print("\n用户表中没有数据")
    except Exception as e:
        print(f"\n查询时出错: {e}")
    
except Exception as e:
    print(f"\n数据库连接失败: {e}")
finally:
    if 'conn' in locals() and conn:
        conn.close()
        print("\n数据库连接已关闭")