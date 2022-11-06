#include<iostream>
#include<queue>
#include<vector>
#include<stack>
#include<algorithm>

using namespace std;

int map[6][6]  
{
	{ 0, 0, 0, 0, 0, 0},
	{ 0, 0, 0, 0, 1, 1},
	{ 0, 0, 0, 0, 0, 0},
	{ 1, 1, 1, 1, 0, 0},
	{ 1, 0, 0, 0, 0, 1},
	{ 0, 0, 0, 0, 0, 1}
};

typedef struct Node{
	
	int x, y;
	int g_value; 		//現在到下一個點的cost
	int h_value;		//現在到目標的cost
	int f_value;		//g+h
	Node* father_pointer;
	Node(int x, int y){
		
		this->x = x;
		this->y = y;
		this->g_value = 0;
		this->h_value = 0;
		this->f_value = 0;
		this->father_pointer = NULL;
	}
	Node(int x, int y, Node* father_pointer){
		
		this->x = x;
		this->y = y;
		this->g_value = 0;
		this->h_value = 0;
		this->f_value = 0;
		this->father_pointer = father_pointer;
	}
}Node;


class Astar{
	
public:
	
	vector<Node*> open_list;
	vector<Node*> close_list;
	Node *start_point;
	Node *end_point;
	static const float beside_weight = 1;		//上下左右 
	static const float incline_weight = 1.4;	//斜 
	static const int row = 6;
	static const int col = 6;
	
	void search(Node* start_point, Node* end_point){
		if (start_point->x < 0 || start_point->x > row || start_point->y < 0 || start_point->y >col ||
			end_point->x < 0 || end_point->x > row || end_point->y < 0 || end_point->y > col){
				return;
			}
			
		Node* now;
		this->start_point = start_point;
		this->end_point = end_point;
		
		open_list.push_back(start_point);
		
		while (open_list.size() > 0){
			
			now = open_list[0];
			if (now->x == end_point->x && now->y == end_point->y){
				
				printPathPoint(now);
				open_list.clear();
				close_list.clear();
				break;
			}
			next_step(now);
			close_list.push_back(now);
			open_list.erase(open_list.begin());
			sort(open_list.begin(), open_list.end(), compare);
		}
	}

	void judge_togo(int x, int y, Node* father, int g){
		if (x < 0 || x > row || y < 0 || y > col){
			return;
		}
			
		if (this->obstacle(x, y)){
			return;
		}
			
		if (include_orNot(&close_list, x, y) != -1){
			return;
		}
			
		int index;
		if ((index = include_orNot(&open_list, x, y)) != -1){
			
			Node *point = open_list[index];
			if (point->g_value > father->g_value + g){
				
				point->father_pointer = father;
				point->g_value = father->g_value + g;
				point->f_value = point->g_value + point->h_value;
			}
		}
		else{
			
			Node * point = new Node(x, y, father);
			ghf_calculate(point, end_point, g);
			open_list.push_back(point);
		}
	}
	
	void next_step(Node* now){
		judge_togo(now->x - 1, now->y, now, beside_weight);		//左
		judge_togo(now->x + 1, now->y, now, beside_weight);		//右
		judge_togo(now->x, now->y + 1, now, beside_weight);		//上
		judge_togo(now->x, now->y - 1, now, beside_weight);		//下
		judge_togo(now->x - 1, now->y + 1, now, incline_weight);	//左上
		judge_togo(now->x - 1, now->y - 1, now, incline_weight);	//左下
		judge_togo(now->x + 1, now->y - 1, now, incline_weight);	//右下
		judge_togo(now->x + 1, now->y + 1, now, incline_weight);	//右上
	}
	
	int include_orNot(vector<Node*>* Nodelist, int x, int y){
		for (int i = 0; i < Nodelist->size(); i++){
			
			if (Nodelist->at(i)->x == x && Nodelist->at(i)->y == y){
				
				return i;
			}
		}
		return -1;
	}
	
	void ghf_calculate(Node* startNode, Node* endNode, int g){
		int h = (abs(startNode->x - endNode->x) + abs(startNode->y - endNode->y)) * beside_weight;
		int g_now = startNode->father_pointer->g_value + g;
		int f = g_now + h;
		startNode->f_value = f;
		startNode->h_value = h;
		startNode->g_value = g_now;
	}
	
	static bool compare(Node* n1, Node* n2){
		return n1->f_value < n2->f_value;
	}
	
	bool obstacle(int x, int y){
		if (map[x][y] == 1)
			return true;
		return false;
	}

	void printPathPoint(Node* now){
		if (now->father_pointer != NULL)
			printPathPoint(now->father_pointer);
		printf("(%d,%d) ", now->x, now->y);
	}
	
	
};


int main(){
	
	Astar astar;
	Node *start_point = new Node(0, 0);
	Node *end_point = new Node(5, 2);
	astar.search(start_point, end_point);
	
	return 0;
}
