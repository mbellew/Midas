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

    def right(self,row,col,replace,pad=3):
        l = len(replace)
        if l < pad:
            replace = (' ' * (pad-l)) + replace
        elif l > pad:
            replace = replace[l-pad:]
        self.write(row,col,replace,False)

    def write(self,row,col,replace,eol=True):
        if row >= self.height or col >= self.width:
            return
        l = len(replace)
        avail = self.width-col
        if l > avail:
            replace = replace[0:avail]
        elif eol and l < avail:
            replace = replace + (' ' * (avail-l))
        if self.screen:
            self.screen._write(self.row+row, self.col+col, replace)
        else:
            self._write(row,col,replace)

    def _write(self, row, col, replace):
        s = self.data[row]
        if s[col:col+len(replace)] != replace:
            self.data[row] = s[0:col] + replace + s[col+len(replace):]
            self.dirty = True

    def subArea(self, row, col, height, width):
        height = max(0,min(height,self.height-row))
        width = max(0,min(width,self.width-col))
        return DisplayArea(self.screen or self, self.row+row, self.col+col, height, width)
        