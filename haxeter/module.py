from random import random, randint
import time

############# Player ###############

class Player:
    def __init__(self, name):
        self.name = name
        self.exp = 0
        self.lv = 1
        self.money = 0
        self.hp = 100
        self.atk = 1
        self.defen = 0
        self.spd = 2

    @staticmethod
    def expRequire(lv):
        return int((lv ** 2)/3+10)

    def presentStatus(self):
        return f"""
 < 스탯입니당 >
이름: {self.name}
레벨: {self.lv} ··· {int(self.exp / Player.expRequire(self.lv) * 1000) / 10}%
돈: {self.money}원
능력치:
 - 체력: {self.hp}
 - 공격력: {self.atk}
 - 방어력: {self.defen}
 - 민첩: {self.spd}         
        """.strip()
    
    def gainExp(self, exp):
        self.exp += exp
        lvDelta = 0
        while self.exp >= Player.expRequire(self.lv+lvDelta):
            self.exp -= Player.expRequire(self.lv)
            lvDelta += 1
        return lvDelta

    @staticmethod
    def statusDelta(lv):
        return { # delta
            'hp': lv * randint(0, 100),
            'atk': lv * randint(0, 10),
            'defen': lv * randint(0, 10),
            'spd': lv * randint(0, 10),
        }
    
    def cridmg(self):
        return self.atk * 1.5



############# HuntManager ##############

class Hunt:
    @staticmethod
    def mlv(name):
        lv = len(name)
        while name.endswith('!'):
            name = name[0:-1]
            lv += 9
        return lv
    
    @staticmethod
    def mhp(lv):
        return int(lv ** 2 / 3 * randint(0, lv+10)) + lv * 10

    @staticmethod    
    def mdmg(lv):
        return lv * randint(0, int(lv + lv/7)) + int(lv ** 2 / 5) + (-2 if lv > 3 else 1)

    @staticmethod
    def mdef(lv):
        return lv * int(randint(0, int(lv / 3)) + lv / 5) + int(lv ** 2 / 5)
    
    @staticmethod
    def turn(monsterLv, userSpd):
        lv = monsterLv
        rate = (((lv * (randint(0, lv) + lv/6)) ** 0.5 + lv) / userSpd ** 0.5) / 2
        rate = 0.35 if rate < 0.35 else 0.65 if rate > 0.65 else rate
        return 'player' if random() > rate else 'monster'

    @staticmethod
    def reward(lv, outOfRange):
        exp = int(lv * random() * 3)
        money = int(lv * random() * 1.5)
        if outOfRange:
            exp = int(exp / 5)+1
            money = int(money / 5)+1
        return {
            'exp': exp,
            'money': money
        }
    
    @staticmethod
    def critical(player):
        return random() > 0.9

    @staticmethod
    def fight(player, monsterName):
        result = []
        died = False
        mlv = Hunt.mlv(monsterName)
        php = player.hp
        mhp = Hunt.mhp(mlv)
        
        result.append(f"""
{mlv} Lv. {monsterName}(이)가 등장해따!
{monsterName}의 체력: {mhp}
""".strip())
        result.append(f'\n------------------< {player.name}의 사냥 결과 >------------------\n')

        while php > 0 and mhp > 0:
            mdmg = Hunt.mdmg(mlv)
            mdef = Hunt.mdef(mlv)
            if Hunt.turn(mlv, player.spd) == "player":
                msg = ""
                if Hunt.critical():
                    msg += "@ 크리티컬!\n"
                    mhp -= player.cridmg()
                else:
                    mhp -= max(0, player.atk - randint(0, mdef))
                    msg += f"@공격이닷!\n > {monsterName}의 남은 체력: {max(0, mhp)}"
                result.append(msg)
            else:
                php -= max(1, mdmg - player.defen)
                result.append(f"{monsterName}: 우워ㅓ어어어!!\n > {player.name}의 남은 체력: {php}")
        
        if mhp < 1:
            reward = Hunt.reward(mlv, abs(mlv - player.lv) > 3)
            player.money += reward['money']
            lvup = player.gainExp(reward['exp'])
            result.append(f"{monsterName}(을)를 쓰러뜨렸다! {reward['exp']}만큼의 경험치랑 {reward['money']}원을 얻어ㅆ다!")
            if lvup > 0:
                up = player.statusDelta(lvup)
                player.hp += up['hp']
                player.atk += up['atk']
                player.defen += up['defen']
                player.spd += up['spd']
            result.append(f'''
 ★ 레벨업! ★
{player.lv-lvup} Lv → {player.lv} Lv
체력이 {up['hp']} 상승!
공격력이 {up['atk']} 상승!
방어력이 {up['defen']} 상승!
민첩이 {up['spd']} 상승!
            '''.strip())

        else:
            result.append('쿠구궁...... 사망하셨습니당.\n 😉 캐릭터가 삭제되었습니당. 처음부터 다시 하세요!')
            died = True

        return {
            'msg': result,
            'died': died
        }


############################3

def reinforce(pay):
    stat = 'hp.hp.hp.hp.hp.atk.atk.defen.defen.spd.spd'.split('.')[randint(0, 11)]
    amount = int(pay * random() * 2 + random() * 3 * pay / 7)
    if stat == "hp":
        amount *= random() * 3 + 1
    return {
        'stat': stat,
        'amount': amount
    }




################# Presenter ###############

class Interface:
    clear = None
    header = None
    footer = None
    tag = None

    @classmethod
    def setClearOutput(self, clear):
        self.clear = clear

    @classmethod
    def setHeader(self, header):
        self.header = header

    @classmethod
    def setFooter(self, footer):
        self.footer = footer

    @classmethod
    def setCmdTag(self, tag):
        self.tag = tag

    @classmethod
    def printHeader(self):
        if self.header != None:
            print(self.header + "\n\n")

    @classmethod
    def printFooter(self):
        if self.footer != None:
            print("\n\n\n" + self.footer)
    
    @classmethod
    def route(self):
        return input('' if self.tag == None else self.tag)
    
    @classmethod
    def present(self, msg):
        self.clear()
        self.printHeader()
        print(msg)
        self.printFooter()
    
    @classmethod
    def presentAll(self, msgList, delay):
        self.clear()
        self.printHeader()
        for msg in msgList:
            time.sleep(delay/1000)
            print(msg)
        self.printFooter()