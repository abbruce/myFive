#带AI的五子棋程序
import wx
UNIT=30
ROW_NODE_NUM=15
BOARD = []
for i in range(UNIT, UNIT * ROW_NODE_NUM + UNIT, UNIT):
    for j in range(UNIT, UNIT * ROW_NODE_NUM + UNIT, UNIT):
        BOARD.append((j, i))
print(BOARD)
class myFrame(wx.Frame):
    def __init__(self):
        self.unit = UNIT
        self.pointNum = ROW_NODE_NUM#每行落棋点数
        self.pieceNum=0
        self.bkCol=(220, 210, 0)
        self.wht=(255,255,255)
        self.blk=(0,0,0)
        self.actColor=self.blk
        self.piecePos =[]
        self.piecePosCols =[]
        # 元组列表记录落棋位置和落棋颜色
        super().__init__\
            (parent=None,pos=[800,100],
             size=[self.unit*self.pointNum
                   +self.unit+20,
                   self.unit*self.pointNum
                   +self.unit+30+20],
             title="商贾三国")
        self.SetIcon(wx.Icon("WeatherBundle.ico"))
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(self.bkCol)
        self.tip = \
            wx.TextCtrl(self.panel, -1, "",
                        pos=(self.unit*self.pointNum
                             +self.unit-80, 0),
                        size=(80,25))
        self.tip.SetBackgroundColour(self.bkCol)
        self.panel.Bind(wx.EVT_PAINT,self.draw)
        self.panel.Bind(wx.EVT_LEFT_UP, self.OnClick)
        self.Show()
    def draw(self,event):
        mydc=wx.PaintDC(self.panel)
        unit=self.unit
        pointNum=self.pointNum
        x=unit
        y=unit
        for i in range(1,pointNum+1):
            mydc.DrawLine(x,y,x,unit*pointNum)
            x=x+unit
        x=unit
        for i in range(1,pointNum+1):
            mydc.DrawLine(x, y, unit*pointNum, y)
            y=y+unit
        for i in range(0,len(self.piecePos)):
            mydc.SetBrush(wx.Brush(self.piecePosCols[i][2]))
            mydc.DrawCircle(self.piecePos[i][0],
                            self.piecePos[i][1], self.unit / 2.5)
    def OnClick(self,event):
        unit=self.unit
        pos = event.GetPosition()
        mydc=wx.ClientDC(self.panel)
        mydc.SetBrush(wx.Brush(self.actColor))
        x = round(pos.x / unit) * unit
        y = round(pos.y / unit) * unit
        piecePo = (x, y)
        if piecePo in BOARD:
            if piecePo not in self.piecePos:
                if self.actColor == self.blk:
                    piecePoCol=(x,y,self.actColor)
                    if piecePo not in self.piecePos:
                        mydc.DrawCircle(x,y,self.unit/2.5)
                        self.piecePos.append(piecePo)
                        self.piecePosCols.append(piecePoCol)
                        self.fiveChk(piecePo)
                        self.pieceNum = self.pieceNum+1
                        print(self.pieceNum)
                        self.tip.SetValue('%s,%s' % (x,y))
                        self.actColor = self.wht
                if self.actColor == self.wht:
                    self.board()
                    print(self.result)
                    mydc.SetBrush(wx.Brush(self.actColor))
                    x = self.result[0]
                    y = self.result[1]
                    piecePo = (x, y)
                    piecePoCol = (x, y, self.actColor)
                    if piecePo not in self.piecePos:
                        mydc.DrawCircle(x, y, self.unit / 2.5)
                        self.piecePos.append(piecePo)
                        self.piecePosCols.append(piecePoCol)
                        self.fiveChk(piecePo)
                        self.pieceNum = self.pieceNum + 1
                        print(self.pieceNum)
                        self.tip.SetValue('%s,%s' % (x, y))
                        self.actColor = self.blk
    def board(self):
        lfupWnum=0
        lfupBnum=0
        xlist=0
        nodeScore=0
        boardScore=[]
        for node in BOARD:
            if node not in self.piecePos:
                # 左上右下
                lfupWnum = 0
                lfupBnum = 0
                xlist = 0
                nodeScore = 0
                for i in [-1,-2,-3,-4,-5]:
                    node_lfup=(node[0]+i*UNIT,node[1]+i*UNIT)
                    if node_lfup in BOARD:
                        if node_lfup in self.piecePos:
                            index=self.piecePos.index(node_lfup)
                            if self.piecePosCols[index][2]==(255,255,255):
                                lfupWnum=lfupWnum+1
                            else:
                                xlist=xlist+1
                                break
                        else:
                            xlist = xlist
                            break
                    else:
                        xlist = xlist + 1
                        break
                for i in [1,2,3,4,5]:
                    node_lfup = (node[0] + i * UNIT, node[1] + i * UNIT)
                    if node_lfup in BOARD:
                        if node_lfup in self.piecePos:
                            index = self.piecePos.index(node_lfup)
                            if self.piecePosCols[index][2] == (255, 255, 255):
                                lfupWnum = lfupWnum + 1
                            else:
                                xlist = xlist + 1
                                break
                        else:
                            xlist = xlist
                            break
                    else:
                        xlist = xlist + 1
                        break
                nodeScore = self.aiW(xlist, lfupWnum) + nodeScore
                print(nodeScore)
                xlist = 0
                for i in [-1,-2,-3,-4,-5]:
                    node_lfup=(node[0]+i*UNIT,node[1]+i*UNIT)
                    if node_lfup in BOARD:
                        if node_lfup in self.piecePos:
                            index=self.piecePos.index(node_lfup)
                            if self.piecePosCols[index][2]==(0,0,0):
                                lfupBnum=lfupBnum+1
                            else:
                                xlist=xlist+1
                                break
                        else:
                            xlist = xlist
                            break
                    else:
                        xlist = xlist + 1
                        break
                for i in [1,2,3,4,5]:
                    node_lfup = (node[0] + i * UNIT, node[1] + i * UNIT)
                    if node_lfup in BOARD:
                        if node_lfup in self.piecePos:
                            index = self.piecePos.index(node_lfup)
                            if self.piecePosCols[index][2] == (0,0,0):
                                lfupBnum = lfupBnum + 1
                            else:
                                xlist = xlist + 1
                                break
                        else:
                            xlist = xlist
                            break
                    else:
                        xlist = xlist + 1
                        break
                nodeScore=self.aiB(xlist,lfupBnum)+nodeScore
                print(nodeScore)
                # 左下右上
                lfupWnum = 0
                lfupBnum = 0
                xlist = 0
                for i in [-1,-2,-3,-4,-5]:
                    node_lfdn = (node[0] + i * UNIT, node[1] - i * UNIT)
                    if node_lfdn in BOARD:
                        if node_lfdn in self.piecePos:
                            index=self.piecePos.index(node_lfdn)
                            if self.piecePosCols[index][2]==(255,255,255):
                                lfupWnum=lfupWnum+1
                            else:
                                xlist=xlist+1
                                break
                        else:
                            xlist = xlist
                            break
                    else:
                        xlist = xlist + 1
                        break
                for i in [1,2,3,4,5]:
                    node_lfdn = (node[0] + i * UNIT, node[1] - i * UNIT)
                    if node_lfdn in BOARD:
                        if node_lfdn in self.piecePos:
                            index = self.piecePos.index(node_lfdn)
                            if self.piecePosCols[index][2] == (255, 255, 255):
                                lfupWnum = lfupWnum + 1
                            else:
                                xlist = xlist + 1
                                break
                        else:
                            xlist = xlist
                            break
                    else:
                        xlist = xlist + 1
                        break
                nodeScore = self.aiW(xlist, lfupWnum) + nodeScore
                print(nodeScore)
                xlist = 0
                for i in [-1,-2,-3,-4,-5]:
                    node_lfdn = (node[0] + i * UNIT, node[1] - i * UNIT)
                    if node_lfdn in BOARD:
                        if node_lfdn in self.piecePos:
                            index=self.piecePos.index(node_lfdn)
                            if self.piecePosCols[index][2]==(0,0,0):
                                lfupBnum=lfupBnum+1
                            else:
                                xlist=xlist+1
                                break
                        else:
                            xlist = xlist
                            break
                    else:
                        xlist = xlist + 1
                        break
                for i in [1,2,3,4,5]:
                    node_lfdn = (node[0] + i * UNIT, node[1] - i * UNIT)
                    if node_lfdn in BOARD:
                        if node_lfdn in self.piecePos:
                            index = self.piecePos.index(node_lfdn)
                            if self.piecePosCols[index][2] == (0,0,0):
                                lfupBnum = lfupBnum + 1
                            else:
                                xlist = xlist + 1
                                break
                        else:
                            xlist = xlist
                            break
                    else:
                        xlist = xlist + 1
                        break
                nodeScore=self.aiB(xlist,lfupBnum)+nodeScore
                print(nodeScore)
                # 左右
                lfupWnum = 0
                lfupBnum = 0
                xlist = 0
                for i in [-1,-2,-3,-4,-5]:
                    node_lf = (node[0] + i * UNIT, node[1])
                    if node_lf in BOARD:
                        if node_lf in self.piecePos:
                            index=self.piecePos.index(node_lf)
                            if self.piecePosCols[index][2]==(255,255,255):
                                lfupWnum=lfupWnum+1
                            else:
                                xlist=xlist+1
                                break
                        else:
                            xlist = xlist
                            break
                    else:
                        xlist = xlist + 1
                        break
                for i in [1,2,3,4,5]:
                    node_lf = (node[0] + i * UNIT, node[1])
                    if node_lf in BOARD:
                        if node_lf in self.piecePos:
                            index = self.piecePos.index(node_lf)
                            if self.piecePosCols[index][2] == (255, 255, 255):
                                lfupWnum = lfupWnum + 1
                            else:
                                xlist = xlist + 1
                                break
                        else:
                            xlist = xlist
                            break
                    else:
                        xlist = xlist + 1
                        break
                nodeScore = self.aiW(xlist, lfupWnum) + nodeScore
                print(nodeScore)
                xlist = 0
                for i in [-1,-2,-3,-4,-5]:
                    node_lf = (node[0] + i * UNIT, node[1])
                    if node_lf in BOARD:
                        if node_lf in self.piecePos:
                            index=self.piecePos.index(node_lf)
                            if self.piecePosCols[index][2]==(0,0,0):
                                lfupBnum=lfupBnum+1
                            else:
                                xlist=xlist+1
                                break
                        else:
                            xlist = xlist
                            break
                    else:
                        xlist = xlist + 1
                        break
                for i in [1,2,3,4,5]:
                    node_lf = (node[0] + i * UNIT, node[1])
                    if node_lf in BOARD:
                        if node_lf in self.piecePos:
                            index = self.piecePos.index(node_lf)
                            if self.piecePosCols[index][2] == (0,0,0):
                                lfupBnum = lfupBnum + 1
                            else:
                                xlist = xlist + 1
                                break
                        else:
                            xlist = xlist
                            break
                    else:
                        xlist = xlist + 1
                        break
                nodeScore = self.aiB(xlist, lfupBnum) + nodeScore
                print(nodeScore)
                # 上下
                lfupWnum = 0
                lfupBnum = 0
                xlist = 0
                for i in [-1,-2,-3,-4,-5]:
                    node_up = (node[0], node[1] + i * UNIT)
                    if node_up in BOARD:
                        if node_up in self.piecePos:
                            index=self.piecePos.index(node_up)
                            if self.piecePosCols[index][2]==(255,255,255):
                                lfupWnum=lfupWnum+1
                            else:
                                xlist=xlist+1
                                break
                        else:
                            xlist = xlist
                            break
                    else:
                        xlist = xlist + 1
                        break
                for i in [1,2,3,4,5]:
                    node_up = (node[0], node[1] + i * UNIT)
                    if node_up in BOARD:
                        if node_up in self.piecePos:
                            index = self.piecePos.index(node_up)
                            if self.piecePosCols[index][2] == (255, 255, 255):
                                lfupWnum = lfupWnum + 1
                            else:
                                xlist = xlist + 1
                                break
                        else:
                            xlist = xlist
                            break
                    else:
                        xlist = xlist + 1
                        break
                nodeScore = self.aiW(xlist, lfupWnum) + nodeScore
                print(nodeScore)
                xlist = 0
                for i in [-1,-2,-3,-4,-5]:
                    node_up = (node[0], node[1] + i * UNIT)
                    if node_up in BOARD:
                        if node_up in self.piecePos:
                            index=self.piecePos.index(node_up)
                            if self.piecePosCols[index][2]==(0,0,0):
                                lfupBnum=lfupBnum+1
                            else:
                                xlist=xlist+1
                                break
                        else:
                            xlist = xlist
                            break
                    else:
                        xlist = xlist + 1
                        break
                for i in [1,2,3,4,5]:
                    node_up = (node[0], node[1] + i * UNIT)
                    if node_up in BOARD:
                        if node_up in self.piecePos:
                            index = self.piecePos.index(node_up)
                            if self.piecePosCols[index][2] == (0,0,0):
                                lfupBnum = lfupBnum + 1
                            else:
                                xlist = xlist + 1
                                break
                        else:
                            xlist = xlist
                            break
                    else:
                        xlist = xlist + 1
                        break
                nodeScore = self.aiB(xlist, lfupBnum) + nodeScore
                print(nodeScore)
            else:nodeScore=0
            boardScore.append(nodeScore)
        for iii in range(0,(ROW_NODE_NUM*ROW_NODE_NUM),ROW_NODE_NUM):
            print(boardScore[iii:(iii+ROW_NODE_NUM)])
        ind=boardScore.index(max(boardScore))
        self.result=BOARD[ind]
    def aiW(self,xlist,Wnum):
        Xlist=[0,1,2]
        Ylist=[0,1,2,3,4,5,6,7,8]
        ZlistW = [[10, 50, 100, 1000, 10000, 10000, 1000, 1000, 1000],
                  [ 0, 10,  50,  100, 10000, 1000, 1000, 1000, 1000],
                  [ 0,  0,   0,    0, 10000, 1000, 1000, 1000, 1000]]
        x=Xlist.index(xlist)
        y=Ylist.index(Wnum)
        zW=ZlistW[x][y]
        return zW
    def aiB(self,xlist,Bnum):
        Xlist=[0,1,2]
        Ylist=[0,1,2,3,4,5,6,7,8]
        ZlistB = [[ 0, 50, 100,500, 0, 10000, 1000, 1000,1000],
                  [ 0, 10, 50, 100,5000, 10000, 1000, 1000,1000],
                  [ 0,  0,  0,  0, 5000, 10000, 10000, 1000,1000]]
        x=Xlist.index(xlist)
        y=Ylist.index(Bnum)
        zB=ZlistB[x][y]
        return zB
    def fiveChk(self,node):
        # 左上右下
        lfupWnum = 0
        for i in [-1, -2, -3, -4, -5]:
            node_lfup = (node[0] + i * UNIT, node[1] + i * UNIT)
            if node_lfup in BOARD:
                if node_lfup in self.piecePos:
                    index = self.piecePos.index(node_lfup)
                    if self.piecePosCols[index][2] == self.actColor:
                        lfupWnum = lfupWnum + 1
                    else:
                        break
                else:
                    break
            else:
                break
        for i in [1, 2, 3, 4, 5]:
            node_lfup = (node[0] + i * UNIT, node[1] + i * UNIT)
            if node_lfup in BOARD:
                if node_lfup in self.piecePos:
                    index = self.piecePos.index(node_lfup)
                    if self.piecePosCols[index][2] == self.actColor:
                        lfupWnum = lfupWnum + 1
                    else:
                        break
                else:
                    break
            else:
                break
        if lfupWnum>=4:
            dlg = wx.MessageDialog(None, u"对局结束", u"五子已经连成",
                                   wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()
            self.Destroy()
            return
        # 左下右上
        lfupWnum = 0
        for i in [-1, -2, -3, -4, -5]:
            node_lfdn = (node[0] + i * UNIT, node[1] - i * UNIT)
            if node_lfdn in BOARD:
                if node_lfdn in self.piecePos:
                    index = self.piecePos.index(node_lfdn)
                    if self.piecePosCols[index][2] == self.actColor:
                        lfupWnum = lfupWnum + 1
                    else:
                        break
                else:

                    break
            else:

                break
        for i in [1, 2, 3, 4, 5]:
            node_lfdn = (node[0] + i * UNIT, node[1] - i * UNIT)
            if node_lfdn in BOARD:
                if node_lfdn in self.piecePos:
                    index = self.piecePos.index(node_lfdn)
                    if self.piecePosCols[index][2] == self.actColor:
                        lfupWnum = lfupWnum + 1
                    else:
                        break
                else:
                    break
            else:
                break
        if lfupWnum>=4:
            dlg = wx.MessageDialog(None, u"对局结束", u"五子已经连成",
                                   wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()
            self.Destroy()
            return
        # 左右
        lfupWnum = 0
        for i in [-1, -2, -3, -4, -5]:
            node_lf = (node[0] + i * UNIT, node[1])
            if node_lf in BOARD:
                if node_lf in self.piecePos:
                    index = self.piecePos.index(node_lf)
                    if self.piecePosCols[index][2] == self.actColor:
                        lfupWnum = lfupWnum + 1
                    else:
                        break
                else:

                    break
            else:

                break
        for i in [1, 2, 3, 4, 5]:
            node_lf = (node[0] + i * UNIT, node[1])
            if node_lf in BOARD:
                if node_lf in self.piecePos:
                    index = self.piecePos.index(node_lf)
                    if self.piecePosCols[index][2] == self.actColor:
                        lfupWnum = lfupWnum + 1
                    else:

                        break
                else:

                    break
            else:

                break
        if lfupWnum>=4:
            dlg = wx.MessageDialog(None, u"对局结束", u"五子已经连成",
                                   wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()
                self.Destroy()
            return
        # 上下
        lfupWnum = 0
        for i in [-1, -2, -3, -4, -5]:
            node_up = (node[0], node[1] + i * UNIT)
            if node_up in BOARD:
                if node_up in self.piecePos:
                    index = self.piecePos.index(node_up)
                    if self.piecePosCols[index][2] == self.actColor:
                        lfupWnum = lfupWnum + 1
                    else:
                        break
                else:
                    break
            else:
                break
        for i in [1, 2, 3, 4, 5]:
            node_up = (node[0], node[1] + i * UNIT)
            if node_up in BOARD:
                if node_up in self.piecePos:
                    index = self.piecePos.index(node_up)
                    if self.piecePosCols[index][2] == self.actColor:
                        lfupWnum = lfupWnum + 1
                    else:
                        break
                else:
                    break
            else:
                break
        if lfupWnum>=4:
            dlg = wx.MessageDialog(None, u"对局结束", u"五子已经连成",
                                   wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                dlg.Destroy()
            self.Destroy()
            return
myapp=wx.App()
myframe=myFrame()
myapp.MainLoop()

