


class MAIN:
    def __init__(self):
        self.board = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]

        self.ai = 'O'
        self.realPlayer = 'X'

        self.print_broad()

        self.check_connect()

    def print_broad(self):  # 印出圈圈叉叉的圖
        number = 0
        for i in range(len(self.board)):
            print('|', end='')
            for j in range(len(self.board[i])):
                number += 1
                if self.board[i][j] == '':
                    print(number, end='|')
                else:
                    print(self.board[i][j], end='|')
            print()


    def check_connect(self):     # 判斷是否有連線
        # horizontal
        for i in range(len(self.board)):
            if self.board[i][0] == self.board[i][1] == self.board[i][2]:
                print(self.board[i][0], 'WIN')
                return

        # vertical
        for i in range(len(self.board[0])):
            if self.board[0][i] == self.board[1][i] == self.board[2][i]:
                print(self.board[0][i], 'WIN')
                return

        # diagonal
        if self.board[0][0] == self.board[1][1] == self.board[2][2]:
            print(self.board[0][0], 'WIN')
            return

        if self.board[0][2] == self.board[1][1] == self.board[2][0]:
            print(self.board[0][2], 'WIN')
            return

        # if full -> tie
        count = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] != '':
                    count += 1

        if count == 9:
            print('TIE')


Main = MAIN()


