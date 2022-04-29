class Tree:
    def __init__(self, select = None, val = None, data = None):
        if select != None:
            self.select = select
        else:
            self.select = "Select"
        
        if val != None:
            self.val = val
        else:
            self.val = "All"
            
        self.data = data

        self.left = None
        self.right = None
    
    def insert(self, select, val):
        # Assume the insertion is legal
        while (self.left is not None): 
            self = self.left
            if self.select == select:
                print("The filter has been used.")
                return
  
        data = []
        for song in self.data:
            # Common case: No., Year, explicit
            if (song[select] == val) & (select != "genre"): data.append(song)             
            
            # Convert case: Release Year, Time, genre
            if select == "release_date":
                if int(song[select][0:4]) == val: 
                    data.append(song)
            if select == "trackTime":
                if song[select]/60000 < val: 
                    data.append(song)
                    
            if select == "genre":
                if val in song[select].lower(): data.append(song)
        
        if select == "trackTime":
            select = "length"
        if select == "release_date":
            select = "release year"
        if select == "No.":
            select = "rank"
        if select == "year":
            select = "chart year"
        
        self.left = Tree(select=select, val=val, data=data)
        
    def traverse(self, prefix = '', bend = ''):
        # Pre-order Traversal
        print(f'{prefix}{bend}{self.select}: {self.val}, Song list length: {len(self.data)}')
        if self.left:
            if bend == '+-':
                prefix = prefix + '  '
            elif bend == '`-':
                prefix = prefix + '  '
            self.left.traverse(prefix, '+-')
    
    def access(self):
        while (self.left is not None): 
            self = self.left
        return self.data