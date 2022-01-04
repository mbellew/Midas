class DisplayArea:
    def __init__(self, screen, row, col, height, width):
        self.screen = screen
        self.row = row
        self.col = col
        self.height = height
        self.width = width
        self.dirty = False
        self.data = []
        if not screen:
            for r in range(0,height):
                self.data.append(" " * width)

    def screen(height,width):
        return DisplayArea(None,0,0,height,width)

    def toString(self):
        ret = "\n".join(self.data)
        self.dirty = False
        return ret

    def isDirty(self):
        return self.dirty

    def write(self,row,col,replace):
        if row >= self.height or col >= self.width:
            return
        if len(replace) > self.width-col:
            replace = replace[0:self.width-col]
        if self.screen:
            self.screen._write(self.row+row, self.col+col, replace)
        else:
            self._write(row,col,replace)

    def _write(self, row, col, replace):
        s = self.data[row]
        if s[col:len(replace)] != replace:
            self.data[row] = s[0:col] + replace + s[col+len(replace):]
            self.dirty = True

    def subArea(self, row, col, height, width):
        height = max(0,min(height,self.height-row))
        width = max(0,min(width,self.width-col))
        return DisplayArea(self.screen or self, self.row+row, self.col+col, height, width)
        