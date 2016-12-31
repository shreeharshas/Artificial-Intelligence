# Automatic Zacate game player
# B551 Fall 2015
# Shree Harsha Sridharamurthy sridhash@iu.edu
#
# Based on skeleton code by D. Crandall
#
# Given:
# 5 fair dice thrown at the same time
# 13 rules with different or similar scores based on their conditions
# 3 rolls per turn - 3rd roll to return the category of choice made
# 13 rounds/turns per game
# 100 games played totally
# Each rule/category is to be applied only once per a game of 13 turns
#
# To find:
# The maximum value for the average score of all the 100 games played based on the rules
#
# Approach:
# Given skeletal code randomly chose a category and used its score to calculate the result
#
# The new AutoPlayer tries to obtain the maximum score based on the probable outcomes and scores of the 13 rules
#
# Principle:
# Given 3 rolls, we first try to obtain a roll which gives maximum score - the quintupulo, otherwise pupusa de queso or elote and so on
# The idea is to obtain the maximum score possible of a given turn
# I have classified the rules into 4 classes based on the decreasing order of their possible maximum scores, average scores, minimum score, probability factor
# It was easier to place the analysis in a tabular format - please refer to the attached excel worksheet by the name "WORK.xlsx" for a detailed analysis
#
# This is very similar to the puzzle of obtaining a $100 bill value with those bills of lesser value such as $20 $5 and coins - we first try to find out
#       the number of bills with the maximum value and then proceed to further. The only difference is that, we do not know how which bill can be picked
#
# Approach:
# After the first roll, i check for class1 rules, the possibility of class1 rules, and class2 rules
# I check for other rules only in the subsequent rolls as the chances of the class1 rules become lesser
# Finally, if no required higher class rules are possible, i pick the category with the highest possible score in the third turn and return it


from ZacateState import Dice
from ZacateState import Scorecard
import copy
import operator

class ZacateAutoPlayer:
    def __init__(self):
        self.rulesChances = { "quintupulo":0, "pupusa de queso":0, "elote":0, "seises":0, "triple":0, "cuadruple":0, "pupusa de frijol":0, "cincos":0, "cuatros":0, "treses":0, "doses":0, "unos":0 }
        pass

    def setRulesChances(self, dice, counts):
        #must be > 3 in first round and > 4 in the second
        self.rulesChances["quintupulo"] = max(counts)
        self.rulesChances["pupusa de queso"] = 5 if (sorted(dice.dice) == [1,2,3,4,5] or sorted(dice.dice) == [2,3,4,5,6]) else 4 if (((1 not in dice.dice) and (2 in dice.dice) and (3 in dice.dice) and (4 in dice.dice) and (5 in dice.dice) and (6 in dice.dice))or((1 in dice.dice) and (2 in dice.dice) and (3 in dice.dice) and (4 in dice.dice) and (5 in dice.dice) and (6 not in dice.dice))) else 3 if (1 not in dice.dice) and (2 in dice.dice) and (3 in dice.dice) and (4 in dice.dice) and (5 in dice.dice) and (6 not in dice.dice) else 2
        self.rulesChances["elote"] = 5 if (2 in counts) and (3 in counts) else (4 if (3 in counts) and (2 not in counts) else 3 if (2 in counts) and (3 not in counts) else 2)

        #must be > 3 in first round and > 4 in the second
        #self.rulesChances["seises"] = counts[6]
        self.rulesChances["triple"] = 5 if max(counts) >= 3 else 4 if max(counts) >= 2 else 3
        self.rulesChances["cuadruple"] = 5 if max(counts) >= 4 else 4 if max(counts) >= 3 else 3 if max(counts) >= 2 else 2
        self.rulesChances["pupusa de frijol"] = 5 if (len(set([1,2,3,4]) - set(dice.dice)) == 0 or len(set([2,3,4,5]) - set(dice.dice)) == 0 or len(set([3,4,5,6]) - set(dice.dice)) == 0) else 4 if ((len(set([1,2,3]) - set(dice.dice)) == 0 or len(set([2,3,4]) - set(dice.dice)) == 0 or len(set([3,4,5]) - set(dice.dice)) == 0) or len(set([4,5,6]) - set(dice.dice)) == 0 or len(set([1,2,4]) - set(dice.dice)) == 0 or len(set([1,2,5]) - set(dice.dice)) == 0 or len(set([1,2,6]) - set(dice.dice)) == 0 or len(set([2,3,5]) - set(dice.dice)) == 0 or len(set([2,3,6]) - set(dice.dice)) == 0 or len(set([3,4,6]) - set(dice.dice)) == 0) else 3 if ((len(set([1,2]) - set(dice.dice)) == 0 or len(set([1,3]) - set(dice.dice)) == 0 or len(set([1,4]) - set(dice.dice)) == 0) or len(set([1,5]) - set(dice.dice)) == 0 or len(set([1,6]) - set(dice.dice)) == 0 or len(set([2,3]) - set(dice.dice)) == 0 or len(set([2,4]) - set(dice.dice)) == 0 or len(set([2,5]) - set(dice.dice)) == 0 or len(set([2,6]) - set(dice.dice)) == 0 or len(set([3,4]) - set(dice.dice)) == 0 or len(set([3,5]) - set(dice.dice)) == 0 or len(set([3,6]) - set(dice.dice)) == 0 or len(set([4,5]) - set(dice.dice)) == 0 or len(set([4,6]) - set(dice.dice)) == 0 or len(set([5,6]) - set(dice.dice)) == 0) else 2

        #must be > its corresponding count score
        self.rulesChances["seises"] = dice.dice.count(6)
        self.rulesChances["cincos"] = dice.dice.count(5)
        self.rulesChances["cuatros"] = dice.dice.count(4)
        self.rulesChances["treses"] = dice.dice.count(3)
        self.rulesChances["doses"] = dice.dice.count(2)
        self.rulesChances["unos"] = dice.dice.count(1)

        #chances of tamal is 100% so omit its calculation here

    def findRemainaingQuinDice(self, dice, maxCount):
        arr = []
        if maxCount == 5:
            return []
        elif maxCount == 4 or maxCount == 3:
            m = max(dice.dice)
            for i in range(0, len(dice.dice)):
                if dice.dice[i] != m:
                    arr.append(i)
            return arr
        else:
            return [0,1,2,3,4]

    def findRemainaingPupQDice(self, dice, maxCount):
        arr = sorted(dice.dice)
        retArr = []

        count2 = 0
        count3 = 0
        count4 = 0
        count5 = 0

        if 1 not in dice.dice and 2 in dice.dice and 3 in dice.dice and 4 in dice.dice and 5 in dice.dice and 6 not in dice.dice:
            for i in range(0, 5):
                if dice.dice[i] == 2:
                    count2 += 1
                    if count2 == 2:
                        retArr.append(i)

                if dice.dice[i] == 3:
                    count3 += 1
                    if count3 == 2:
                        retArr.append(i)

                if dice.dice[i] == 4:
                    count4 += 1
                    if count4 == 2:
                        retArr.append(i)

                if dice.dice[i] == 5:
                    count5 += 1
                    if count5 == 2:
                        retArr.append(i)

            return  retArr
        else:
            return [0,1,2,3,4]

    def findRemainaingPupFDice(self, dice, maxChance):
        arr = sorted(dice.dice)
        retArr = []
        if maxChance == 5:
            return []
        else:
            return [0,1,2,3,4]

    def getNumberToCheck(self, counts):
        m = max(counts)
        for x in range(0,len(counts)):
            if counts[x] == m:
                return x+1

    def findRemainaingEloteDice(self, dice, maxChance, counts):
        arr = []
        if maxChance == 5:
            return []
        elif maxChance == 4 or maxChance == 3:
            m = self.getNumberToCheck(counts)
            counter = 0
            for i in range(0, len(dice.dice)):
                if dice.dice[i] != m:
                    counter += 1
                    arr.append(i)
            if counter>0:
                return arr
            else:
                return [0,1,2,3,4]
        else:
            return [0,1,2,3,4]

    def findRemainaingTripleDice(self, dice, maxChance, counts):
        return self.findRemainaingEloteDice(dice, maxChance, counts)

    def findRemainaingCuadDice(self, dice, maxChance, counts):
        return self.findRemainaingEloteDice(dice, maxChance, counts)

    def findRemainingNumberDice(self, dice, maxChance, number):
        retArry = []
        for i in dice.dice:
            if dice.dice[i] != number:
                retArry.append(i)
        return retArry

    def bestOfRemaining(self, dice, scorecard):
        tempScorecard = Scorecard()
        tempScorecard.scorecard = scorecard.scorecard.copy()
        tempScorecard.Categories = copy.deepcopy(scorecard.Categories)
        tempScorecard.Numbers = scorecard.Numbers.copy()
        scores = { "unos" : 0, "doses" : 0, "treses" : 0, "cuatros" : 0, "cincos" : 0, "seises" : 0, "pupusa de queso" : 0, "pupusa de frijol" : 0, "elote" : 0, "triple" : 0, "cuadruple" : 0, "quintupulo" : 0, "tamal" : 0 }

        flagOK = False
        for i in scores:
            if i not in tempScorecard.scorecard:
                tempScorecard.record(i, dice)
                if scores[i]==0:
                    scores[i] = tempScorecard.scorecard[i]

        maxScore = max(scores.values())
        if len(scores)>0:
            for key, val in scores.items():
                if val == maxScore:
                    return key

        """for x in scores:
            if scores[x] == maxScore:
                flagOK = True
                return scores.keys(x)"""

        if flagOK == False:
            return ""

    def first_roll(self, dice, scorecard):
        counts = [dice.dice.count(i) for i in range(1,7)]
        self.setRulesChances(dice, counts)

        if "quintupulo" not in scorecard.scorecard or "pupusa de queso" not in scorecard.scorecard or "elote" not in scorecard.scorecard:
            if self.rulesChances["quintupulo"] == 5 or self.rulesChances["pupusa de queso"] == 5 or self.rulesChances["elote"]==5:
                return []

            elif self.rulesChances["quintupulo"] >= 3:
                return self.findRemainaingQuinDice(dice, self.rulesChances["quintupulo"])

            elif self.rulesChances["pupusa de queso"] >= 3:
                return self.findRemainaingPupQDice(dice, self.rulesChances["pupusa de queso"])

            elif self.rulesChances["elote"]:
                return self.findRemainaingEloteDice(dice, self.rulesChances["elote"], counts)

        if "seises" not in scorecard.scorecard or "triple" not in scorecard.scorecard or "cuadruple" not in scorecard.scorecard or "pupusa de frijol" not in scorecard.scorecard:
            if self.rulesChances["seises"] == 5 or self.rulesChances["triple"] == 5 or self.rulesChances["cuadruple"] == 5 or self.rulesChances["pupusa de frijol"]==5:
                return []

            elif self.rulesChances["seises"] >=3:
                return self.findRemainingNumberDice(dice, self.rulesChances["seises"], 6)

            elif self.rulesChances["triple"] >=3:
                return self.findRemainaingTripleDice(dice, self.rulesChances["triple"], counts)

            elif self.rulesChances["cuadruple"] >= 3:
                return self.findRemainaingCuadDice(dice, self.rulesChances["cuadruple"], counts)

            elif self.rulesChances["pupusa de frijol"] >= 3:
                return self.findRemainaingPupFDice(dice, self.rulesChances["pupusa de frijol"])

        return [0,1,2,3,4] #if none match

    def second_roll(self, dice, scorecard):
        counts = [dice.dice.count(i) for i in range(1,7)]
        self.setRulesChances(dice, counts)

        if "quintupulo" not in scorecard.scorecard or "pupusa de queso" not in scorecard.scorecard or "elote" not in scorecard.scorecard:
            if self.rulesChances["quintupulo"] == 5 or self.rulesChances["pupusa de queso"] == 5 or self.rulesChances["elote"]==5:
                return []
            elif self.rulesChances["quintupulo"] ==4:
                return self.findRemainaingQuinDice(dice, self.rulesChances["quintupulo"])

            elif self.rulesChances["pupusa de queso"] ==4:
                return self.findRemainaingPupQDice(dice, self.rulesChances["pupusa de queso"])

            elif self.rulesChances["elote"] ==4:
                return self.findRemainaingEloteDice(dice, self.rulesChances["elote"], counts)

        if "seises" not in scorecard.scorecard or "triple" not in scorecard.scorecard or "cuadruple" not in scorecard.scorecard or "pupusa de frijol" not in scorecard.scorecard:
            if self.rulesChances["seises"] == 5 or self.rulesChances["triple"] == 5 or self.rulesChances["cuadruple"] == 5 or self.rulesChances["pupusa de frijol"]==5:
                return []
            elif self.rulesChances["seises"] ==4:
                return self.findRemainingNumberDice(dice, self.rulesChances["seises"], 6)

            elif self.rulesChances["triple"] ==4:
                return self.findRemainaingTripleDice(dice, self.rulesChances["triple"], counts)

            elif self.rulesChances["cuadruple"] ==4:
                return self.findRemainaingCuadDice(dice, self.rulesChances["cuadruple"], counts)

            elif self.rulesChances["pupusa de frijol"] ==4:
                return self.findRemainaingPupFDice(dice, self.rulesChances["pupusa de frijol"])

        if "cincos" not in scorecard.scorecard or "cuatros" not in scorecard.scorecard or "treses" not in scorecard.scorecard or "doses" not in scorecard.scorecard or "unos" not in scorecard.scorecard:
            if self.rulesChances["seises"] == 5 or self.rulesChances["triple"] == 5 or self.rulesChances["cuadruple"] == 5 or self.rulesChances["pupusa de frijol"]==5:
                return []

            elif self.rulesChances["seises"] ==4:
                return self.findRemainingNumberDice(dice, self.rulesChances["seises"], 6)

            elif self.rulesChances["triple"] ==4:
                return self.findRemainaingTripleDice(dice, self.rulesChances["triple"], counts)

            elif self.rulesChances["cuadruple"] ==4:
                return self.findRemainaingCuadDice(dice, self.rulesChances["cuadruple"], counts)

            elif self.rulesChances["pupusa de frijol"] ==4:
                return self.findRemainaingPupFDice(dice, self.rulesChances["pupusa de frijol"])

        return [0,1,2,3,4] #if none match

    def sendMaxtoMin(self, dice, scorecard, num):
        if "quintupulo" not in scorecard.scorecard and self.rulesChances["quintupulo"] == num:
            return "quintupulo"
        elif "pupusa de queso" not in scorecard.scorecard and self.rulesChances["pupusa de queso"] == num:
            return "pupusa de queso"
        elif "elote"  not in scorecard.scorecard and self.rulesChances["elote"] == num:
            return "elote"
        elif "seises" not in scorecard.scorecard and self.rulesChances["seises"] == num:
            return "seises"
        elif "triple" not in scorecard.scorecard and self.rulesChances["triple"] == num:
            return "triple"
        elif "cuadruple" not in scorecard.scorecard and self.rulesChances["cuadruple"] == num:
            return "cuadruple"
        elif "pupusa de frijol" not in scorecard.scorecard and self.rulesChances["pupusa de frijol"] == num:
            return "pupusa de frijol"
        #return the one category with max of numbers score
        elif "cincos" not in scorecard.scorecard and self.rulesChances["cincos"] == num:
            return "cincos"
        elif "cuatros" not in scorecard.scorecard and self.rulesChances["cuatros"] == num:
            return "cuatros"
        elif "treses"  not in scorecard.scorecard and self.rulesChances["treses"] == num:
            return "treses"
        elif "doses" not in scorecard.scorecard and self.rulesChances["doses"] == num:
            return "doses"
        elif "unos" not in scorecard.scorecard and self.rulesChances["unos"] == num:
            return "unos"
        else:
           # return self.bestOfRemaining(dice, scorecard)
            return "null"

    def getScore(self, category, dice, scorecard):
        tempScorecard = Scorecard()
        tempScorecard.scorecard = scorecard.scorecard.copy()
        tempScorecard.Categories = copy.deepcopy(scorecard.Categories)
        tempScorecard.Numbers = scorecard.Numbers.copy()

        tempScorecard.record(category,dice)
        return tempScorecard.scorecard[category]


    def getBestScoreCategory(self, CategoryArray, dice, scorecard):
        scoreCategories = {}
        for categoryToCheck in CategoryArray:
            scoreCategories[categoryToCheck] = self.getScore(categoryToCheck, dice, scorecard)

        maxScore = max(scoreCategories.values())
        if len(scoreCategories)>0:
            for key, val in scoreCategories.items():
                if val == maxScore:
                    return key


    def third_roll(self, dice, scorecard):
        counts = [dice.dice.count(i) for i in range(1,7)]
        self.setRulesChances(dice, counts)
        retCategory = []

        for i in range(6, 0, -1):
            temp = self.sendMaxtoMin(dice, scorecard, i)
            if temp!= "null" and temp not in retCategory:
                retCategory.append(temp)

        if len(retCategory)>1:
            return self.getBestScoreCategory(retCategory, dice, scorecard)

        return retCategory[0] if len(retCategory)> 0 else self.bestOfRemaining(dice, scorecard)




        #return random.choice(list(set(Scorecard.Categories) - set(scorecard.scorecard.keys())))