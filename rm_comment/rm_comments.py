import os
import sys
import re


def _min(a, b):
    if a < b:
        return a
    else:
        return b
def _max(a, b):
    if a < b:
        return b
    else:
        return a

def make_str_same_length(short, longs):
    diff = len(longs) - len(short)
    str = '%'+'%d' % (diff) +'s'
    short = short + str % ('_')
    return short, longs

def hex2(a):
    return a > 0 and hex(a) or hex(a&0xffffffff)

def __print_list_to_another_file(lists, cfile='', retu=1, level=0):
    if cfile == '':
        log_fp = sys.stdout
    else:
        if os.path.exists(cfile):
            os.remove(cfile)
        log_fp = open(cfile, 'a+')
    for li in lists:
        if type(li) != type([]): 
            if li == '':
                print >>log_fp, '\t',
            elif type(li) == type(0):
                print >>log_fp, '\t', hex2(li),
            else:
                print >>log_fp, '\t',li,
        elif level < 10:
            level += 1
            __print_list_to_another_file(li, '', retu, level)
            level -= 1        
    if level == retu:
        print >>log_fp

class Comments():
    NOT_COMMENT = 'NOT_COMMENT'
    ONE_LINE_COMMENT = 'ONE_LINE_COMMENT'
    LINES_COMMENT_BEGIN = 'LINES_COMMENT_BEGIN'
    LINES_COMMENT = 'LINES_COMMENT'
    LINES_COMMENT_END = 'LINES_COMMENT_END'

    def _remove_comments(self, filename):
        linenum = 0
        ctype = Comments.NOT_COMMENT
        after = []
        f = open(filename, 'r')
        for line in open(filename):
            line = f.readline()
            linenum = linenum + 1
            ctype, after = self.__do_remove(linenum, ctype, after, line)
        f.close()

        return after

    def __is_one_line_comment(self,line):
        is_comment = Comments.NOT_COMMENT
        c_s = line.find('/*')
        c_e = line.find('*/')
        while (  c_s != -1 ) and ( c_e != -1 ) and ( c_s < c_e):
            line = line[:c_s] + line[c_e+2:]
            c_s = line.find('/*')
            c_e = line.find('*/')
        eline = line.lstrip().rstrip()
        if eline == '':
            is_comment = Comments.ONE_LINE_COMMENT
        if line.lstrip().startswith('//'):
            is_comment = Comments.ONE_LINE_COMMENT
        else:
            c_index = line.lstrip().find('//')
            if -1 != c_index:
                is_comment = Comments.NOT_COMMENT
                line = line[:c_index]
                line = line.rstrip() +'\n'
        return line, is_comment
    
    def __is_lines_comments(self, line, ctype=0):
        eline = ''
        j = 0
        if ctype == Comments.LINES_COMMENT:
            index = line.find('*/')
            while( -1 != index and line.split()):            
                line = line[index+2:]
                if line.rstrip() == '':
                    if eline == '': 
                        ctype = Comments.LINES_COMMENT_END
                    else:
                        ctype = Comments.NOT_COMMENT
                else:
                    i = line.find('/*')
                    if -1 != i:
                        li = line[:i]
                        if li.lstrip() == '/':
                            line = line[i:]
                        else:
                            eline += li.lstrip()
                            line = line[i+2:]
                        index = line.find('*/')
                        if eline == '':
                            ctype = Comments.LINES_COMMENT
                        else:
                            ctype = Comments.LINES_COMMENT_BEGIN
                        
                    else:
                        index = -1
                        eline += line.lstrip().rstrip()
                        if eline == '':
                            ctype = Comments.ONE_LINE_COMMENT
                        else:
                            ctype = Comments.NOT_COMMENT
                j = j + 1
            if -1 == eline.find('\n'):
                eline = eline.rstrip() + '\n'
            if eline != '':
                line = eline                      
        else:
            if -1 != line.find('/*'):            
                    ctype = Comments.LINES_COMMENT
                    line = re.sub("\/\*.*", "", line)      
                    eline = line.lstrip()
                    if eline != '':
                        ctype = Comments.LINES_COMMENT_BEGIN
                        line = eline
                    
            else:        
                ctype = Comments.NOT_COMMENT
                
        return line, ctype
    
    def __is_comments(self, line, ctype=NOT_COMMENT):
        if ctype == Comments.NOT_COMMENT:
            line, ctype = self.__is_one_line_comment(line)
            if ctype == Comments.NOT_COMMENT:
                line, ctype = self.__is_lines_comments(line, ctype)
        else:
            line, ctype = self.__is_lines_comments(line, ctype)     
        return line, ctype
    
    
    def __do_remove(self, linenum, ctype, after, line):
        if line.lstrip().rstrip() == '' or line[0] == '$':
            return ctype, after
            print 'blank line'
        line, ctype = self.__is_comments(line, ctype)
        if ctype == Comments.NOT_COMMENT or ctype == Comments.LINES_COMMENT_BEGIN:
            after.append(str(linenum) + ' | ' + line)
        elif ctype == Comments.LINES_COMMENT_END or ctype == Comments.ONE_LINE_COMMENT:
            ctype = Comments.NOT_COMMENT
        if ctype == Comments.LINES_COMMENT_BEGIN:
            ctype = Comments.LINES_COMMENT
        
        return ctype, after



def __get_line_from_cleanline(line):
    index = line.find("|")
    if index != -1:
        li = line[index+1:].lstrip()
    else:
        li = line
    return ' '+li

def __is_end_of_statement(line):
    ret = False
    operators = ['=', ',', '(', '<>', 'OR', 'AND']
    for opr in operators:
        l = len(opr) + 1
        if not cmp(line[-l:-1], opr):
            ret = True
            break
    
    return ret    

def __remove_blank(line):
    return line.rstrip()+'\n'

def __combine_lines(cleanlines):
    contin = False
    index = 0
    tli = []
    for li in cleanlines:
        if li[-1] == '\n':
            li = __remove_blank(li)
            if __is_end_of_statement(li):
                tmp = li[0:-1]
                if contin == True:
                    tmp = __get_line_from_cleanline(tmp)
                    tli[index] = tli[index] + tmp
                else:
                    tli.append(tmp)
                contin = True
            else:
                if contin == True:
                    li = __get_line_from_cleanline(li)
                    tli[index] = tli[index] + li
                else:
                    tli.append(li)
                contin = False
        if contin == False:
            index = index + 1
    return tli

def remove_comments(filename, cleanfile, return_type=''):   
    if ( not filename.lower().endswith('.c')):
        print '%s is not C source codes' % (filename)
        return
#    fn = os.path.basename(filename)
    print 'analyzing %s' % filename
    comms = Comments()
    cleanlines = comms._remove_comments(filename)
    if return_type == 'string':
        return cleanlines
    
    __print_list_to_another_file(cleanlines, cleanfile)
    return


if __name__ == "__main__":
    remove_comments(r'.\example.c', 'expected.c')