import json
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 模拟数据库操作
class DataProcessor:
    def __init__(self):
        # 模拟数据存储
        self.companies = []
        self.people = []
        self.news = []
        self.relationships = []
    
    def load_data(self, data_file):
        """加载爬虫抓取的数据"""
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for item in data:
            if 'industry' in item:
                # 公司数据
                self.companies.append(item)
            elif 'position' in item:
                # 人员数据
                self.people.append(item)
            elif 'source' in item:
                # 新闻数据
                self.news.append(item)
    
    def process_relationships(self):
        """处理人脉关系，计算亲密指数"""
        # 模拟计算亲密指数
        for i, person1 in enumerate(self.people):
            for j, person2 in enumerate(self.people):
                if i < j:
                    # 计算亲密指数（模拟）
                    intimacy_score = 50 + (i * j) % 50
                    common_connections = (i + j) % 10
                    interaction_frequency = (i + j) % 15
                    
                    self.relationships.append({
                        "person1Id": person1['id'],
                        "person2Id": person2['id'],
                        "intimacyScore": intimacy_score,
                        "commonConnections": common_connections,
                        "interactionFrequency": interaction_frequency
                    })
    
    def generate_organization(self):
        """生成组织架构数据"""
        organization = {}
        
        for company in self.companies:
            company_id = company['id']
            organization[company_id] = {
                "id": company_id,
                "name": company['name'],
                "children": []
            }
            
            # 按公司分组人员
            company_people = [p for p in self.people if p['companyId'] == company_id]
            
            # 构建组织架构树
            root_nodes = [p for p in company_people if not p['parentId']]
            
            for root in root_nodes:
                root_node = {
                    "id": root['id'],
                    "name": root['name'],
                    "position": root['position'],
                    "phone": root['phone'],
                    "email": root['email'],
                    "news": [n for n in self.news if n['personId'] == root['id']],
                    "children": self._build_children(root['id'], company_people)
                }
                organization[company_id]['children'].append(root_node)
        
        return organization
    
    def _build_children(self, parent_id, all_people):
        """递归构建子节点"""
        children = []
        
        for person in all_people:
            if person['parentId'] == parent_id:
                child_node = {
                    "id": person['id'],
                    "name": person['name'],
                    "position": person['position'],
                    "phone": person['phone'],
                    "email": person['email'],
                    "news": [n for n in self.news if n['personId'] == person['id']],
                    "children": self._build_children(person['id'], all_people)
                }
                children.append(child_node)
        
        return children
    
    def save_to_flask(self):
        """将数据保存到Flask应用中"""
        # 生成组织架构数据
        organization = self.generate_organization()
        
        # 模拟更新Flask应用的数据
        # 实际项目中，这里会将数据存储到数据库中
        print("数据处理完成，已更新Flask应用数据")
        print(f"公司数量: {len(self.companies)}")
        print(f"人员数量: {len(self.people)}")
        print(f"新闻数量: {len(self.news)}")
        print(f"关系数量: {len(self.relationships)}")
        
        return {
            "companies": self.companies,
            "organization": organization,
            "relationships": self.relationships
        }

if __name__ == "__main__":
    # 示例用法
    processor = DataProcessor()
    # 假设爬虫数据已保存到data.json文件
    # processor.load_data('data.json')
    # processor.process_relationships()
    # processor.save_to_flask()
