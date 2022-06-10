import numpy as np
import random

class Buffer():
    def __init__(self,max_len):
        self.memory = []# spacials, non_spacials, act_dis, win_rate
        self.max_len = max_len


    def add_to_buffer(self,new_memory):
        game_array, opponent_array, act_dis  = new_memory[0],new_memory[1],new_memory[2]
        if len(self.memory) > self.max_len:
            keep_this = self.max_len - game_array.shape[0]
            self.memory = self.memory[-keep_this:]
        # self.memory = np.concatenate((self.memory,newMemory),axis=0)
        for i in range(game_array.shape[0]):
            self.memory.append((game_array[i],opponent_array[i],act_dis[i]))
        print('size of buffer: ',len(self.memory))


    def get_from_buffer(self,len):
        batch = random.choices(self.memory,k=len)
        game_array = np.array([i[0] for i in batch])
        opponent_array = np.array([i[1] for i in batch])
        act_dis  = np.array([i[2] for i in batch])

        print('got from buffer game arrays: ',game_array.shape)
        print('got from buffer opponent arrays: ',opponent_array.shape)
        return game_array,opponent_array,act_dis

    def set_len(self, new_len):
        self.max_len = new_len