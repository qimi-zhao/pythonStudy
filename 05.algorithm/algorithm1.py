#coding:utf-8

from __future__ import division

import random

def score(score_list,course_list,student_num):
    course_num = len(course_list)
    ### get students scores
    every_score = [[score_list[j][i] for j in range(course_num)] for i in range(student_num)]
    ### calc sum of scores for all students
    every_total = [sum(every_score[i]) for i in range(student_num)]
    ### get average scores for all students
    ave_course = [sum(score_list[i])/len(score_list[i]) for i in range(len(score_list))]
    return (every_score, every_total, ave_course)

if __name__=="__main__":
    course_list = ["C++","Java","Servlet","JSP","EJB"]
    student_num = 20
    score_list = [[random.randint(0,100) for i in range(student_num)] for j in range(len(course_list))]
    
    for i in range(len(course_list)):
        print('score of every one in %s:'%course_list[i])   ### 格式化输出字符串替换
        print(score_list[i])
        
    ### calc
    every_score, every_total, ave_one_course = score(score_list, course_list, student_num)
    
    print('\nNEXT IS EVERY ONE SCORE IN EVERY COURSE:')
    print(every_score)
    print('\n')
    
    for name in course_list:
        print(name, '\t\t', end="")
    
    print('\n')
    print('every course of average score:\t', ave_one_course)
    print('every one all score:\t', every_total)