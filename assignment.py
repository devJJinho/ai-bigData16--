class Model :
    def __init__(self):
        self.stuDict=dict()
        self.index=0
    
    def addStudent(self,sid,name,mid,fin):
        if sid in self.stuDict:
            return False
        avg=(mid+fin)/2
        self.stuDict[sid]={'sid':sid,'name':name,'mid':mid,'fin':fin,'avg':avg,'grd':self.getGrade(avg)}
        return True

    def importFile(self,fname="students.txt"):
        try:
            read_file=open(fname,'r')
            for line in read_file:
                sid,name,mid,fin=line.split('\t')
                self.addStudent(int(sid),name,int(mid),int(fin))
            read_file.close()
        except:
            print("file error")

    def getGrade(self,score):
        grade="A"
        if score<60:
            grade="F"
        elif score<70:
            grade="D"
        elif score<80:
            grade="c"
        elif score<90:
            grade="B"
        return grade

    def searchById(self,id):
        res=list()
        if id in self.stuDict:
            res.append(list(self.stuDict[id].values()))
        return res
       
    def searchByGrade(self,grade):
        res=list()
        for k,v in self.stuDict.items():
            if v['grd']==grade:
                res.append(list(v.values()))
        return res

    def __iter__(self):
        self.index=0
        self.keys=list(self.stuDict.keys())
        return self

    def __next__(self):
        result=None
        try:
            result=list(self.stuDict[self.keys[self.index]].values())
        except IndexError:
            raise StopIteration
        self.index+=1
        return result
    
    def removeStu(self,id):
        if id in self.stuDict:
            self.stuDict.pop(id)
            return True
        else:
            return False

    def countStu(self):
        return len(self.stuDict)

    def changeScore(self,id,isMid,score):
        if not id in self.stuDict:
            return False
        if isMid:
            self.stuDict[id]['mid']=score
        else : 
            self.stuDict[id]['fin']=score

        self.stuDict[id]['avg']=(self.stuDict[id]['mid']+self.stuDict[id]['fin'])/2
        self.stuDict[id]['grd']=self.getGrade(self.stuDict[id]['avg'])
    

class View:
    def show(self,sidList):
        sidList.sort(key=lambda x:x[4],reverse=True)
        print("   Student           Name       Midterm      Final   Average      Grade")
        print("-"*73)
        for stu in sidList:
            print("%10s %15s %10s %10s %10s %10s" %(stu[0],stu[1],stu[2],stu[3],stu[4],stu[5]))
    
    def rmStu(self):
        return int(input("Student ID: "))
        
    def addStu(self):
        name=input("Name: ")
        mid=int(input("Midtern Score: "))
        fin=int(input("Final Score: "))
        return (name,mid,fin)

    def printElert(self,code):
        errCode={'NO_MATCH':"NO SUCH PERSON.",
                "EMPTY":"List is Empty",
                "NO_RESULT":"NO RESULTS.",
                "REMOVED":"Student removed.",
                "EXIST":"ALREADY EXISTS.",
                "ADDED":"Student added."
                }
        print(errCode[code])
    
    def getID(self):
        return int(input("Student ID: "))
    
    def getGrd(self):
        return input("Grade to search: ")

    def getIsMid(self):
        return input("Mid/Final? ")

    def getNewScore(self):
        return int(input("Input new score: "))
    
    def getQuitOption(self):
        return input("Save data?[yes/no] ")

    def getFname(self):
        return input("File name: ")

class Controller:
    def __init__(self):
        self.model=Model()
        self.view=View()
    
    def initProgram(self,fname):
        self.model.importFile(fname)
        self.showAll()

    def showAll(self):
        member=list()
        for i in self.model:
            member.append(i)
        self.view.show(member)

    def searchById(self):
        searchId=self.view.getID()
        res=self.model.searchById(searchId)
        if not len(res):
            self.view.printElert("NO_MATCH")
        else:
            self.view.show(res)
        
    def searchByGrd(self):
        searchGrd=self.view.getGrd()
        if searchGrd not in ['A','B','C','D','F']:
            return
        res=self.model.searchByGrade(searchGrd)
        if not len(res):
            self.view.printElert("NO_RESULT")
        else:
            self.view.show(res)

    def rmStu(self):
        if not self.model.countStu():
            self.view.printElert("EMPTY")
            return
        delId=self.view.rmStu()
        res=self.model.removeStu(delId)
        if res:
            self.view.printElert("REMOVED")
        else:
            self.view.printElert("NO_MATCH")

    def addStu(self):
        addId=self.view.getID()
        if len(self.model.searchById(addId)):
            self.view.printElert("EXIST")
            return
        name,mid,fin=self.view.addStu()
        if self.model.addStudent(addId,name,mid,fin):
            self.view.printElert("ADDED")
    
    def changeScore(self):
        changeId=self.view.getID()
        orgData=self.model.searchById(changeId)
        if not len(orgData):
            self.view.printElert("NO_MATCH")
            return
        exam=self.view.getIsMid()
        exam=exam.lower()
        if exam not in ['mid','final']:
            return
        nscore=self.view.getNewScore()
        if not 0<=nscore<=100:
            return
        if exam=='mid':
            self.model.changeScore(changeId,True,nscore)
        else:
            self.model.changeScore(changeId,False,nscore)
        self.view.show(orgData)
        print("Score changed")
        self.view.show(self.model.searchById(changeId))

    def quit(self):
        quitOption=self.view.getQuitOption()
        quitOption=quitOption.lower()
        if not quitOption in ['no','yes']:
            return False
        if quitOption=='no':
            return True
        fname=self.view.getFname()
        fw=open(fname,'w')
        ls=list()
        for stu in self.model:
            ls.append(stu)
        ls.sort(key=lambda x:x[4],reverse=True)
        for stu in ls:
            fw.write("%10s %15s %10s %10s %10s %10s\n" %(stu[0],stu[1],stu[2],stu[3],stu[4],stu[5]))
        fw.close()
        return True

def main():
    import sys
    args=sys.argv[1:]
    fname="students.txt"
    controller=Controller()
    if len(args):
        fname=args[0]
    controller.initProgram(fname)
    while True:
        command=input("# ")
        command=command.lower()
        if command=='show':
            controller.showAll()
        elif command=='search':
            controller.searchById()
        elif command=='changescore':
            controller.changeScore()
        elif command=='add':
            controller.addStu()
        elif command=='searchgrade':
            controller.searchByGrd()
        elif command=='remove':
            controller.rmStu()
        elif command=='quit':
            if controller.quit():
                return 

main()