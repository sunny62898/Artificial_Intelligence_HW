
'''
想法：
    1.先將地圖畫完
    2.在找查時先把路徑走完，再回頭判斷是否有d-separation
'''

class MAIN:
    def __init__(self):
        self.make_map()     # 製作地圖
        self.input_question()   # 輸入題目
        self.find_collider()
        self.find_unblock()
        self.initial_map()  # 初始化地圖
        self.build_path()   # 建立路徑
        self.find_path()    # 尋找路徑
        self.d_separation()


    def make_map(self):
        self.map_list = []  # 儲存map資訊

        # 開始存map資訊
        # A
        temp_map = MAP('A', ['D'], [], False)
        self.map_list.append(temp_map)

        # B
        temp_map = MAP('B', ['D'], [], False)
        self.map_list.append(temp_map)

        # C
        temp_map = MAP('C', ['E'], [], False)
        self.map_list.append(temp_map)

        # D
        temp_map = MAP('D', ['G', 'H'], ['A', 'B'], False)
        self.map_list.append(temp_map)

        # E
        temp_map = MAP('E', ['I'], ['C', 'H'], False)
        self.map_list.append(temp_map)

        # F
        temp_map = MAP('F', ['I', 'J'], [], False)
        self.map_list.append(temp_map)

        # G
        temp_map = MAP('G', ['K'], ['D'], False)
        self.map_list.append(temp_map)

        # H
        temp_map = MAP('H', ['E', 'K'], ['D'], False)
        self.map_list.append(temp_map)

        # I
        temp_map = MAP('I', ['L'], ['E', 'F'], False)
        self.map_list.append(temp_map)

        # J
        temp_map = MAP('J', ['M'], ['F'], False)
        self.map_list.append(temp_map)

        # K
        temp_map = MAP('K', [], ['G', 'H'], False)
        self.map_list.append(temp_map)

        # L
        temp_map = MAP('L', [], ['I'], False)
        self.map_list.append(temp_map)

        # M
        temp_map = MAP('M', [], ['J'], False)
        self.map_list.append(temp_map)

    def input_question(self):
        self.start_point = input("start point : ")
        input_z_point = input("z set(以逗號分隔) : ")

        self.z_point = input_z_point.split(',')


    def initial_map(self):
        for i in self.map_list:
            i.beWalk = False

    def build_path(self):
        self.path_stack = []

        start_location = self.start_point    # 起點

        temp_stack = STACK(start_location, None)
        self.path_stack.append(temp_stack)

        number_of_stack = 0     # 現在在stack的第幾層

        while number_of_stack < len(self.path_stack):

            # 現在位置
            location_now = self.path_stack[number_of_stack].now
            location_comeFrom_number = self.path_stack[number_of_stack].comeFrom
            # 查詢從哪裡來 以防無限循環
            if location_comeFrom_number != None:
                location_comeFrom = self.path_stack[location_comeFrom_number].now
            else:
                location_comeFrom = -1

            # print(location_now)
            # print(location_comeFrom)

            # 查詢地圖
            now_map = None
            for i in self.map_list:
                if i.name == location_now:
                    now_map = i
                    break

            # 標記已經被走過
            now_map.beWalk = True

            # 儲存toPoint和bePoint資料
            now_toPoint = now_map.toPoint
            now_bePoint = now_map.bePoint

            # print(now_toPoint)
            # print(now_bePoint)

            # 增加stack
            # 儲存 toPoint
            for i in now_toPoint:
                if self.judge_beWalk(i):
                    continue

                if i != location_comeFrom:   # 從誰來的不能存
                    temp_stack = STACK(i, number_of_stack)
                    self.path_stack.append(temp_stack)

            # 儲存 bePoint
            for i in now_bePoint:
                if self.judge_beWalk(i):
                    continue

                if i != location_comeFrom:  # 從誰來的不能存

                    temp_stack = STACK(i, number_of_stack)
                    self.path_stack.append(temp_stack)

            # print('len fo path stack', len(self.path_stack))

            # 前往下一個stack
            number_of_stack += 1
            # print('number of stack', number_of_stack)


    def judge_final(self, final_location, location):
        if final_location == location:
            return True
        else:
            return False

    def judge_beWalk(self, location):
        for i in self.map_list:
            if i.name == location:
                if i.beWalk:
                    return True
                else:
                    return False

    def find_path(self):
        self.point_list = []

        for i in range(len(self.path_stack)):
            self.point_list.append(self.path_stack[i].now)


    def find_collider(self):
        self.collider_list = []      # 被兩個箭頭所指向的點
        head_list = []          # 箭頭所指向的點
        tail_list = []          # 箭尾的點

        for i in self.map_list:
            if len(i.bePoint) > 0:
                head_list.append(i.name)
            if len(i.toPoint) > 0:
                tail_list.append(i.name)

            if len(i.bePoint) > 1:
                self.collider_list.append(i.name)

            for j in i.bePoint:
                tail_list.append(j)

            for j in i.toPoint:
                head_list.append(j)


    def find_unblock(self):
        self.unblock_list = []

        for i in self.collider_list:
            descendant = []
            descendant.append(i)

            number = 0
            while number < len(descendant):
                descendant = self.searchMap_zSet(descendant[number], descendant)
                number += 1

            for j in descendant:
                if self.judge_zSet(j):
                    self.unblock_list.append(i)

        print('unblock', self.unblock_list)


    def d_separation(self):

        self.d_connect_list = []
        self.d_connect_list.append(self.start_point)
        past_list = []

        while self.d_connect_list != past_list:
            for i in self.d_connect_list:
                if i not in past_list:
                    past_list.append(i)
                    if not self.judge_zSet(i):

                        if i in self.unblock_list:
                            self.d_connect_list = self.searchMap_zSet_head(i, self.d_connect_list)
                            self.d_connect_list = self.searchMap_zSet_tail(i, self.d_connect_list)

                        else:
                            self.d_connect_list = self.searchMap_zSet_tail(i, self.d_connect_list)

                    self.d_connect_list = sorted(set(self.d_connect_list))
                    past_list = sorted(set(past_list))


        print(self.d_connect_list)
        self.different_set()

    def different_set(self):
        original_set = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
        d_separation = []
        for i in original_set:
            if i not in self.d_connect_list:
                d_separation.append(i)

        print(d_separation)


    def searchMap_zSet(self, point, d_list):
        for map in self.map_list:
            # 去查每個的tail，若有point，就將head加入list
            for i in map.bePoint:
                if i == point:
                    d_list.append(map.name)

        return d_list

    def searchMap_zSet_head(self, point, list):
        for map in self.map_list:
            # 去查每個的to point，若有point，就將tail加入list
            for i in map.toPoint:
                if i == point:
                    if not self.judge_zSet(map.name):
                        list.append(map.name)

        return list

    def searchMap_zSet_tail(self, point, list):
        for map in self.map_list:
            # 去查每個的be point，若有point，就將head加入list
            for i in map.bePoint:
                if i == point:
                    if not self.judge_zSet(map.name):
                        list.append(map.name)

        return list


    def judge_zSet(self, point):
        for i in self.z_point:  # 判斷是否在z set中
            if i == point:
                return True

        return False

    def add_nearPoint(self, point, now_list):
        for map in self.map_list:
            if map.name == point:
                for i in map.toPoint:
                    now_list.append(i)
                for i in map.bePoint:
                    if not self.judge_zSet(i):
                        now_list.append(i)

                return now_list

    def judge_point(self, location, front, after):

        for map in self.map_list:
            if map.name == location:
                front_point = -1
                after_point = -1
                for i in map.toPoint:
                    if front == i:
                        front_point = 1     # toPoint
                    if after == i:
                        after_point = 1     # toPoint
                for i in map.bePoint:
                    if front == i:
                        front_point = 2     # bePoint
                    if after == i:
                        after_point = 2     # bePoint

                return front_point, after_point


# 地圖class
class MAP:
    def __init__(self, name, toPoint, bePoint, beWalk):
        self.name = name
        self.toPoint = toPoint  # 指向誰
        self.bePoint = bePoint  # 被誰指
        self.beWalk = beWalk    # 記錄有沒有被走過(boolean)


# stack class
class STACK:
    def __init__(self, now, comeFrom):
        self.now = now      # 記錄現在位置
        self.comeFrom = comeFrom     # 記錄從哪一層stack來的



Main = MAIN()


