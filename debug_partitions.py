import asyncio
import os

# ==========================================
# 必须在导入 client 之前设置环境变量！
# ==========================================
os.environ["WCL_CLIENT_ID"] = "a0e16bba-fba8-432d-a317-4a6a83d98728"
os.environ["WCL_CLIENT_SECRET"] = "Rowpl4stVguifS4YJbzow1HCjh1g2uNuGNaFYRPk"

from lorgs.clients.wcl.client import WarcraftlogsClient

async def get_partitions():
    client = WarcraftlogsClient.get_instance()
    
    # 查询 Zone 73 (Arcadion) 的所有分区信息
    query = """
    worldData {
        zone(id: 73) {
            name
            partitions {
                name
                id
                compactName
                default
            }
        }
    }
    """
    
    print("正在查询 Zone 73 的分区信息...")
    try:
        result = await client.query(query)
        
        zone_data = result.get("worldData", {}).get("zone", {})
        print(f"\n区域名称: {zone_data.get('name')}")
        print("-" * 40)
        print(f"{'ID':<5} | {'Name':<30} | {'Default':<10}")
        print("-" * 40)
        
        partitions = zone_data.get("partitions", [])
        if not partitions:
            print("警告: 没有找到任何分区信息！")
            
        for p in partitions:
            print(f"{p['id']:<5} | {p['name']:<30} | {p['default']}")
            
    except Exception as e:
        print(f"查询失败: {e}")

if __name__ == "__main__":
    asyncio.run(get_partitions())