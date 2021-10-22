# class Student(list):
#     def __init__(self,sid,name,mid,fin,avg,grd):
#         self.sid=sid
#         self.name=name
#         self.mid=mid
#         self.fin=fin
#         self.avg=avg
#         self.grd=grd
    
#     def changeMidScore(self,nscore):
#         self.mid=nscore

#     def changeFinScore(self,nscore):
#         self.fin=nscore
    
#     def changeAvg(self,navg):
#         self.avg=navg
    
#     def changeGrd(self,ngrd):
#         self.grd=ngrd

#     def __gt__(self,other):
#         return self.avg>other.getAvg()

#     def __lt__(self,other):
#         return self.avg<other.getAvg()

#     def getAvg(self):
#         return self.avg

#     def getGrd(self):
#         return self.grd

#     def getMid(self):
#         return self.mid
    
#     def getFin(self):
#         return self.fin
    
#     def getId(self):
#         return self.sid
    
#     def getName(self):
#         return self.name

class Score :
    def __init__(self):
        self.stuDict=dict()
        self.index=0
    
    def addStudent(self,sid,name,mid,fin):
        if sid in self.stuDict:
            return False
        avg=(mid+fin)/2
        self.stuDict[sid]={'sid':sid,'name':name,'mid':mid,'fin':fin,'avg':avg,'grd':self.getGrade(avg)}
        print(self.stuDict.items())
        return True

    def importFile(self,fname="students.txt"):
        # try:
        read_file=open(fname,'r')
        print(read_file)
        for line in read_file:
            sid,name,mid,fin=line.split('\t')
            print(sid,name,mid,fin)
            self.addStudent(int(sid),name,int(mid),int(fin))
        read_file.close()
        # except:
            # print("file error")

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
        if id in self.stuDict:
            return self.stuDict[id].values()
        else :
            return None
    
    def searchByGrade(self,grade):
        res=list()
        for k,v in self.stuDict.items():
            if v['grd']==grade:
                res.append(list(v.values()))
        return res

    # def members(self):
    #     res=list()
    #     for k,v in self.stuDict.items():
    #         res.append(list(v.values()))
    #     return res

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
            del(self.stuDict,id)
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

        self.stuDict[id]['avg']=(self.stuDict[id]['min']+self.stuDict[id]['fin'])/2
        self.stuDict[id]['grd']=self.getGrade(self.stuDict[id]['avg'])
    

class View:
    def show(self,sidList):
        sidList.sort(key=lambda x:x[4],reverse=True)
        print("   Student           Name       Midterm      Final   Average      Grade")
        print("-"*73)
        for stu in sidList:
            print("%10s %15s %10s %10s %10s %10s" %(stu[0],stu[1],stu[2],stu[3],stu[4],stu[5]))

class Controller:
    def __init__(self,fname="students.txt"):
        self.model=Score(fname)




model=Score()
model.importFile()
view=View()
grade="A"
print(model.searchById(20180009))
aa=model.searchByGrade(grade)
print(aa)
view.show(aa)

member=list()
for i in model:
    member.append(i)

view.show(member)

