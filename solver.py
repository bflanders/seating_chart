# -*- coding: utf-8 -*-
"""
@author: bflander

LICENSE: use at your own risk, do whatever you want. Don't blame me. 
"""
#%% imports
from random import shuffle
#%% Variables
class Seater:
    def __init__(self
            ,seats=30, columns=5, students=28
            ,together=[], apart=[], front=[], back=[]
        ):
        self.seats = seats
        self.students = students
        self.unpicked = {i for i in range(students)}
        self.columns = columns
        self.together = together
        self.apart = apart
        self.front = front
        self.back = back
        self.consider = set(self.back+self.front)
        for a,b in together:
            self.consider.add(a)
            self.consider.add(b)
        for a,b in apart:
            self.consider.add(a)
            self.consider.add(b)
            
        self.seat_pairs = [
            (a,b) 
            for a in range(seats) 
            for b in range(seats) 
            if self.adjacent(a,b)
        ]
        
    @property
    def student_pairs(self):
        return [
            (self.seat_map[a],self.seat_map[b]) 
            for a in range(self.students) 
            for b in range(self.students)
            if (
                a != b
                and self.student_map[a] != 0
                and self.student_map[b] != 0
            )
        ]
        
    def preflight(self):
        front,back,seats,cols = self.front, self.back, self.seats, self.columns
        # Check if there are enough seats in the front
        if len(front) > cols:
            print('Error: not enough front seats.')
            print(f'Pick a larger `columns` number, at least {len(front)}')
            return False
        # Check if there is enough seats in the back
        if len(back) > seats%cols and seats%cols!=0:
            print('Error: not enough back seats.')
            print(f'Pick a larger `columns` number, at least {len(back)}')
            return False
        # No front and back sharing
        if set(self.front).intersection(set(self.back)):
            print('Error: FRONT and BACK share students!')
            return False
        # Make sure all your students to consider is below the student number
        if max(self.consider) > self.students:
            print('Error: you are referencing a student ID > # students')
            print('Max student ID allowed: {self.students-1}')
        # TODO: other checks...
        return True
    
    def print(self):
        prefix = ' '*(2*int(self.columns/2)-1)
        print(prefix+'---------')
        print(prefix+'| FRONT |')
        print(prefix+'---------')
        for seat in range(self.seats):
            print(f'{self.assignment[seat]:>2}',end=' ')
            # Start next line after # of columns
            if (seat+1)%self.columns==0:
                print()
    # Helper
    def adjacent(self, a, b):
        c = self.columns
        if a==b: return False
        if a//c==b//c: # same row
            return abs(a-b)==1
        if a%c==b%c: #   same column
            return abs(a-b)==c
    
    def in_front(self, seat):
        return seat//self.columns==0
    
    def in_back(self, seat):
        max_row = self.seats//self.columns-1
        return seat//self.columns==max_row
    
    def check(self, assignment=[]):
        seat_map = {i:v for i,v in enumerate(assignment)}
        student_map = {v:i for i,v in enumerate(assignment) if v!='*'} 
        
        # Are all fronts in the front and backs in back? And is there room?
        for front in self.front:
            if front in student_map:
                if not self.in_front(student_map[front]): return False
        for back in self.back:
            if back in student_map:
                if not self.in_back(student_map[back]): return False
        if len([seat 
               for seat in range(self.columns) 
               if (assignment[seat] in self.front or assignment[seat]=='*')
               ]) < len(self.front):
            return False
        back_row = self.columns if self.seats%self.columns==0 else self.seats%self.columns
        if len([seat 
               for seat in range(back_row) 
               if (assignment[-(seat+1)] in self.back or assignment[seat]=='*')
               ]) < len(self.back):
            return False
        
        # Are aparts together?
        for a,b in self.seat_pairs:
            student_a, student_b = seat_map[a], seat_map[b] 
            if student_a!='*' and student_b!='*':
                if (student_a,student_b) in self.apart: return False
                if (student_b,student_a) in self.apart: return False
        
        # Are togethers apart?
        for a,b in self.together:
            if a in student_map and b in student_map:
                seat_a, seat_b = student_map[a], student_map[b]
                ab = (seat_a, seat_b) not in self.seat_pairs 
                ba = (seat_b, seat_a) not in self.seat_pairs
                if ab and ba: return False
        
        
        # No early outs...
        return True
    def _next(self, assignment):
        branches = []
        unpicked = {i for i in self.consider if i not in self.assignment}
        empty = {i for i in range(self.seats) if self.assignment[i]=='*'}
        nexts = [(u,e) for u in unpicked for e in empty]
        for k,seat in nexts:
            copy = assignment[:]
            copy[seat] = k
            if self.check(copy):
                branches.append(copy)
        return branches
    
    def solve(self, stop=1):
        if not self.preflight(): return []
        # Prime the pump
        self.branches = [list('*'*self.seats)]
        solutions = []
        itr = 0
        while self.branches:
            assignment = self.branches.pop()
            self.assignment = assignment
            if len([seat for seat in assignment if seat!='*'])==len(self.consider):
                if assignment not in solutions:
                    solutions.append(assignment)
                    print('Solution!')
                    self.print()
                    if len(solutions)==stop: break
            self.branches.extend(self._next(assignment))
            itr += 1
            if itr%100==0:
                shuffle(self.branches)
                print(f'Still running after {itr:,d} checks...')
        return solutions
            
#%% Print seat layout
togethers = [
    (1,5)
    ,(2,10)
    ,(20,17)
]

apart = [
    (7,11)
    ,(8,19)        
    ,(9,17)
]

front = [3,8,16,19]

back = [9,13,5]

seater = Seater(**{
    'seats': 30
    ,'students': 25
    ,'columns': 6
    ,'together': togethers, 'apart': apart, 'front': front, 'back': back        
})

solutions = seater.solve(stop=2)
