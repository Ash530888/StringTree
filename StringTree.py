class STNode:
    def __init__(self,d,l,m,r):
        self.data = d
        self.left = l
        self.right = r
        self.fwd = m
        self.mult = 0
          
    # prints the node and all its children in a string
    def __str__(self):  
        st = "("+str(self.data)+", "+str(self.mult)+") -> ["
        if self.left != None:
            st += str(self.left)
        else: st += "None"
        if self.fwd != None:
            st += ", "+str(self.fwd)
        else: st += ", None"
        if self.right != None:
            st += ", "+str(self.right)
        else: st += ", None"
        return st + "]"
    
    def updateChild(self, oldChild, newChild):
        if self.left==oldChild:
            self.left=newChild
        elif self.fwd==oldChild:
            self.fwd=newChild
        else:
            self.right=newChild
    
class StringTree:
    def __init__(self):
        self.root = None
        self.size = 0
        
    def __str__(self):
        return str(self.root)

    def add(self,st):
        if st == "":
            return None
        if self.root == None:
            self.root = STNode(st[0],None,None,None)
        ptr = self.root
        for i in range(len(st)):
            d = st[i]
            while True:
                if d == ptr.data:
                    break
                elif d < ptr.data:
                    if ptr.left == None:
                        ptr.left = STNode(d,None,None,None)
                    ptr = ptr.left
                else:
                    if ptr.right == None:
                        ptr.right = STNode(d,None,None,None)
                    ptr = ptr.right
            if i < len(st)-1 and ptr.fwd == None:
                ptr.fwd = STNode(st[i+1],None,None,None)
            if i < len(st)-1:
                ptr = ptr.fwd
        ptr.mult += 1
        self.size += 1    
    
    def addAll(self,A):
        for x in A: self.add(x)
        
    def printAll(self):
        def printFrom(ptr,s):
            if ptr == None: return
            s0 = s + ptr.data
            for i in range(ptr.mult,0,-1): print(s0)
            if ptr.left != None: printFrom(ptr.left,s)
            if ptr.fwd != None: printFrom(ptr.fwd,s+ptr.data)
            if ptr.right != None: printFrom(ptr.right,s)

        printFrom(self.root,"")         
    
    # returns the number of times that string st is stored in the tree
    def count(self, st):
        ptr=self.root
        
        for i in range(len(st)):
            d = st[i]
            while True:
                if ptr==None: return 0
                if d == ptr.data:
                    if i==len(st)-1:
                        return ptr.mult
                    ptr=ptr.fwd
                    break
                elif d < ptr.data:
                    if ptr.left == None:
                        return 0
                    ptr = ptr.left
                else:
                    if ptr.right == None:
                        return 0
                    ptr = ptr.right
        return None
                    
                
        
    
    # returns the lexicographically largest string in the tree
    # if the tree is empty, return None
    def max(self):    
        ptr=self.root
        if ptr==None: return None
        st=""
        while ptr!=None:
            if ptr.right!=None:
                ptr=ptr.right
            else:
                st+=ptr.data
                ptr=ptr.fwd
        
        return st

    # returns the lexicographically smallest string in the tree
    # if the tree is empty, return None
    def min(self):    
        # TODO: needs to be implemented
        return 

    # removes one occurrence of string st from the tree and returns None
    # if st does not occur in the tree then it returns without changing the tree
    # it updates the size of the tree accordingly
    def remove(self,st):
        count=self.count(st)
        
        if count==0 or count==None: return
        elif count>1:
            ptr=self.root
            for i in range(len(st)):
                d = st[i]
                while d != ptr.data:
                    if d < ptr.data:
                        ptr = ptr.left
                    else:
                        ptr = ptr.right
                if i==len(st)-1: break
                ptr=ptr.fwd
            ptr.mult=ptr.mult-1
            self.size-=1
        else:
            for i in range(len(st),0,-1):
                st2=st[:i]
                parentPtr=None
                ptr=self.root
                
                index=0
                
                for j in range(len(st2)-1):
                    d = st2[j]
                    while d != ptr.data:
                        if d < ptr.data:
                            ptr = ptr.left
                        else:
                            ptr = ptr.right
                    parentPtr=ptr
                    ptr=ptr.fwd

                while ptr.data!=st2[-1]:
                    parentPtr=ptr
                    if st2[-1] < ptr.data:
                        ptr = ptr.left
                    else:
                        ptr = ptr.right
                
                if (ptr.mult==0 or  (ptr.mult==1 and i==len(st)))and ptr.fwd==None:
                    self.removeNode(ptr, parentPtr)
                #elif ptr.fwd!=None and ptr.data==st[-1]:
                elif ptr.fwd!=None and st2==st:
                    ptr.mult-=1
                    self.size-=1
                    return
                else:
                    self.size-=1
                    return
            
            self.size-=1
                    
                    
    def removeNode(self, ptr, parentPtr):
        if parentPtr==None:
            self.removeRoot()
        elif ptr.left==ptr.right==None:
            parentPtr.updateChild(ptr, None)
        elif ptr.left==None:
            parentPtr.updateChild(ptr, ptr.right)
        elif ptr.right==None:
            parentPtr.updateChild(ptr, ptr.left)
        else:
            parentMinRNode=ptr
            minRNode=ptr.right
            while minRNode.left!=None:
                parentMinRNode=minRNode
                minRNode=minRNode.left
                
            ptr.data=minRNode.data
            ptr.mult=minRNode.mult
            ptr.fwd=minRNode.fwd
            
            parentMinRNode.updateChild(minRNode, minRNode.right)
                
    
    def removeRoot(self):
        parentRoot=STNode(None,self.root,None,None)
        self.removeNode(self.root, parentRoot)
        self.root=parentRoot.left
                
            
        
                        
