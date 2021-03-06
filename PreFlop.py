# -*- coding: utf-8 -*-
"""
Created on Wed May 25 18:46:26 2022

@author: NatBr
"""

actions = {
    "i":2
    }

RangeRFI = {
    "UTG":10,
    "UTG+1":14,
    "UTG+2":16,
    "LJ":18,
    "HJ":21,
    "CO":27,
    "button":51,
    ("sb","call"):"KK+,22-77,A2s-A9s,K2s-KTs,Q2s-QTs,J5s+,T6s+,96s+,86s+,75s+,64s+,54s,32s,AKo,A2o-A9o,K5o-KTo,Q6o+,J7o+,T7o+,97o+,87o,76o,65o",
    ("sb","raise"):"88-QQ,ATs+,KJs+,QJs,J2s-J4s,T4s-T5s,94s-95s,84s-85s,74s,63s,53s,43s,ATo-AQo,KJo+,K2o-K3o,Q2o-Q5o,J6o,T6o,96o,86o",
    ("bb","UTG","call"):"22-JJ,A2s-AJs,K5s+,Q7s+,J7s+,T7s+,96s+,87s,ATo+,KTo+,QTo+,JTo",
    ("bb","UTG","raise"):"QQ+,AQs+,86s,75s+,64s+,54s,43s",
    ("bb","UTG+1","call"):"22-JJ,A2s-AJs,K5s+,Q7s+,J7s+,T7s+,96s+,87s,ATo+,KTo+,QTo+,JTo",
    ("bb","UTG+1","raise"):"QQ+,AQs+,86s,75s+,64s+,54s,43s",  
    ("bb","UTG+2","call"):"22-TT,A2s-AJs,K4s+,Q6s+,J6s+,T6s+,96s+,87s,ATo-AQo,KTo+,QTo+,JTo",
    ("bb","UTG+2","raise"):"JJ+,AQs+,85s-86s,74s+,64s+,53s+,43s,AKo",
    ("bb","LJ","call"):"22-99,A2s-ATs,K2s-KJs,Q4s+,J5s+,T5s+,95s+,86s+,76s,ATo-AQo,KTo+,QTo+,JTo",
    ("bb","LJ","raise"):"TT+,AQs+,85s,74s-75s,64s+,53s+,43s,AKo,A9o",
    ("bb","HJ","call"):"22-99,A2s-ATs,K2s-KJs,Q2s+,J5s+,T5s+,95s+,86s+,ATo-AJo,KTo+,QTo+,JTo",
    ("bb","HJ","raise"):"TT+,AJs+,KQs,85s,74s+,63s+,53s+,43s,32s,AQo+,A9o",  
    ("bb","CO","call"):"22-99,A2s-A9s,K2s-KTs,Q2s-QTs,J4s+,T4s+,94s+,86s+,A8o-ATo,A5o,K9o-KJo,Q9o+,J9o+,T9o,98o",
    ("bb","CO","raise"):"TT+,ATs+,KJs+,84s-85s,73s+,63s+,52s+,42s,32s,AJo+,A3o-A4o,KQo",  
    ("bb","button","call"):"22-88,A2s-A9s,K2s-K9s,Q2s-Q9s,J2s-J9s,T2s+,92s+,82s+,72s,62s,A4o-ATo,K6o-KJo,Q7o+,J6o+,T6o+,96o+,86o+,76o",
    ("bb","button","raise"):"99+,ATs+,KTs+,QTs+,JTs,73s+,63s+,52s+,42s+,32s,AJo+,A2o-A3o,KQo,K2o-K5o,Q5o-Q6o,75o,65o",    
    ("bb","sb","call"):"22-88,A2s-A9s,K2s-K9s,Q2s-Q9s,J2s-J8s,T2s-T7s,92s-97s,82s-86s,72s-75s,62s-64s,52s-53s,42s+,32s,A3o-ATo,K4o-KJo,Q5o+,J6o+,T6o+,96o+,86o+",
    ("bb","sb","raise"):"99+,ATs+,KTs+,QTs+,J9s+,T8s+,98s,87s,76s,65s,54s,AJo+,A2o,KQo,K2o-K3o,Q2o-Q4o,J5o,T5o,75o+,64o+,54o"
    }

RangeFacingRFI ={
    ("UTG+1","UTG","call"):"88-JJ,AJs-AQs,KQs,QJs,JTs",
    ("UTG+1","UTG","raise"):"QQ+,AKs,ATs,KJs,AQo+",
    ("UTG+2","UTG", "call"):"88-JJ,AJs-AQs,KQs,QJs,JTs",
    ("UTG+2","UTG", "raise"):"QQ+,AKs,ATs,KJs,AQo+",
    ("UTG+2","UTG+1", "call"):"88-JJ,AJs-AQs,KQs,QJs,JTs",
    ("UTG+2","UTG+1", "raise"):"QQ+,AKs,ATs,KJs,AQo+",
    ("LJ","UTG","call"):"77-JJ,AJs-AQs,KQs,QJs,JTs",
    ("LJ","UTG","raise"):"QQ+,AKs,ATs,A5s,KJs,AQo+",
    ("LJ","UTG+1","call"):"77-JJ,AJs-AQs,KQs,QJs,JTs,T9s",
    ("LJ","UTG+1","raise"):"QQ+,AKs,ATs,A5s,KJs,AQo+",      
    ("LJ","UTG+2","call"):"66-JJ,AJs-AQs,KQs,QJs,JTs,T9s",
    ("LJ","UTG+2","raise"):"QQ+,AKs,ATs,A5s,KJs,98s,87s,AQo+",
    ("HJ","UTG","call"):"77-JJ,AJs-AQs,KQs,QJs,JTs,T9s",
    ("HJ","UTG","raise"):"QQ+,AKs,ATs,A5s,KJs,AQo+",
    ("HJ","UTG+1","call"):"66-JJ,AJs-AQs,KQs,QJs,JTs,T9s,98s",
    ("HJ","UTG+1","raise"):"QQ+,AKs,ATs,A5s,KJs,AQo+",
    ("HJ","UTG+2","call"):"55-JJ,AJs-AQs,KQs,QJs,JTs,T9s,98s",
    ("HJ","UTG+2","raise"):"QQ+,AKs,ATs,A3s-A5s,KJs,87s,76s,AQo+",
    ("HJ","LJ","call"):"55-JJ,ATs,KTs-KJs,QTs+,JTs,T9s,98s,87s",
    ("HJ","LJ","raise"):"QQ+,ATs+,A2s-A5s,KQs,76s,65s,ATo+,KQo",
    ("CO","UTG","call"):"66-JJ,ATs-AJs,KTs+,QTs+,JTs,T9s,98s",
    ("CO","UTG","raise"):"QQ+,AQs+,A4s-A5s,AJo+",
    ("CO","UTG+1","call"):"66-JJ,ATs-AJs,KTs+,QTs+,JTs,T9s,98s",
    ("CO","UTG+1","raise"):"QQ+,AQs+,A4s-A5s,AJo+",
    ("CO","UTG+2","call"):"55-JJ,ATs-AJs,KTs+,QTs+,JTs,T9s,98s",
    ("CO","UTG+2","raise"):"QQ+,AQs+,A2s-A5s,87s,76s,AJo+",
    ("CO","LJ","call"):"44-JJ,ATs,KTs-KJs,QTs+,JTs,T9s,98s",
    ("CO","LJ","raise"):"QQ+,AJs+,A2s-A5s,KQs,87s,76s,65s,54s,AJo+,KQo",
    ("CO","HJ","call"):"44-JJ,ATs,KTs-KJs,QTs+,JTs,T9s,98s,87s",
    ("CO","HJ","raise"):"QQ+,AJs+,A2s-A9s,KQs,K9s,Q9s,J9s,76s,65s,54s,AJo+,KQo",
    ("button","UTG","call"):"22-JJ,ATs-AQs,KTs+,QTs+,JTs,T9s,98s,87s",
    ("button","UTG","raise"):"QQ+,AKs,A4s-A5s,76s,AJo+,KQo",
    ("button","UTG+1","call"):"22-JJ,ATs-AQs,KTs+,QTs+,J9s+,T9s,98s,87s,76s",
    ("button","UTG+1","raise"):"QQ+,AKs,A2s-A5s,76s,AJo+,KQo",
    ("button","UTG+2","call"):"22-JJ,ATs-AQs,KTs+,QTs+,J9s+,T9s,98s,87s,76s",
    ("button","UTG+2","raise"):"QQ+,AQs+,A9s,A2s-A5s,65s,54s,AQo+,ATo,KJo",
    ("button","LJ","call"):"22-JJ,A9s-AJs,KTs+,QTs+,J9s+,T9s,98s,87s,76s,AJo,KQo",
    ("button","LJ","raise"):"QQ+,AQs+,A2s-A8s,65s,54s,AQo+,ATo,KJo",
    ("button","HJ","call"):"22-JJ,A9s-ATs,K9s+,Q9s+,J9s+,T8s+,97s+,87s,76s,AJo,KQo",
    ("button","HJ","raise"):"QQ+,AJs+,A2s-A8s,75s,65s,54s,AQo+,ATo,KJo",
    ("button","CO","call"):"22-JJ,A9s-ATs,A4s-A5s,K9s+,Q9s+,J9s+,T8s+,97s+,87s,76s,ATo-AJo,KJo+",
    ("button","CO","raise"):"QQ+,AJs+,A6s-A8s,A2s-A3s,K8s,Q8s,J8s,86s,75s,64s+,54s,43s,AQo+,A9o,KTo,QJo",
    ("sb","UTG","call"):"77-JJ,ATs-AQs,KJs+,QJs,JTs,T9s,AQo+",
    ("sb","UTG","raise"):"QQ+,AKs,A5s,98s,87s",
    ("sb","UTG+1","call"):"77-JJ,ATs-AQs,KJs+,QJs,JTs,T9s,AQo+",
    ("sb","UTG+1","raise"):"QQ+,AKs,A5s,98s,87s",
    ("sb","UTG+2","call"):"66-JJ,ATs-AQs,KTs+,QTs+,JTs,T9s,98s,AQo+",
    ("sb","UTG+2","raise"):"QQ+,AKs,A5s,87s,76s",
    ("sb","LJ","call"):"55-JJ,ATs-AJs,KTs+,QTs+,JTs,T9s,98s,AQo",
    ("sb","LJ","raise"):"QQ+,AQs+,A4s-A5s,87s,76s,AKo,AJo",
    ("sb","HJ","call"):"44-JJ,ATs-AJs,KTs+,QTs+,JTs,T9s,98s,87s,AQo",
    ("sb","HJ","raise"):"QQ+,AQs+,A9s,A3s-A5s,76s,65s,54s,AKo,AJo",
    ("sb","CO","call"):"",
    ("sb","CO","raise"):"44+,A2s+,K9s+,Q9s+,J9s+,T9s,98s,87s,76s,65s,54s,AJo+,KQo",
    ("sb","button","call"):"",
    ("sb","button","raise"):"22+,A2s+,K9s+,Q9s+,J9s+,T8s+,97s+,86s+,76s,65s,54s,ATo+,KJo+,QJo",
    ("bb","UTG","call"):"22-JJ,A2s-AJs,K5s+,Q7s+,J7s+,T7s+,96s+,87s,ATo+,KTo+,QTo+,JTo",
    ("bb","UTG","raise"):"QQ+,AQs+,86s,75s+,64s+,54s,43s",
    ("bb","UTG+1","call"):"22-JJ,A2s-AJs,K5s+,Q7s+,J7s+,T7s+,96s+,87s,ATo+,KTo+,QTo+,JTo",
    ("bb","UTG+1","raise"):"QQ+,AQs+,86s,75s+,64s+,54s,43s",  
    ("bb","UTG+2","call"):"22-TT,A2s-AJs,K4s+,Q6s+,J6s+,T6s+,96s+,87s,ATo-AQo,KTo+,QTo+,JTo",
    ("bb","UTG+2","raise"):"JJ+,AQs+,85s-86s,74s+,64s+,53s+,43s,AKo",
    ("bb","LJ","call"):"22-99,A2s-ATs,K2s-KJs,Q4s+,J5s+,T5s+,95s+,86s+,76s,ATo-AQo,KTo+,QTo+,JTo",
    ("bb","LJ","raise"):"TT+,AQs+,85s,74s-75s,64s+,53s+,43s,AKo,A9o",
    ("bb","HJ","call"):"22-99,A2s-ATs,K2s-KJs,Q2s+,J5s+,T5s+,95s+,86s+,ATo-AJo,KTo+,QTo+,JTo",
    ("bb","HJ","raise"):"TT+,AJs+,KQs,85s,74s+,63s+,53s+,43s,32s,AQo+,A9o",  
    ("bb","CO","call"):"22-99,A2s-A9s,K2s-KTs,Q2s-QTs,J4s+,T4s+,94s+,86s+,A8o-ATo,A5o,K9o-KJo,Q9o+,J9o+,T9o,98o",
    ("bb","CO","raise"):"TT+,ATs+,KJs+,84s-85s,73s+,63s+,52s+,42s,32s,AJo+,A3o-A4o,KQo",  
    ("bb","button","call"):"22-88,A2s-A9s,K2s-K9s,Q2s-Q9s,J2s-J9s,T2s+,92s+,82s+,72s,62s,A4o-ATo,K6o-KJo,Q7o+,J6o+,T6o+,96o+,86o+,76o",
    ("bb","button","raise"):"99+,ATs+,KTs+,QTs+,JTs,73s+,63s+,52s+,42s+,32s,AJo+,A2o-A3o,KQo,K2o-K5o,Q5o-Q6o,75o,65o",    
    ("bb","sb","call"):"22-88,A2s-A9s,K2s-K9s,Q2s-Q9s,J2s-J8s,T2s-T7s,92s-97s,82s-86s,72s-75s,62s-64s,52s-53s,42s+,32s,A3o-ATo,K4o-KJo,Q5o+,J6o+,T6o+,96o+,86o+",
    ("bb","sb","raise"):"99+,ATs+,KTs+,QTs+,J9s+,T8s+,98s,87s,76s,65s,54s,AJo+,A2o,KQo,K2o-K3o,Q2o-Q4o,J5o,T5o,75o+,64o+,54o",
    }

RangeFacing3bet = {
    ("UTG","UTG+1","call"):"99-QQ,AJs-AQs,KQs,QJs,JTs",
    ("UTG","UTG+1","raise"):"KK+,AKs,ATs,AQo+",
    ("UTG","UTG+2","call"):"88-QQ,AJs-AQs,KQs,QJs,JTs",
    ("UTG","UTG+2","raise"):"KK+,AKs,A9s-ATs,AQo+",
    ("UTG","LJ","call"):"88-QQ,AJs-AQs,KQs,QJs,JTs,T9s",
    ("UTG","LJ","raise"):"KK+,AKs,A9s-ATs,AQo+",
    ("UTG","HJ","call"):"77-JJ,AJs-AQs,KJs+,QJs,JTs,T9s",
    ("UTG","HJ","raise"):"QQ+,AKs,A9s-ATs,A5s,AQo+",
    ("UTG","CO","call"):"77-JJ,ATs-AQs,KJs+,QJs,JTs,T9s,AQo",
    ("UTG","CO","raise"):"QQ+,AKs,A9s,A5s,KTs,QTs,98s,AKo",
    ("UTG","button","call"):"77-JJ,ATs-AQs,KJs+,QJs,JTs,T9s,AQo",
    ("UTG","button","raise"):"QQ+,AKs,A9s,A5s,KTs,QTs,98s,AKo",
    ("UTG","sb","call"):"66-JJ,ATs-AQs,KJs+,QJs,JTs,T9s,AQo",
    ("UTG","sb","raise"):"QQ+,AKs,A9s,A5s,KTs,QTs,98s,AKo",
    ("UTG","bb","call"):"66-JJ,ATs-AQs,KJs+,QJs,JTs,T9s,AQo",
    ("UTG","bb","raise"):"QQ+,AKs,A9s,A5s,KTs,QTs,98s,AKo",
    ("UTG+1","UTG+2","call"):"77-QQ,AJs-AQs,KJs+,QJs,JTs,T9s",
    ("UTG+1","UTG+2","raise"):"KK+,AKs,A9s-ATs,A5s,AJo+",
    ("UTG+1","LJ","call"):"77-QQ,ATs-AQs,KJs+,QJs,JTs,T9s,AQo",
    ("UTG+1","LJ","raise"):"KK+,AKs,A9s,A4s-A5s,KTs,QTs,AKo,AJo",
    ("UTG+1","HJ","call"):"66-QQ,ATs-AQs,KJs+,QJs,JTs,T9s,98s,87s,AQo",
    ("UTG+1","HJ","raise"):"KK+,AKs,A9s,A4s-A5s,KTs,QTs,AKo,AJo,KQo",
    ("UTG+1","CO","call"):"66-QQ,ATs-AQs,KJs+,QJs,JTs,T9s,98s,87s,AQo",
    ("UTG+1","CO","raise"):"KK+,AKs,A9s,A4s-A5s,KTs,QTs,AKo,AJo,KQo",
    ("UTG+1","button","call"):"66-QQ,ATs-AQs,KJs+,QJs,JTs,T9s,98s,87s,AJo-AQo",
    ("UTG+1","button","raise"):"KK+,AKs,A9s,A4s-A5s,KTs,QTs,J9s,AKo,ATo,KQo",
    ("UTG+1","sb","call"):"66-JJ,ATs-AQs,KTs+,QTs+,JTs,T9s,98s,87s,AJo-AQo",
    ("UTG+1","sb","raise"):"QQ+,AKs,A8s-A9s,A4s-A5s,K9s,J9s,AKo,ATo,KQo",
    ("UTG+1","bb","call"):"66-JJ,ATs-AQs,KTs+,QTs+,JTs,T9s,98s,87s,AJo-AQo",
    ("UTG+1","bb","raise"):"QQ+,AKs,A8s-A9s,A4s-A5s,K9s,J9s,AKo,ATo,KQo",
    ("UTG+2","LJ","call"):"77-QQ,ATs-AQs,KJs+,QJs,JTs,T9s,98s,AQo",
    ("UTG+2","LJ","raise"):"KK+,AKs,A9s,A2s-A5s,AKo,AJo,KQo",
    ("UTG+2","HJ","call"):"66-QQ,ATs-AQs,KJs+,QJs,JTs,T9s,98s,AQo",
    ("UTG+2","HJ","raise"):"KK+,AKs,A9s,A2s-A5s,87s,AKo,AJo,KQo",
    ("UTG+2","CO","call"):"55-QQ,ATs-AQs,KTs+,QTs+,JTs,T9s,98s,87s,AQo",
    ("UTG+2","CO","raise"):"KK+,AKs,A8s-A9s,A2s-A5s,AKo,AJo,KQo",
    ("UTG+2","button","call"):"55-QQ,ATs-AQs,KTs+,QTs+,JTs,T9s,98s,87s,AQo",
    ("UTG+2","button","raise"):"KK+,AKs,A8s-A9s,A2s-A5s,AKo,AJo,KQo",
    ("UTG+2","sb","call"):"55-JJ,ATs-AQs,KTs+,QTs+,JTs,T9s,98s,87s,AQo",
    ("UTG+2","sb","raise"):"QQ+,AKs,A8s-A9s,A2s-A5s,AKo,AJo,KQo",
    ("UTG+2","bb","call"):"55-JJ,ATs-AQs,KTs+,QTs+,JTs,T9s,98s,87s,AQo",
    ("UTG+2","bb","raise"):"QQ+,AKs,A8s-A9s,A2s-A5s,AKo,AJo,KQo",
    ("LJ","HJ","call"):"77-JJ,ATs-AQs,KTs+,QTs+,JTs,T9s,98s,AQo",
    ("LJ","HJ","raise"):"QQ+,AKs,A8s-A9s,A2s-A5s,AKo,AJo,KQo",
    ("LJ","CO","call"):"66-TT,ATs-AQs,KTs+,QTs+,JTs,T9s,98s,AQo",
    ("LJ","CO","raise"):"JJ+,AKs,A8s-A9s,A2s-A5s,87s,AKo,AJo,KQo",
    ("LJ","button","call"):"55-TT,ATs-AQs,KTs+,QTs+,JTs,T9s,98s,87s,AQo",
    ("LJ","button","raise"):"JJ+,AKs,A7s-A9s,A2s-A5s,76s,AKo,AJo,KQo",
    ("LJ","sb","call"):"55-TT,ATs-AQs,KTs+,QTs+,J9s+,T9s,98s,87s,76s,AJo-AQo,KQo",
    ("LJ","sb","raise"):"JJ+,AKs,A2s-A9s,AKo,ATo,KJo",
    ("LJ","bb","call"):"44-TT,ATs-AQs,KTs+,QTs+,JTs,T9s,98s,87s,76s,AQo",
    ("LJ","bb","raise"):"JJ+,AKs,A2s-A9s,AKo,AJo,KQo",
    ("HJ","CO","call"):"55-TT,ATs-AQs,K9s+,Q9s+,J9s+,T9s,98s,87s,AJo-AQo,KQo",
    ("HJ","CO","raise"):"JJ+,AKs,A2s-A9s,76s,AKo,ATo,KJo",  
    ("HJ","button","call"):"44-TT,ATs-AQs,K9s+,Q9s+,J9s+,T9s,98s,87s,AJo-AQo,KQo",
    ("HJ","button","raise"):"JJ+,AKs,A2s-A9s,76s,65s,54s,AKo,ATo,KJo",    
    ("HJ","sb","call"):"44-TT,ATs-AQs,K9s+,Q9s+,J9s+,T9s,98s,87s,76s,AJo-AQo,KQo",
    ("HJ","sb","raise"):"JJ+,AKs,A2s-A9s,AKo,ATo,KJo",      
    ("HJ","bb","call"):"44-TT,ATs-AQs,KTs+,QTs+,JTs,T9s,98s,87s,76s,AQo",
    ("HJ","bb","raise"):"JJ+,AKs,A2s-A9s,AKo,AJo,KQo",
    ("CO","button","call"):"44-99,A9s-AQs,A5s,K9s+,Q9s+,J9s+,T8s+,98s,87s,76s,65s,AJo-AQo,KQo",
    ("CO","button","raise"):"TT+,AKs,A6s-A8s,A2s-A4s,97s,86s,75s,54s,AKo,ATo,KJo",
    ("CO","sb","call"):"44-99,A9s-AQs,A5s,K9s+,Q9s+,J9s+,T8s+,98s,87s,76s,65s,AJo-AQo,KQo",
    ("CO","sb","raise"):"TT+,AKs,A6s-A8s,A2s-A4s,97s,86s,75s,54s,AKo,ATo,KJo",
    ("CO","bb","call"):"44-99,A9s-AQs,A5s,K9s+,Q9s+,J9s+,T9s,98s,87s,76s,AJo-AQo,KQo",
    ("CO","bb","raise"):"TT+,AKs,A8s,A2s-A4s,T8s,97s,65s,54s,AKo,ATo,KJo",
    ("button","sb","call"):"22-88,A2s-ATs,K7s+,Q8s+,J8s+,T7s+,97s+,87s,76s,65s,A9o-AJo,KTo+,QJo",
    ("button","sb","raise"):"99+,AJs+,K4s-K6s,Q7s,J7s,86s,75s,64s,54s,43s,AQo+,A8o,A3o-A5o,K9o,QTo,JTo",
    ("button","bb","call"):"22-88,A2s-ATs,K7s+,Q8s+,J8s+,T7s+,97s+,87s,76s,65s,A9o-AJo,KTo+,QJo",
    ("button","bb","raise"):"99+,AJs+,K4s-K6s,Q7s,J7s,86s,75s,64s,54s,43s,AQo+,A8o,A3o-A5o,K9o,QTo,JTo",
    ("sb","bb","call"):"88-TT,ATs,KJs+,QJs,95s,85s,74s,43s,ATo-AJo,KJo+",
    ("sb","bb","raise"):"JJ-QQ,AJs+,J4s,AQo,K2o-K3o,Q4o-Q5o",
    ("sb","bb","limp/call"):"22-77,A2s-A9s,K2s-KTs,Q2s-QTs,J5s+,T6s+,96s+,86s+,75s+,64s+,54s,32s,A4o-A9o,K7o-KTo,Q8o+,J8o+,T8o+,97o+,87o,76o",
    ("sb","bb","limp/raise"):"KK+,AKo,A2o-A3o,K5o-K6o,Q7o"
    }

RangeFacing4bet = {
    ("UTG+1","UTG","All-in"):"QQ+,AKs,AKo",
    ("UTG+2","UTG","All-in"):"QQ+,AKs,AKo",
    ("UTG+2","UTG+1","All-in"):"QQ+,AKs,AKo",
    ("LJ","UTG","All-in"):"QQ+,AKs,AKo",
    ("LJ","UTG+1","All-in"):"QQ+,AKs,AKo",
    ("LJ","UTG+2","All-in"):"QQ+,AKs,AKo",
    ("HJ","UTG","All-in"):"QQ+,AKs,AKo",
    ("HJ","UTG+1","All-in"):"QQ+,AKs,AKo",
    ("HJ","UTG+2","All-in"):"QQ+,AKs,AKo",
    ("HJ","LJ","All-in"):"QQ+,AJs+,KQs,AQo+",
    ("CO","UTG","All-in"):"QQ+,AQs+,AKo",
    ("CO","UTG+1","All-in"):"QQ+,AQs+,AKo",
    ("CO","UTG+2","All-in"):"QQ+,AQs+,AKo",
    ("CO","LJ","All-in"):"QQ+,AJs+,KQs,AKo",
    ("CO","HJ","All-in"):"QQ+,AJs+,KQs,AKo",
    ("button","UTG","All-in"):"QQ+,AKs,AKo",
    ("button","UTG+1","All-in"):"QQ+,AKs,AKo",
    ("button","UTG+2","All-in"):"QQ+,AQs+,AQo+",
    ("button","LJ","All-in"):"QQ+,AQs+,AQo+",
    ("button","HJ","All-in"):"QQ+,AJs+,AQo+",
    ("button","CO","All-in"):"QQ+,AJs+,AQo+",
    ("sb","UTG","All-in"):"QQ+,AKs",
    ("sb","UTG+1","All-in"):"QQ+,AKs",
    ("sb","UTG+2","All-in"):"QQ+,AKs",
    ("sb","LJ","All-in"):"QQ+,AQs+,AKo",
    ("sb","HJ","All-in"):"QQ+,AQs+,AKo",
    ("sb","CO","All-in"):"TT+,ATs+,KQs,AQo+",
    ("sb","button","All-in"):"TT+,ATs+,KJs+,AJo+,KQo",
    ("bb","UTG","All-in"):"QQ+,AQs+",
    ("bb","UTG+1","All-in"):"QQ+,AQs+",
    ("bb","UTG+2","All-in"):"JJ+,AQs+,AKo",
    ("bb","LJ","All-in"):"TT+,AJs+,KQs,AKo",
    ("bb","HJ","All-in"):"TT+,AJs+,KQs,AQo+",
    ("bb","CO","All-in"):"TT+,ATs+,KJs+,QJs,AJo+,KQo",
    ("bb","button","All-in"):"99+,ATs+,KTs+,QTs+,JTs,AJo+,KQo",
    ("bb","sb","All-in"):"99+,ATs+,KTs+,QTs+,JTs,AJo+,KQo"
    }

RangeFacing5bet = {
    ("UTG","UTG+1","All-in"):"KK+,AKs,AKo",
    ("UTG","UTG+2","All-in"):"KK+,AKs,AKo",
    ("UTG","LJ","All-in"):"KK+,AKs,AKo",
    ("UTG","HJ","All-in"):"QQ+,AKs,AKo",
    ("UTG","CO","All-in"):"QQ+,AKs,AKo",
    ("UTG","button","All-in"):"QQ+,AKs,AKo",
    ("UTG","sb","All-in"):"QQ+,AKs,AKo",
    ("UTG","bb","All-in"):"KK+,AKs,AKo",
    ("UTG+1","UTG+2","All-in"):"KK+,AKs,AKo",
    ("UTG+1","LJ","All-in"):"KK+,AKs,AKo",
    ("UTG+1","HJ","All-in"):"KK+,AKs,AKo",
    ("UTG+1","CO","All-in"):"KK+,AKs,AKo",
    ("UTG+1","button","All-in"):"KK+,AKs,AKo",
    ("UTG+1","sb","All-in"):"QQ+,AKs,AKo",
    ("UTG+1","bb","All-in"):"QQ+,AKs,AKo",
    ("UTG+2","LJ","All-in"):"KK+,AKs,AKo",
    ("UTG+2","HJ","All-in"):"KK+,AKs,AKo",
    ("UTG+2","CO","All-in"):"KK+,AKs,AKo",
    ("UTG+2","button","All-in"):"KK+,AKs,AKo",
    ("UTG+2","sb","All-in"):"QQ+,AKs,AKo",
    ("UTG+2","bb","All-in"):"QQ+,AKs,AKo",
    ("LJ","HJ","All-in"):"QQ+,AKs,AKo",
    ("LJ","CO","All-in"):"JJ+,AKs,AKo",
    ("LJ","button","All-in"):"JJ+,AKs,AKo",
    ("LJ","sb","All-in"):"JJ+,AKs,AKo",
    ("LJ","bb","All-in"):"JJ+,AKs,AKo",
    ("HJ","CO","All-in"):"JJ+,AKs,AKo",
    ("HJ","button","All-in"):"JJ+,AKs,AKo",
    ("HJ","sb","All-in"):"JJ+,AKs,AKo",
    ("HJ","bb","All-in"):"JJ+,AKs,AKo",
    ("CO","button","All-in"):"TT+,AKs,AKo",
    ("CO","sb","All-in"):"TT+,AKs,AKo",
    ("CO","bb","All-in"):"TT+,AKs,AKo",
    ("button","sb","All-in"):"99+,AJs+,AQo+",
    ("button","bb","All-in"):"99+,AJs+,AQo+",
    ("sb","bb","All-in"):"JJ+,AJs+,AQo+"
    }