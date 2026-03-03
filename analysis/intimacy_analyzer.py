import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class IntimacyAnalyzer:
    def __init__(self):
        self.graph = nx.Graph()
    
    def build_network(self, people, relationships):
        """构建人脉关系网络"""
        # 添加人员节点
        for person in people:
            self.graph.add_node(person['id'], name=person['name'], position=person['position'])
        
        # 添加关系边
        for rel in relationships:
            self.graph.add_edge(
                rel['person1Id'],
                rel['person2Id'],
                intimacy=rel['intimacyScore'],
                common_connections=rel['commonConnections'],
                interaction_frequency=rel['interactionFrequency']
            )
    
    def calculate_intimacy(self, person1_id, person2_id):
        """计算两个人之间的亲密指数"""
        if not self.graph.has_edge(person1_id, person2_id):
            return 0
        
        edge_data = self.graph.get_edge_data(person1_id, person2_id)
        return edge_data['intimacy']
    
    def get_top_connections(self, person_id, top_n=5):
        """获取某个人的 top N 亲密关系"""
        if not self.graph.has_node(person_id):
            return []
        
        neighbors = list(self.graph.neighbors(person_id))
        connections = []
        
        for neighbor in neighbors:
            intimacy = self.calculate_intimacy(person_id, neighbor)
            connections.append({
                'personId': neighbor,
                'name': self.graph.nodes[neighbor]['name'],
                'position': self.graph.nodes[neighbor]['position'],
                'intimacyScore': intimacy
            })
        
        # 按亲密指数排序
        connections.sort(key=lambda x: x['intimacyScore'], reverse=True)
        return connections[:top_n]
    
    def analyze_network(self):
        """分析人脉网络"""
        analysis = {
            'nodes': self.graph.number_of_nodes(),
            'edges': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'average_clustering': nx.average_clustering(self.graph),
            'average_degree': np.mean([d for n, d in self.graph.degree()])
        }
        return analysis
    
    def visualize_network(self, output_file='network.png'):
        """可视化人脉网络"""
        plt.figure(figsize=(12, 8))
        
        # 计算节点位置
        pos = nx.spring_layout(self.graph, k=0.3, iterations=50)
        
        # 绘制节点
        node_labels = {node: self.graph.nodes[node]['name'] for node in self.graph.nodes()}
        nx.draw_networkx_nodes(self.graph, pos, node_size=500, node_color='lightblue')
        nx.draw_networkx_labels(self.graph, pos, labels=node_labels, font_size=10)
        
        # 绘制边，根据亲密指数设置颜色和宽度
        edges = self.graph.edges(data=True)
        edge_colors = [edge[2]['intimacy'] for edge in edges]
        edge_widths = [edge[2]['intimacy'] / 20 for edge in edges]
        
        nx.draw_networkx_edges(
            self.graph, 
            pos, 
            edgelist=edges, 
            edge_color=edge_colors, 
            width=edge_widths, 
            edge_cmap=plt.cm.Blues
        )
        
        plt.colorbar(plt.cm.ScalarMappable(cmap=plt.cm.Blues), label='Intimacy Score')
        plt.title('Personnel Network')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
        
        return output_file
    
    def predict_connections(self, person_id, threshold=70):
        """预测可能的人脉关系"""
        if not self.graph.has_node(person_id):
            return []
        
        # 获取所有未连接的节点
        all_nodes = set(self.graph.nodes())
        connected_nodes = set(self.graph.neighbors(person_id)) | {person_id}
        unconnected_nodes = all_nodes - connected_nodes
        
        predictions = []
        for node in unconnected_nodes:
            # 基于共同联系人数量预测亲密指数
            common_neighbors = len(list(nx.common_neighbors(self.graph, person_id, node)))
            predicted_intimacy = min(100, common_neighbors * 20)
            
            if predicted_intimacy >= threshold:
                predictions.append({
                    'personId': node,
                    'name': self.graph.nodes[node]['name'],
                    'position': self.graph.nodes[node]['position'],
                    'predictedIntimacy': predicted_intimacy
                })
        
        # 按预测亲密指数排序
        predictions.sort(key=lambda x: x['predictedIntimacy'], reverse=True)
        return predictions

if __name__ == "__main__":
    # 示例用法
    analyzer = IntimacyAnalyzer()
    
    # 模拟数据
    people = [
        {'id': '111', 'name': 'David Taylor', 'position': 'CEO'},
        {'id': '121', 'name': 'John Smith', 'position': '市场总监'},
        {'id': '211', 'name': 'Alan Jope', 'position': 'CEO'}
    ]
    
    relationships = [
        {
            "person1Id": "111",
            "person2Id": "121",
            "intimacyScore": 85,
            "commonConnections": 5,
            "interactionFrequency": 10
        },
        {
            "person1Id": "111",
            "person2Id": "211",
            "intimacyScore": 60,
            "commonConnections": 3,
            "interactionFrequency": 5
        }
    ]
    
    analyzer.build_network(people, relationships)
    print(analyzer.analyze_network())
    print(analyzer.get_top_connections('111'))
    print(analyzer.predict_connections('111'))
    analyzer.visualize_network()
