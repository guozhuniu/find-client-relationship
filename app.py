from flask import Flask, render_template, jsonify, request
import json
import os
import sys
import sqlite3

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# 导入数据分析模块
try:
    from analysis.intimacy_analyzer import IntimacyAnalyzer
    analyzer_available = True
except ImportError:
    print("Error: Could not import IntimacyAnalyzer. Please make sure the analysis module is properly installed.")
    analyzer_available = False
    IntimacyAnalyzer = None

app = Flask(__name__)

# 数据库连接
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 初始化数据库
def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # 创建公司表
    c.execute('''
        CREATE TABLE IF NOT EXISTS companies (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            industry TEXT NOT NULL,
            website TEXT,
            description TEXT,
            logo TEXT
        )
    ''')
    
    # 创建人员表
    c.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            position TEXT,
            phone TEXT,
            email TEXT,
            companyId TEXT,
            parentId TEXT,
            FOREIGN KEY (companyId) REFERENCES companies (id)
        )
    ''')
    
    # 创建新闻表
    c.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT,
            date TEXT,
            source TEXT,
            personId TEXT,
            FOREIGN KEY (personId) REFERENCES people (id)
        )
    ''')
    
    # 创建关系表
    c.execute('''
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person1Id TEXT,
            person2Id TEXT,
            intimacyScore INTEGER,
            commonConnections INTEGER,
            interactionFrequency INTEGER,
            FOREIGN KEY (person1Id) REFERENCES people (id),
            FOREIGN KEY (person2Id) REFERENCES people (id)
        )
    ''')
    
    # 插入示例数据
    c.execute('SELECT COUNT(*) FROM companies')
    if c.fetchone()[0] == 0:
        companies = [
            ("1", "宝洁公司", "日化", "https://www.pg.com", "全球最大的日用消费品公司之一", "https://example.com/pg_logo.png"),
            ("2", "联合利华", "日化", "https://www.unilever.com", "全球领先的日用消费品公司", "https://example.com/unilever_logo.png"),
            ("3", "欧莱雅", "美妆", "https://www.loreal.com", "全球最大的化妆品公司", "https://example.com/loreal_logo.png"),
            ("4", "苹果公司", "数码", "https://www.apple.com", "全球领先的科技公司", "https://example.com/apple_logo.png"),
            ("5", "可口可乐", "快消", "https://www.coca-cola.com", "全球最大的饮料公司", "https://example.com/coca_cola_logo.png")
        ]
        c.executemany('INSERT INTO companies VALUES (?, ?, ?, ?, ?, ?)', companies)
    
    c.execute('SELECT COUNT(*) FROM people')
    if c.fetchone()[0] == 0:
        people = [
            ("111", "David Taylor", "CEO", "123-456-7890", "david.taylor@pg.com", "1", ""),
            ("121", "John Smith", "市场总监", "123-456-7891", "john.smith@pg.com", "1", "111"),
            ("211", "Alan Jope", "CEO", "234-567-8901", "alan.jope@unilever.com", "2", "")
        ]
        c.executemany('INSERT INTO people VALUES (?, ?, ?, ?, ?, ?, ?)', people)
    
    c.execute('SELECT COUNT(*) FROM news')
    if c.fetchone()[0] == 0:
        news = [
            ("宝洁公司CEO David Taylor宣布退休", "https://www.reuters.com/business/consumer-products/pg-ceo-david-taylor-step-down-2023-05-15/", "2023-05-15", "Reuters", "111"),
            ("宝洁市场总监John Smith分享品牌策略", "https://www.marketingweek.com/pg-brand-strategy-john-smith/", "2023-06-20", "Marketing Week", "121"),
            ("联合利华CEO Alan Jope推动可持续发展战略", "https://www.bbc.com/news/business-65000000", "2023-07-10", "BBC News", "211")
        ]
        c.executemany('INSERT INTO news VALUES (NULL, ?, ?, ?, ?, ?)', news)
    
    c.execute('SELECT COUNT(*) FROM relationships')
    if c.fetchone()[0] == 0:
        relationships = [
            ("111", "121", 85, 5, 10),
            ("111", "211", 60, 3, 5)
        ]
        c.executemany('INSERT INTO relationships VALUES (NULL, ?, ?, ?, ?, ?)', relationships)
    
    conn.commit()
    conn.close()

# 初始化数据库
print("Initializing database...")
try:
    init_db()
    print("Database initialized successfully")
except Exception as e:
    print(f"Error initializing database: {e}")

# 加载数据
companies = []
people = []
relationships = []

try:
    print("Loading data...")
    conn = get_db_connection()
    c = conn.cursor()
    
    # 加载公司数据
    c.execute('SELECT * FROM companies')
    for row in c.fetchall():
        companies.append({
            "id": row['id'],
            "name": row['name'],
            "industry": row['industry'],
            "website": row['website'],
            "description": row['description'],
            "logo": row['logo']
        })
    
    # 加载人员数据
    c.execute('SELECT * FROM people')
    for row in c.fetchall():
        people.append({
            "id": row['id'],
            "name": row['name'],
            "position": row['position'],
            "phone": row['phone'],
            "email": row['email'],
            "companyId": row['companyId'],
            "parentId": row['parentId']
        })
    
    # 加载关系数据
    c.execute('SELECT * FROM relationships')
    for row in c.fetchall():
        relationships.append({
            "person1Id": row['person1Id'],
            "person2Id": row['person2Id'],
            "intimacyScore": row['intimacyScore'],
            "commonConnections": row['commonConnections'],
            "interactionFrequency": row['interactionFrequency']
        })
    
    conn.close()
    print(f"Data loaded successfully: {len(companies)} companies, {len(people)} people, {len(relationships)} relationships")
except Exception as e:
    print(f"Error loading data: {e}")
    if 'conn' in locals():
        conn.close()

# 生成组织架构数据
organization = {}
try:
    print("Generating organization data...")
    for company in companies:
        company_id = company['id']
        organization[company_id] = {
            "id": company_id,
            "name": company['name'],
            "children": []
        }
        
        # 按公司分组人员
        company_people = [p for p in people if p['companyId'] == company_id]
        
        # 构建组织架构树
        root_nodes = [p for p in company_people if not p['parentId']]
        
        for root in root_nodes:
            # 加载人员新闻
            conn = get_db_connection()
            c = conn.cursor()
            c.execute('SELECT * FROM news WHERE personId = ?', (root['id'],))
            news = []
            for news_row in c.fetchall():
                news.append({
                    "title": news_row['title'],
                    "url": news_row['url'],
                    "date": news_row['date'],
                    "source": news_row['source']
                })
            conn.close()
            
            root_node = {
                "id": root['id'],
                "name": root['name'],
                "position": root['position'],
                "phone": root['phone'],
                "email": root['email'],
                "news": news,
                "children": []
            }
            organization[company_id]['children'].append(root_node)
    print("Organization data generated successfully")
except Exception as e:
    print(f"Error generating organization data: {e}")

# 初始化数据分析器
analyzer = None
if analyzer_available:
    try:
        print("Initializing IntimacyAnalyzer...")
        analyzer = IntimacyAnalyzer()
        analyzer.build_network(people, relationships)
        print("IntimacyAnalyzer initialized successfully")
    except Exception as e:
        print(f"Error initializing IntimacyAnalyzer: {e}")
        analyzer = None

@app.route('/')
def index():
    return render_template('index.html', companies=companies)

@app.route('/api/companies')
def get_companies():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM companies')
    companies = []
    for row in c.fetchall():
        companies.append({
            "id": row['id'],
            "name": row['name'],
            "industry": row['industry'],
            "website": row['website'],
            "description": row['description'],
            "logo": row['logo']
        })
    conn.close()
    return jsonify(companies)

@app.route('/api/companies', methods=['POST'])
def create_company():
    data = request.get_json()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        'INSERT INTO companies (id, name, industry, website, description, logo) VALUES (?, ?, ?, ?, ?, ?)',
        (data['id'], data['name'], data['industry'], data['website'], data['description'], data['logo'])
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Company created successfully"}), 201

@app.route('/api/companies/<id>', methods=['PUT'])
def update_company(id):
    data = request.get_json()
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        'UPDATE companies SET name = ?, industry = ?, website = ?, description = ?, logo = ? WHERE id = ?',
        (data['name'], data['industry'], data['website'], data['description'], data['logo'], id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Company updated successfully"})

@app.route('/api/companies/<id>', methods=['DELETE'])
def delete_company(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM companies WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Company deleted successfully"})

@app.route('/api/organization/<company_id>')
def get_organization(company_id):
    conn = get_db_connection()
    c = conn.cursor()
    
    # 获取公司信息
    c.execute('SELECT * FROM companies WHERE id = ?', (company_id,))
    company_row = c.fetchone()
    if not company_row:
        conn.close()
        return jsonify({}), 404
    
    company = {
        "id": company_row['id'],
        "name": company_row['name'],
        "children": []
    }
    
    # 获取公司人员
    c.execute('SELECT * FROM people WHERE companyId = ?', (company_id,))
    people = []
    for row in c.fetchall():
        # 获取人员新闻
        c.execute('SELECT * FROM news WHERE personId = ?', (row['id'],))
        news = []
        for news_row in c.fetchall():
            news.append({
                "title": news_row['title'],
                "url": news_row['url'],
                "date": news_row['date'],
                "source": news_row['source']
            })
        
        people.append({
            "id": row['id'],
            "name": row['name'],
            "position": row['position'],
            "phone": row['phone'],
            "email": row['email'],
            "news": news,
            "parentId": row['parentId']
        })
    
    conn.close()
    
    # 构建组织架构树
    root_nodes = [p for p in people if not p['parentId']]
    
    def build_tree(person):
        children = [build_tree(p) for p in people if p['parentId'] == person['id']]
        person['children'] = children
        del person['parentId']
        return person
    
    for root in root_nodes:
        company['children'].append(build_tree(root))
    
    return jsonify(company)

@app.route('/api/relationships/<person_id>')
def get_relationships(person_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        'SELECT * FROM relationships WHERE person1Id = ? OR person2Id = ?',
        (person_id, person_id)
    )
    related = []
    for row in c.fetchall():
        # 确定目标人员ID
        if row['person1Id'] == person_id:
            target_id = row['person2Id']
        else:
            target_id = row['person1Id']
        
        # 模拟共同联系人数据
        common_connections = []
        if row['commonConnections'] > 0:
            # 模拟共同联系人
            all_common_connections = [
                {"id": "301", "name": "Michael Johnson", "position": "财务总监", "email": "michael.johnson@example.com", "phone": "123-456-7892"},
                {"id": "302", "name": "Sarah Chen", "position": "人力资源总监", "email": "sarah.chen@example.com", "phone": "123-456-7893"},
                {"id": "303", "name": "Robert Williams", "position": "技术总监", "email": "robert.williams@example.com", "phone": "123-456-7894"},
                {"id": "304", "name": "Lisa Wang", "position": "运营总监", "email": "lisa.wang@example.com", "phone": "123-456-7895"},
                {"id": "305", "name": "James Brown", "position": "销售总监", "email": "james.brown@example.com", "phone": "123-456-7896"}
            ]
            common_connections = all_common_connections[:row['commonConnections']]
        
        # 模拟互动活动数据
        interaction_activities = []
        if row['interactionFrequency'] > 0:
            # 根据不同的关系提供不同的活动内容
            if (row['person1Id'] == '111' and row['person2Id'] == '121') or (row['person1Id'] == '121' and row['person2Id'] == '111'):
                # David Taylor 和 John Smith 之间的互动（宝洁内部）
                all_activities = [
                    {"id": "a001", "type": "会议", "description": "宝洁公司产品战略会议", "date": "2023-01-15"},
                    {"id": "a002", "type": "邮件", "date": "2023-02-10", "description": "宝洁市场部项目进度沟通"},
                    {"id": "a003", "type": "电话", "date": "2023-03-05", "description": "宝洁产品紧急问题讨论"},
                    {"id": "a004", "type": "会议", "date": "2023-04-20", "description": "宝洁第一季度业绩回顾会议"},
                    {"id": "a005", "type": "邮件", "date": "2023-05-10", "description": "宝洁新产品营销方案讨论"},
                    {"id": "a006", "type": "会议", "date": "2023-06-15", "description": "宝洁品牌战略规划会议"},
                    {"id": "a007", "type": "电话", "date": "2023-07-05", "description": "宝洁市场活动协调"},
                    {"id": "a008", "type": "邮件", "date": "2023-08-10", "description": "宝洁第三季度计划讨论"},
                    {"id": "a009", "type": "会议", "date": "2023-09-15", "description": "宝洁年度营销总结会议"},
                    {"id": "a010", "type": "邮件", "date": "2023-10-10", "description": "宝洁下一年度预算讨论"}
                ]
            elif (row['person1Id'] == '111' and row['person2Id'] == '211') or (row['person1Id'] == '211' and row['person2Id'] == '111'):
                # David Taylor 和 Alan Jope 之间的互动（宝洁与联合利华）
                all_activities = [
                    {"id": "b001", "type": "会议", "date": "2023-01-20", "description": "行业峰会交流"},
                    {"id": "b002", "type": "邮件", "date": "2023-02-15", "description": "可持续发展合作探讨"},
                    {"id": "b003", "type": "电话", "date": "2023-03-10", "description": "行业趋势讨论"},
                    {"id": "b004", "type": "会议", "date": "2023-04-25", "description": "消费品论坛"},
                    {"id": "b005", "type": "邮件", "date": "2023-05-15", "description": "供应链合作机会讨论"}
                ]
            else:
                # 其他关系的互动
                all_activities = [
                    {"id": "c001", "type": "会议", "date": "2023-01-15", "description": "业务合作会议"},
                    {"id": "c002", "type": "邮件", "date": "2023-02-10", "description": "项目跟进"},
                    {"id": "c003", "type": "电话", "date": "2023-03-05", "description": "问题协调"},
                    {"id": "c004", "type": "会议", "date": "2023-04-20", "description": "季度回顾"},
                    {"id": "c005", "type": "邮件", "date": "2023-05-10", "description": "合作方案讨论"}
                ]
            interaction_activities = all_activities[:row['interactionFrequency']]
        
        if row['person1Id'] == person_id:
            related.append({
                "person1Id": row['person1Id'],
                "person2Id": row['person2Id'],
                "intimacyScore": row['intimacyScore'],
                "commonConnections": row['commonConnections'],
                "commonConnectionsList": common_connections,
                "interactionFrequency": row['interactionFrequency'],
                "interactionActivities": interaction_activities
            })
        else:
            related.append({
                "person1Id": row['person2Id'],
                "person2Id": row['person1Id'],
                "intimacyScore": row['intimacyScore'],
                "commonConnections": row['commonConnections'],
                "commonConnectionsList": common_connections,
                "interactionFrequency": row['interactionFrequency'],
                "interactionActivities": interaction_activities
            })
    conn.close()
    return jsonify(related)

@app.route('/api/analysis/network')
def get_network_analysis():
    """获取网络分析结果"""
    if not analyzer:
        return jsonify({"error": "Analyzer not available"}), 500
    
    analysis = analyzer.analyze_network()
    return jsonify(analysis)

@app.route('/api/analysis/top-connections/<person_id>')
def get_top_connections(person_id):
    """获取某个人的 top N 亲密关系"""
    if not analyzer:
        return jsonify({"error": "Analyzer not available"}), 500
    
    top_connections = analyzer.get_top_connections(person_id)
    return jsonify(top_connections)

@app.route('/api/analysis/predict-connections/<person_id>')
def get_predicted_connections(person_id):
    """获取预测的人脉关系"""
    if not analyzer:
        return jsonify({"error": "Analyzer not available"}), 500
    
    predictions = analyzer.predict_connections(person_id)
    return jsonify(predictions)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)