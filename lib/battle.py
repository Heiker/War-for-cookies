#-*- coding: utf-8 -*-
import os, math, unit_w, lib_game.core
from random import randint
class Battle():
    def __init__(self):
        infantry=unit_w.Unit('data\\units\\infantry.txt')
        marines=unit_w.Unit('data\\units\\marines.txt')
        mob_infantry=unit_w.Unit('data\\units\\mobinf.txt')
        tank=unit_w.Unit('data\\units\\tank.txt')
        artillery=unit_w.Unit('data\\units\\artillery.txt')
        self.core=core.Core()
        self.units_list=[infantry,marines,mob_infantry,tank,artillery]
        self.hp_last1=[infantry.get_abil('xp',0),marines.get_abil('xp',0),mob_infantry.get_abil('xp',0),tank.get_abil('xp',0),artillery.get_abil('xp',0)]
        self.hp_last2=[infantry.get_abil('xp',0),marines.get_abil('xp',0),mob_infantry.get_abil('xp',0),tank.get_abil('xp',0),artillery.get_abil('xp',0)]
        self.move_last1=[infantry.get_abil('move',0),marines.get_abil('move',0),mob_infantry.get_abil('move',0),tank.get_abil('move',0),artillery.get_abil('move',0)]
        self.move_last1=[infantry.get_abil('move',0),marines.get_abil('move',0),mob_infantry.get_abil('move',0),tank.get_abil('move',0),artillery.get_abil('move',0)]
        self.cells_list=core.load_battle_cells(self,current_name)
        self.coord_army1=get_army_coords(self.cells_list,0)
        self.coord_army2=get_army_coords(self.cells_list,0)
        #остаток здоровья и остаток хода
    def find_strength(self, army):
        strength=0
        for i in range(5):
            strength+=army[i+1]*(self.units_list[i].get_abil('xp',0)+self.units_list[i].get_abil('kick',0)+self.units_list[i].get_abil('move',0))
        return strength
        
    def chanse(self,army_str1, army_str2):
        chans=army_str1/float(army_str2)
        if (chans<0.2):
            str='Однозначное поражение'
        elif(chans<0.4):
            str='Тяжелое поражение'
        elif(chans<0.6):
            str='Поражение'
        elif(chans<0.8):
            str='Незначительное поражение'
        elif(chans<1):
            str='Паритет'
        elif(chans<1.2):
            str='Пиррова победа'
        elif(chans<1.4):
            str='Тяжелая победа'
        elif(chans<1.6):
            str='Победа'
        elif(chans<1.8):
            str='Блестящая победа'
        else:
            str='Легкая разминка'
        print str
        
    def kick(self,army1,army2,type1,type2):
        self.move_last1[type1-1]=0#no more moving
        damag=(army1[type1]*rendom.randintself.units_list[type1].get_abil('kick',0)*self.units_list[type1].get_abil('bonus',type2))#количество*тычка*бонус
        last_health=math.modf(army2[type2]-damag/self.units_list[type2].get_abil('xp',0))
        if(last_health[1]<0):#если убили
            last_health[0]=0
            last_health[1]=0
        self.hp_last2[type2-1]=last_health[0]*self.units_list[type2].get_abil('xp',0)
        army2[type2]= last_health[1]
        return army2
    
    def is_in_range(self,coord_army1,coord_army2,attacker,victim):
        distance_x=coord_army1[attacker][0]-coord_army2[victim][0]-self.units_list[attacker].get_abil('range',0)
        distance_y=coord_army1[attacker][1]-coord_army2[victim][1]-self.units_list[attacker].get_abil('range',0)
        in_range_by_x=distance_x<=0
        in_range_by_y=distance_y<=0
        if (in_range_by_x and in_range_by_y):
            return True
        return False
        
    def get_alive(self,army):
        alive_list=[]
        for i in range(1,5):
            if (army[1]>0):
                alive_list.append(i)
        return alive_list
    
    def get_vunerable(self,atacker,army2):
        victim=0
        alive_list=get_alive(army2)
        for i in range(alive_list.len()):
            if (victim<self.units_list[atacker].get_abil('bonus',alive_list[i])):
                temp=alive_list[i]
                victim=self.units_list[atacker].get_abil('bonus',alive_list[i])
        return temp
    
    def bot_moving(self,unit_number, dir_x, dir_y ):
        temp=self.list_coords[coord_army1[unit_number][0]*20+coord_army1[unit_number][1]]
        if (temp[0]+dir_x>-1 and temp[0]+dir_x<20 and temp[1]+dir_y>-1 and temp[1]+dir_y<11):
            destination=self.list_coords[(coord_army1[unit_number][0]+dir_x)*20+(coord_army1[unit_number][1]+dir_y)]
            if (destination[3]<2 and destination[2]==0):
                self.list_coords[coord_army1[unit_number][0]*20+coord_army1[unit_number][1]][3]=0
                self.list_coords[(coord_army1[unit_number][0]+dir_x)*20+(coord_army1[unit_number][1]-dir_y)][3]=temp[3]
                self.coord_army1[unit_number][0]+=dir_x
                self.coord_army1[unit_number][1]+=dir_y
            else:
                return False
        else:
                return False
            
    def get_army_coords(self,fraction):
        coord_army=[]
        for i in range(20):
            for j in range(11):
                if (self.cells_list[2]>(0+fraction*5)):
                    coord_army[self.cells_list][0]=self.cells_list[0]
                    coord_army[self.cells_list][1]=self.cells_list[1]
        return coord_army
                 
    def bot_1step(self, army1, army2, attacker):
        attacker=1
        alive_list=get_alive(army2)
        no_in_range=0#если ни одного в пределах досягаемости за ход, это - просто чтобы топал
        victim=get_vunerable(attacker,army2)
        victim_chosen=False
        while(victim_chosen == False):
            for i in range('остаток хода'):
                distance_x=self.coord_army1[attacker][0]-self.coord_army2[victim][0]-self.units_list[attacker].get_abil('range',0)
                distance_y=self.coord_army1[attacker][1]-self.coord_army2[victim][1]-self.units_list[attacker].get_abil('range',0)
                if (no_in_range+distanse_x+distance_y<self.units_list[attacker].get_abil('move',0)):#если дотопает за ход
                    victim_chosen=True
                    in_range_by_x=distance_x<=0
                    in_range_by_y=distance_y<=0
                    if (in_range_by_x and in_range_by_y):#если кто-то уже в радиусе атаки
                        kick(army1,army2,atacker,victim+1)#то это его проблемы
                        break
            
                    if (distance_x<abs(self.units_list[attacker].get_abil('range',0))):
                        if (distance_x<0):
                            bot_moving(attacker, -1, 0)  #move left           
                        else:
                            bot_moving(attacker, 1, 0)  #move right
                    else:
                        if (distance_y<abs(self.units_list[attacker].get_abil('range',0))):
                            if (distance_x<0):
                                bot_moving(attacker, 0, -1)      #move up
                            else:
                                bot_moving(attacker, 0, 1)      #move down
                else:
                    false_army=army2
                    false_army[victim]=0
                    if(math.sum(false_army>0)):
                        victim=get_vunerable(attacker,false_army)
                    else:
                        no_in_range=20
                        victim=get_vunerable(attacker,army2)
                        
                        
    def who_wins(self):
        countwarrs1=0
        countwarrs2=0
        for i in range(5):
            countwarrs1+=army1[i]
            countwarrs2+=army1[i]#считаем кол-во войск
        if(countwarrs1>0 and countwarrs2>0):
            return 0
        elif(countwarrs1==0):
            return 1
        else:
            return 2   
    
    def auto_battle(self,army1,army2):
        #coord_army1 = [[1,0],[3,0],[5,0],[7,0],[9,0]]
        #coord_army2 = [[1,20],[3,20],[5,20],[7,20],[9,20]]
        alive_list=get_alive(army1)    
        while(who_wins() == False):
            for i in range(5):
                bot_1step(army1, army2,coord_army1,coord_army2, i)
                if(who_wins()):
                    break
                bot_1step(army2, army1,coord_army2,coord_army1, i)
                if(who_wins()):
                    break
        return (who_wins())
bat=Battle()
#bat.find_strength([0,10,0,0,0,0])
bat.autobattle([0,10,0,0,0,0],[0,0,20,0,0,0])