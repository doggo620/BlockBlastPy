from dis import Positions
from itertools import combinations_with_replacement
from typing import Optional
import copy
#import pygame, random
from pygame import sprite, Surface, draw, surface, SRCALPHA
from random import choice, randint

block_size = 60

class BreakOut(Exception):
  pass

colors = ["red", "green", "pink", "yellow", "orange", "white", "brown"]
blocks = [
    ([[0,1],
      [1,1],
      [1, 0]],2,3),
    ([[1,0],
      [1,1],
      [0,1]],2,3),
    ([[1,1],
      [1,1],
      [1,1]],2,3),
    ([[1,1],
      [1,0],
      [1,0]],2,3),
    ([[1,1],
      [0,1],
      [0,1]],2,3),
    ([[0,1],
      [0,1],
      [1,1]],2,3),
    ([[1,0],
      [1,0],
      [1,1]],2,3),
    ([[1,0],
      [1,1],
      [1,0]],2,3),
    ([[0,1],
      [1,1],
      [0,1]],2,3),
    ([[1,1],
      [1,1]],2,2),
    ([[0,1],
      [1,1]],2,2),
    ([[1,0],
      [1,1]],2,2),
    ([[1,1],
      [1,0]],2,2),
    ([[1,1],
      [0,1]],2,2),
    ([[1,1,1],
      [1,1,1]],3,2),
    ([[1,0,0],
      [1,1,1]],3,2),
    ([[1,1,1],
      [1,0,0]],3,2),
    ([[0,0,1],
      [1,1,1]],3,2),
    ([[1,1,1],
      [0,0,1]],3,2),
    ([[0,1,0],
      [1,1,1]],3,2),
    ([[1,1,1],
      [0,1,0]],3,2),
    ([[1,1,1]],3,1),
    ([[1,1,1,1]],4,1),
    ([[1,1,1,1,1]],5,1),
    ([[1],
      [1],
      [1]],1,3),
    ([[1],
      [1],
      [1],
      [1]],1,4),
    ([[1],
      [1],
      [1],
      [1],
      [1]],1,5),
    ([[1,1,1],
      [1,1,1],
      [1,1,1]],3,3),
    ([[0,0,1],
      [0,0,1],
      [1,1,1]],3,3),
    ([[1,0,0],
      [1,0,0],
      [1,1,1]],3,3),
    ([[1,1,1],
      [1,0,0],
      [1,0,0]],3,3),
    ([[1,1,1],
      [0,0,1],
      [0,0,1]],3,3),
    ([[1]],1,1),
    ([[1,1]],2,1),
    ([[1],
      [1]],1,2),
]

def checkPicked(blocks: list):
    for block in blocks:
        if block.picked == True: return block
    return False

class Block(sprite.Sprite):
    def __init__(self, color, width, height, pickable):
        sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = Surface([block_size, block_size])
        self.image.fill(color)

        self.color = color
        self.picked = False
        self.pickable = pickable
        self.invisible = False
        self.filled = False
        self.clickOffset = (0,0)
        self.oldColor = color
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
    def update(self, x, y):
        self.rect.topleft = (x,y)
    def render(self,screen:surface.Surface):
        screen.blit(self.image, (self.rect.x,self.rect.y))
        if not self.invisible:
          draw.rect(screen, "black", self.rect,1)

class Shape():
  def __init__(self, color,shape:tuple[list[list[int]],int,int]):
    self.shape:tuple[list[list[int]],int,int] = shape
    self.blocks:list[list[Block]] = []
    self.offset = (0,0,0,0)
    self.color = color
    self.origin = (0,0)
    self.picked = False
    for y in range(shape[2]):
      self.blocks.append([])
      for x in range(shape[1]):
        s = Block(color, block_size,block_size, True)
        s.update(x * block_size, y *block_size)
        if shape[0][y][x] == 0:
          s.image = Surface([block_size, block_size], SRCALPHA)
          s.image.fill((0, 0, 0, 0))
          s.invisible = True
        self.blocks[y].append(s)


  def checkClick(self,x,y):
    for iy, yl in enumerate(self.blocks):
      for ix , block in enumerate(yl):
        if block.picked == False and block.rect.collidepoint(x, y):
          self.offset = (x - block.rect.x, y - block.rect.y,ix,iy)
          return True
    return False
  def update(self,x,y):
    for iy, yl in enumerate(self.blocks):
      for ix, block in enumerate(yl):
        block.update(x-((self.offset[2] - ix)* block_size + self.offset[0]),y-((self.offset[3] - iy)* block_size + self.offset[1]))

  def render(self,screen):
    for y in self.blocks:
      for block in y:
        block.render(screen)

class map:
    def __init__(self, size=(8,8)):
        self.size = size
        self.map: list[list[Block]] = []
        for y in range(size[1]):
            self.map.append([])
            for x in range(size[0]):
                self.map[y].append(Block("purple", block_size, block_size, False))

        for y in range(size[1]):
            for x in range(size[0]):
                self.map[y][x].update(x*block_size, y*block_size)

    def render(self,screen):
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.map[x][y].render(screen)
    def print(self):
      for y in self.map:
        for x in y:
          print(x.filled, end=",")
        print()
    def reset(self):
      for y in self.map:
        for x in y:
          x.filled = False
          x.image.fill("purple")

    def resetHover(self):
      for y in range(self.size[1]):
        for x in range(self.size[0]):
          if self.map[x][y].filled == False:
            self.map[x][y].image.fill("purple")
          else:
            self.map[x][y].image.fill(self.map[x][y].oldColor)
            

    def getAvaliable(self, sh:Shape) -> list[tuple[int,int]]:
      av = []
      for iy, y in enumerate(self.map):
        for ix, x in enumerate(y):
          # go back here
          try:
            if x.filled == True: raise BreakOut
            for yi, yRow in enumerate(sh.shape[0]):
              for xi, xRow in enumerate(yRow):
                if xRow == 1:
                  if iy + yi >= self.size[1] or iy + yi < 0: raise BreakOut
                  if ix + xi >= self.size[0] or ix + xi < 0: raise BreakOut
                  if self.map[iy + yi][ix + xi].filled: raise BreakOut
            av.append((ix,iy))
          except BreakOut:
            pass
      return av
    def simulatePlace(self, pos:tuple[int,int], sh:Shape, holdPosY = 0, holdPosX = 0) -> Optional["map"]:
      av = self.getAvaliable(sh)
      if not pos in av: return None

      newMap:map = map(self.size)
      for yi,y in enumerate(newMap.map):
        for xi,x in enumerate(y):
          x.filled = copy.deepcopy(self.map[yi][xi].filled)

      for yi, yRow in enumerate(sh.shape[0]):
        for xi, xRow in enumerate(yRow):
          if xRow == 1:
            newMap.map[pos[1] + yi][pos[0] + xi].filled = True
            newMap.map[pos[1] + yi][pos[0] + xi].image.fill("red")\
            #newMap.map[pos[1] + (yi - holdPosY)][pos[0] + (xi - holdPosX)].filled = True
            #newMap.map[pos[1] + (yi - holdPosY)][pos[0] + (xi - holdPosX)].image.fill("red")
      return newMap

#def mapPlaceCheck(shape:Shape, mapa:map):
#  holdOffSetX, holdOffSetY, holdPosX, holdPosY = shape.offset
#  for iy, y in enumerate(mapa.map):
#    for ix, x in enumerate(y):
#      shapeX, shapeY = shape.blocks[holdPosY][holdPosX].rect.topleft
#      if x.rect.collidepoint(shapeX + holdOffSetX, shapeY + holdOffSetY):
#        x.image.fill("black")

def mapPlaceCheck(xClick,yClick, shape:Shape, mapa:map):
  mapa.resetHover()
  holdOffSetX, holdOffSetY, holdPosX, holdPosY = shape.offset
  for iy, y in enumerate(mapa.map):
    for ix, x in enumerate(y):
      if x.rect.collidepoint(xClick, yClick) and x.filled == False:
        for yi, yRow in enumerate(shape.shape[0]):
          for xi, xRow in enumerate(yRow):
            if xRow == 1:
              if iy + (yi - holdPosY) >= mapa.size[1] or iy + (yi - holdPosY) < 0: return False
              if ix + (xi - holdPosX) >= mapa.size[0] or ix + (xi - holdPosX) < 0: return False
              if mapa.map[iy + (yi - holdPosY)][ix + (xi - holdPosX)].filled: return False
        for yi, yRow in enumerate(shape.shape[0]):
          for xi, xRow in enumerate(yRow):
            if xRow == 1:
              mapa.map[iy + (yi - holdPosY)][ix + (xi - holdPosX)].image.fill("black")
        try:
          newMap = mapa.simulatePlace((ix + (0 - holdPosX),iy + (0 - holdPosY)), shape,holdPosY, holdPosX)
          checkWin(newMap, True, shape.color, mapa)
        except:
          pass
        return True
  return False

def mapPlace(xClick,yClick, shape:Shape, mapa:map):
  mapa.resetHover()
  holdOffSetX, holdOffSetY, holdPosX, holdPosY = shape.offset
  for iy, y in enumerate(mapa.map):
    for ix, x in enumerate(y):
      if x.rect.collidepoint(xClick, yClick) and x.filled == False:
        for yi, yRow in enumerate(shape.shape[0]):
          for xi, xRow in enumerate(yRow):
            if xRow == 1:
              if iy + (yi - holdPosY) >= mapa.size[1] or iy + (yi - holdPosY) < 0: return False
              if ix + (xi - holdPosX) >= mapa.size[0] or ix + (xi - holdPosX) < 0: return False
              if mapa.map[iy + (yi - holdPosY)][ix + (xi - holdPosX)].filled: return False
        for yi, yRow in enumerate(shape.shape[0]):
          for xi, xRow in enumerate(yRow):
            if xRow == 1:
              mapa.map[iy + (yi - holdPosY)][ix + (xi - holdPosX)].filled = True
              mapa.map[iy + (yi - holdPosY)][ix + (xi - holdPosX)].oldColor = shape.color
              mapa.map[iy + (yi - holdPosY)][ix + (xi - holdPosX)].image.fill(shape.color)
        return True
  return False

def mapPlaceAuto(xClick,yClick, ix,iy, shape:Shape, mapa:map):
  mapa.resetHover()
  #for iy, y in enumerate(mapa.map):
    #for ix, x in enumerate(y):
  for yi, yRow in enumerate(shape.shape[0]):
    for xi, xRow in enumerate(yRow):
      if xRow == 1:
        if iy + yi >= mapa.size[1] or iy + yi < 0: return False
        if ix + xi >= mapa.size[0] or ix + xi < 0: return False
        if mapa.map[iy + yi][ix + xi].filled: return False
  for yi, yRow in enumerate(shape.shape[0]):
    for xi, xRow in enumerate(yRow):
      if xRow == 1:
        mapa.map[iy + yi][ix + xi].filled = True
        mapa.map[iy + yi][ix + xi].image.fill(shape.color)
  return True

def checkWin(mapa:map, check:bool = False, checkcolor="black", checkmap = None):
  #check y wins
  score = 0
  yWins = []
  xWins = []
  #for yi,y in enumerate(mapa.map):
  #  if all(y[x].filled for x in range(len(y))):
  #    yWins.append(y)
  for y in range(len(mapa.map)):
    if all(mapa.map[y][x].filled for x in range(len(mapa.map[0]))):
      yWins.append(y)
  
  
  for x in range(len(mapa.map[0])):
    if all(mapa.map[y][x].filled for y in range(len(mapa.map))):
      xWins.append(x)

  #for y in yWins:
  #  score +=100* len(yWins) + randint(1,99)
  #  for x in range(len(y)):
  #    if not check:
  #      y[x].filled = False
  #      y[x].image.fill("purple")
  #    else:
  #      checkmap.map[y][x].image.fill(checkcolor)
  
  for y in yWins:
    score +=100 * len(yWins) + randint(1,99)
    for x in range(len(mapa.map[0])):
      if not check:
        mapa.map[y][x].filled = False
        mapa.map[y][x].image.fill("purple")
      else:
        checkmap.map[y][x].image.fill(checkcolor)
      
  for x in xWins:
    score +=100 * len(xWins) + randint(1,99)
    for y in range(len(mapa.map)):
      if not check:
        mapa.map[y][x].filled = False
        mapa.map[y][x].image.fill("purple")
      else:
        checkmap.map[y][x].image.fill(checkcolor)
  return score

def checkPossibility(mapa:map, bList: list[Shape]):
  #TODO:
  #fix score  score = 0
  score = 0
  positions = []
  try:
    if bList == []: raise BreakOut
    for shape1 in bList:
      shape1Avaliability = mapa.getAvaliable(shape1)
      if shape1Avaliability == []: continue
      for possibleMove1 in shape1Avaliability:
        map2 = mapa.simulatePlace(possibleMove1, shape1)
        checkWin(map2)
        bList2 = bList.copy()
        bList2.remove(shape1)
        if bList2 == []:
          positions.append((shape1, possibleMove1))
          score = checkWin(map2)
          raise BreakOut
        for shape2 in bList2:
          shape2Avaliability = map2.getAvaliable(shape2)
          if shape2Avaliability == []: continue
          for possibleMove2 in shape2Avaliability:
            map3 = map2.simulatePlace(possibleMove2, shape2)
            checkWin(map3)
            bList3 = bList2.copy()
            bList3.remove(shape2)
            if bList3 == []:
              positions.append((shape1, possibleMove1))
              positions.append((shape2,possibleMove2))
              score = checkWin(map2) + checkWin(map3)
              raise BreakOut
            for shape3 in bList3:
              shape3Avaliability = map3.getAvaliable(shape3)
              if shape3Avaliability == []: continue
              positions.append((shape1, possibleMove1))
              positions.append((shape2,possibleMove2))
              positions.append((shape3,shape3Avaliability[0]))
              score = checkWin(map2) + checkWin(map3)
              raise BreakOut

  except BreakOut:
    return (True, positions, score)
  return (False, positions, score)

def genBlocks(mapa:map) -> list[Shape]:
  blocksNew = []
  running = True
  while running:
    blocksNew = []
    for i in range(3):
      s = Shape(choice(colors), choice(blocks))
      #s.update(50 + block_size * 4 * i, 50 + block_size * mapa.size[1])
      #s.origin = (50 + block_size * 4 * i, 50 + block_size * mapa.size[1])
      blocksNew.append(s)
    running = not checkPossibility(mapa, blocksNew)[0]
    i = 0
  for s in blocksNew:
    s.update(50 + block_size * 4 * i, 50 + block_size * mapa.size[1])
    s.origin = (50 + block_size * 4 * i, 50 + block_size * mapa.size[1])
    i +=1
  return blocksNew
#def checkPossibility(mapa: map, bList: list[Shape]) -> bool:
  #try:
  #  for shape1 in bList:
  #    shape1Avaliability = mapa.getAvaliable(shape1)
  #    if shape1Avaliability == []: continue
  #    for possibleMove1 in shape1Avaliability:
  #      map2 = mapa.simulatePlace(possibleMove1, shape1)
  #      bList2 = copy.deepcopy(bList)
  #      bList2.remove(shape1)
  #      for shape2 in bList2:
  #        shape2Avaliability = map2.getAvaliable(shape2)
  #        if shape2Avaliability == []: continue
  #        for possibleMove2 in shape2Avaliability:
  #          map3 = map2.simulatePlace(possibleMove2, shape2)
 #           bList3 = copy.deepcopy(bList2)
#            bList3.remove(shape2)
#            for shape3 in bList3:
#              shape3Avaliability = map3.getAvaliable(shape3)
#              if shape3Avaliability == []: continue
#              raise BreakOut
#
 # except BreakOut:
 #   return True
#  return False
#