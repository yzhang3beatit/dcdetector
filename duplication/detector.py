import os
import sys
import re
from types import MethodType

#from DxMml.helper import DictItem, ListItem

class ListItem:

    def __str__(self):
        tmp = ",".join(sorted([ "%s=%s" % (item, getattr(self, item)) for item in dir(self)
                                if not item.startswith("_") and getattr(self, item) != None and
                                    type(getattr(self, item)) is not MethodType ] ))
        for i in xrange(len(tmp)):
            if ord(tmp[i]) > 127:
                tmp = tmp.replace(tmp[i], " ")
        return tmp

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()
    
    def __getitem__(self, attribute):
        try:
            if not attribute.startswith("_") and getattr(self, attribute) != None and type(getattr(self, attribute)) is not MethodType:
                return getattr(self, attribute)       
        except:
                pass        
            
        return None    
    

class DictItem(dict):
    
    def __init__(self,*args):
        dict.__init__(self,*args)
        self.ordered_keys = []
        
    def __str__(self):
        try:
            tmp = "\n".join([ key + ':' + str(self[key]) for key in self.ordered_keys ])
            for i in xrange(len(tmp)):
                if ord(tmp[i]) > 127:
                    tmp = tmp.replace(tmp[i], " ")
            return tmp
        except AttributeError:
            return ""

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self,key)
        except:
            pass
        if type(key) == type(1):
            try:
                return dict.__getitem__(self, self.ordered_keys[key])
            except:
                pass
        return None

    def __setitem__(self, key, item):
        dict.__setitem__(self, key, item)
        try:
            if key in self.ordered_keys:
                self.ordered_keys.remove(key)
            self.ordered_keys.append(key)
        except AttributeError:
            self.ordered_keys = [key, ]

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        self.ordered_keys.remove(key)

    def __getattr__(self, name):
        if len(self) != 1:
            raise AttributeError
        return getattr(self.values()[0], name)

    def length(self):
        return len(self)

    def _get_empty_container(self):
        return DictItem()

    def sort(self,*args):
        try:
            self.ordered_keys.sort(*args)
        except AttributeError:
            pass


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
    return a>0 and hex(a) or hex(a&0xffffffff)

def __print_list_to_another_file(lists, cfile='', retu=1, level=0):
    if cfile == '':
        log_fp = sys.stdout
    else:
        if os.path.exists(cfile):
            os.remove(cfile)
        log_fp = open(cfile, 'a+')
    for li in lists:
#        if type(li) == type(u'') or type(li) == type('') or type(li) == type(0) or type(li) == type(0.0):
        if type(li) != type([]): 
            if li == '':
                print >>log_fp, '\t',
            elif type(li) == type(0):
                print >>log_fp, '\t', hex2(li),
            else:
                print >>log_fp, '\t',li,
        elif level < 10:
            level += 1
#            print level, li, type(li)
            __print_list_to_another_file(li, '', retu, level)
            level -= 1        
    if level == retu:
        print >>log_fp

class org_Comments_test():
    NOT_COMMENT = 'NOT_COMMENT'
    ONE_LINE_COMMENT = 'ONE_LINE_COMMENT'
    LINES_COMMENT_BEGIN = 'LINES_COMMENT_BEGIN'
    LINES_COMMENT = 'LINES_COMMENT'
    LINES_COMMENT_END = 'LINES_COMMENT_END'

    def _remove_comments(self, filename):
        linenum = 0
        ctype = org_Comments_test.NOT_COMMENT
        after = []
        f = open(filename, 'r')
        for line in open(filename):
            line = f.readline()
            linenum = linenum + 1
            ctype, after = self.__do_remove(linenum, ctype, after, line)
        f.close()

        return after

    def __is_one_line_comment(self,line):
        is_comment = org_Comments_test.NOT_COMMENT
        c_s = line.find('/*')
        c_e = line.find('*/')
        while (  c_s != -1 ) and ( c_e != -1 ) and ( c_s < c_e):
            line = line[:c_s] + line[c_e+2:]
            c_s = line.find('/*')
            c_e = line.find('*/')
    #        line = re.sub("(\/\*)[^(\/\*)]*(\*\/){1}", "", line)   
        eline = line.lstrip().rstrip()
    #    print ':',eline,':'
        if eline == '':
            is_comment = org_Comments_test.ONE_LINE_COMMENT
        return line, is_comment
    
    def __is_lines_comments(self, line, ctype=0):
        eline = ''
        j = 0
        if ctype == org_Comments_test.LINES_COMMENT:
            index = line.find('*/')
            while( -1 != index and line.split()):            
                line = line[index+2:]
                if line.rstrip() == '':
                    if eline == '': 
                        ctype = org_Comments_test.LINES_COMMENT_END
                    else:
                        ctype = org_Comments_test.NOT_COMMENT
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
                            ctype = org_Comments_test.LINES_COMMENT
                        else:
                            ctype = org_Comments_test.LINES_COMMENT_BEGIN
                        
                    else:
                        index = -1
                        eline += line.lstrip().rstrip()
                        if eline == '':
                            ctype = org_Comments_test.ONE_LINE_COMMENT
                        else:
                            ctype = org_Comments_test.NOT_COMMENT
                j = j + 1
            if -1 == eline.find('\n'):
                eline = eline.rstrip() + '\n'
            if eline != '':
                line = eline                      
        else:
            if -1 != line.find('/*'):            
                    ctype = org_Comments_test.LINES_COMMENT
                    line = re.sub("\/\*.*", "", line)      
                    eline = line.lstrip()
#                    print ';',eline,';'
                    if eline != '':
                        ctype = org_Comments_test.LINES_COMMENT_BEGIN
                        line = eline
                    
            else:        
                ctype = org_Comments_test.NOT_COMMENT
                
        return line, ctype
    
    def __is_comments(self, line, ctype=NOT_COMMENT):
    #    print line,
        if ctype == org_Comments_test.NOT_COMMENT:
            line, ctype = self.__is_one_line_comment(line)
            if ctype == org_Comments_test.NOT_COMMENT:
                line, ctype = self.__is_lines_comments(line, ctype)
        else:
            line, ctype = self.__is_lines_comments(line, ctype)     
        return line, ctype
    
    
    def __do_remove(self, linenum, ctype, after, line):
        if line.lstrip().rstrip() == '' or line[0] == '$':
            return ctype, after
            print 'blank line'
        line, ctype = self.__is_comments(line, ctype)
#        print ctype, line
        if ctype == org_Comments_test.NOT_COMMENT or ctype == org_Comments_test.LINES_COMMENT_BEGIN:
            after.append(str(linenum) + ' | ' + line)
        elif ctype == org_Comments_test.LINES_COMMENT_END or ctype == org_Comments_test.ONE_LINE_COMMENT:
            ctype = org_Comments_test.NOT_COMMENT
        if ctype == org_Comments_test.LINES_COMMENT_BEGIN:
            ctype = org_Comments_test.LINES_COMMENT
        
        return ctype, after



class Subblock(ListItem):
    def __init__(self, lists, index, size):
        self.sep = ':'
        self.block = []
        for i in xrange(size):           
            self.block.append(lists[index])
            index = index + 1
            
        
    def _get_type(self):
        return self.block[0][0]+self.sep+self.block[0][1]
    def _get_block(self):
        return self.block 
        
class Couple(DictItem):
    def __init__(self):
        self.male = None
        self.female = None
        
    def _append(self, lists, index, size):
#        print len(lists), index, size
        if self.male == None:
            self.male = Subblock(lists, index, size)
        elif self.female == None:
            self.female = Subblock(lists, index, size)
            self[self.male._get_type()+self.female._get_type()] = [self.male, self.female]
            self.male = None
            self.female = None
            
    def _get_male(self, key):
        return self[key][0]
    
    def _get_female(self, key):
        return self[key][1]

class Duplication():
    def __init__(self, type, nlines, nwords):
        self.type = type 
        self.hashcode = []
        self.conlib = []
        self.lib = []
        self.hctmp = []
        self.contmp = []
        self.tmp = []
        self.dups = Couple()
        self.comdup = Couple()
        self.dupsize = 0
        self.nlines = nlines
        self.nwords = nwords
        self.remove_keyword = ['PROCEDURE', 'FUNCTION']
        
    def _combine(self):
        print self.dups.keys()

    def _similar(self, diff, maxs):
        value = ( 10 * ( diff ) ) / maxs
        if value <= self.nwords:
            return True
        else:
            return False

    def _is_similar(self, boy, brother):
        bol = len(boy)
        brl = len(brother)
        mins = _min(bol, brl)
        maxs = _max(bol, brl)

        if bol == mins:
            short = boy
            longs = brother
        else:
            short = brother
            longs = boy
            
        if maxs == 0:
            maxs = 1
#            print 'maxs == 0:',longs,':'            
        diff = maxs - mins
        similar = self._similar(diff, maxs)
        if not similar:
            return False  # different line
        index = 0
        diff = 0
        short, longs = make_str_same_length(short, longs)     
        while (self._similar(diff, maxs) and ( index < maxs )):             
            if (short[index] != longs[index]):
                diff = diff + 1
            index = index + 1
        return self._similar(diff, maxs)            

    def _str_cmp(self, one, two_index):
        return self._is_similar(one, self.conlib[two_index][2])
    
    def _hashcode_cmp(self, one, two_index):
        if self.nwords != 10:
            print one, self.hashcode[two_index][2]
            return self._is_similar(str(one), str(self.hashcode[two_index][2]))
        else:
            return one == self.hashcode[two_index][2]
#        return (one == self.hashcode[two_index][2])  
             
    def _line_same(self, index):
        same = 0
        i = 0
#        if self.type == 'hashcmp':
        line_cmp = self._hashcode_cmp
#        lis = self.hctmp
#        else:
#            line_cmp = self._str_cmp
#            lis = self.contmp
        
        for li in self.hctmp:
            if not line_cmp(li[2], index + i):
                return False
            i = i + 1
            
        return True
        
    def _lines_same(self):
        ll = len(self.conlib)
        if ll < self.nlines:
            return -1
        for index in xrange(ll - self.nlines): 
            if self._line_same(index):
                return index
        return -1                  
        
    def _remove_keyword(self, line):
        li = line.split(':')
        for keyword in self.remove_keyword:
            if li and len(li) >=2  and ((li[1].lstrip().rstrip() == keyword)):
                line = li[0] 
        return line

    def _contract(self, line):
        line = self._remove_keyword(line)
        line = re.sub("[^A-Za-z0-9]", "", line)
        return line.upper()
    
    def _delete_tmp(self):
        self.contmp = self.contmp[1:]
        self.tmp = self.tmp[1:]
        self.hctmp = self.hctmp[1:]

    def _empty_tmp(self):
        self.contmp = []
        self.tmp = []
        self.hctmp = []
    
    def _insert_db(self, index):
        self.conlib.append([self.contmp[index][0], self.contmp[index][1], self.contmp[index][2]])
#        self.conlib.append([self.contmp[0][0], self.contmp[0][1], self.contmp[0][2]])
#        self.lib.append([self.tmp[0][0], self.tmp[0][1], self.tmp[0][2]])
        self.lib.append([self.tmp[index][0], self.tmp[index][1], self.tmp[index][2]])
        self.hashcode.append([self.hctmp[index][0], self.hctmp[index][1], self.hctmp[index][2]])
#        self.hashcode.append([self.hctmp[0][0], self.hctmp[0][1], self.hctmp[0][2]])
    
    def _examine_dup(self, filen, linenum, oline):
        line = self._contract(oline)
        self.contmp.append([filen, linenum, line])
        self.tmp.append([filen, linenum, oline])
        self.hctmp.append([filen, linenum, line.__hash__()])
        
        l = len(self.contmp)
        if l >= self.nlines:
            found_i = self._lines_same()
#            print found_i, linenum
            if -1 != found_i:
                self.dups._append(self.lib, found_i, self.nlines)
                self.dups._append(self.tmp, 0, self.nlines)
                self.dupsize = self.dupsize + 1
                    
                for li in xrange(l):
                    self._insert_db(li);
#                    self.conlib.append([self.contmp[li][0], self.contmp[li][1], self.contmp[li][2]])
#                    self.lib.append([self.tmp[li][0], self.tmp[li][1], self.tmp[li][2]])
#                    self.hashcode.append([self.hctmp[li][0], self.hctmp[li][1], self.hctmp[li][2]])
                self._empty_tmp()
            else:
                self._insert_db(0)
#                self.conlib.append([self.contmp[0][0], self.contmp[0][1], self.contmp[0][2]])
#                self.lib.append([self.tmp[0][0], self.tmp[0][1], self.tmp[0][2]])
#                self.hashcode.append([self.hctmp[0][0], self.hctmp[0][1], self.hctmp[0][2]])
                self._delete_tmp()
    
class Block(ListItem):
    def __init__(self, parent, btype, linenum, name):
        self.sep = '\t'
        self.parent = parent
        self.type = btype
        self.name = name
        self.deif = 0
        self.elsf = 0
        self.endd = 0
        self.lines = 0
        self.lineno = linenum
    
    def _get_type(self):
        return self.type
      
    def _parse_decision(self, lan, line):
        if lan._is_decision(line):
            self.deif = self.deif + 1
        elif lan._is_end_decision(line):
            self.endd = self.endd + 1        
        elif lan._is_elif(line):
            self.elsf = self.elsf + 1
        self.lines = self.lines + 1
        
    def _get_lines(self):
        return self.lines
    
    def _get_cc(self):
#        assert(self.elsf >= self.deif)
        return self.deif + (self.elsf) + 1

    def _get_key(self):
        return self.name
    
    def _get_parent(self):
        return self.parent



class Procd(Block):
    def __init__(self, parent, btype, linenum, name):
        Block.__init__(self, parent, btype, linenum, name)
        
    def _get_key(self):
        return self.parent +  self.sep + self.name

class Input(Block):
    def __init__(self, parent, btype, linenum, name):
        Block.__init__(self, parent, btype, linenum, name)

    def _get_key(self):
        return self.parent._get_key() + self.sep + Block._get_key(self)

class State(Block):
    def __init__(self, procedure, linenum, state):
        Block.__init__(self, procedure, Sdl.TYPE_STATE, linenum, state)
        
    def _get_key(self):
        return self.parent._get_key() + self.parent.sep + Block._get_key(self)

class Language():
    NONE_TYPE = 'None'
    TYPE_PROCD = 'PROCEDURE'

    def __init__(self):
        self.name = ''
    
    def _createAnalyzer(self, fname):
        lan = None
        self.name = fname
        if fname.lower().endswith('sdl'):
            lan = Sdl()
        elif fname.lower().endswith('p38'):
            lan = Plm()
        elif fname.lower().endswith('.c') or fname.lower().endswith('.cpp'):
            lan = Cpp()
        else:
            assert(False)
        return lan
        
    def _strip_line(self, line):
        return line.lstrip().rstrip()
    def _createBlock(self):pass
    def _is_block_begin(self):pass
    def _is_block_end(self):pass
    def _is_decision(self, line):pass
    def _is_end_decision(self, line):pass
    def _is_elif(self, line):pass
    
class Cpp(Language):
    def __init__(self):
        Language.__init__(self)
        self.last_line = ''
        self.procd = None
        
    def _is_block_begin(self, linenum, line):
        if self._is_procedure(line):
            return True    
    def _is_block_end(self, linenum, line):
        if self._is_end_of_procd(line):
            return True

    def _createBlock(self, fname, linenum, line):
        if line.startswith(' {'):
            line = self.last_line
        bb = Procd(fname, Cpp.TYPE_PROCD, linenum, line)
        self.procd = bb
        assert(bb != None)
        return bb      

        
    def _insert_last_line(self, line):
        self.last_line = line
    
    def _get_name(self):
        return self.last_line
    
    def _strip_line(self, line):        
        return line.rstrip()
    
    def _is_procedure(self, line):
        return line.startswith(" {")
    
    def _is_end_of_procd(self, line):
        return line.startswith(" }")

    def _is_decision(self, line):
        return line.lstrip().startswith('for') or line.lstrip().startswith('while') or line.lstrip().startswith('if')

    def _is_end_decision(self, line):
        return line.lstrip().startswith('}')
    
    def _is_elif(self, line):
        return line.lstrip().startswith('else if')

class Sdl(Language):
    TYPE_INPUT = 'INPUT'
    TYPE_STATE = 'STATE'
    TYPE_PROCESS = 'PROCESS'

    def __init__(self):
        Language.__init__(self)
        self.type = Sdl.NONE_TYPE
        self.input = None
        self.state = None
        self.procd = None
        self.process = None
        
    def _is_block_begin(self, linenum, line):
        bb = None
        if self._is_process(line):
            self.type = Sdl.TYPE_PROCESS
            return True
        elif self._is_procedure(line):
            self.type = Sdl.TYPE_PROCD
            return True
        elif self._is_state(line):
            self.type = Sdl.TYPE_STATE
            return True
        elif self._is_input(line):
            self.type = Sdl.TYPE_INPUT
            return True
    
    def _is_block_end(self, linenum, line):
        if self._is_end_of_state(line):
            self.type = self.state._get_parent()._get_type()
            self.input = None
            return True
        elif self._is_end_of_procd(line):
            parent = self.procd._get_parent()
            if parent != None and type('') != type(parent):
                self.type = parent._get_type()
            else:
                self.type = None
            self.procd = None
            return True
        elif self._is_end_of_process(line):
            self.type = Sdl.NONE_TYPE
            self.process = None
            return True


    def _createBlock(self, fname, linenum, line):
        bb = None
        line = self._remove_comment(line)
        if self.type == Sdl.TYPE_PROCESS:
            bb = Procd(fname, self.type, linenum, line)
            self.process = bb
        elif self.type == Sdl.TYPE_PROCD:
            bb = Procd(fname, self.type, linenum, line)
            self.procd = bb
        elif self.type == Sdl.TYPE_STATE:
            if self.procd != None:
                bb = State(self.procd, linenum, line) # create State class
            elif self.process != None:
                bb = State(self.process, linenum, line)
            self.state = bb
        elif self.type == Sdl.TYPE_INPUT:          
            bb = Input(self.state, self.type, linenum, line)
            self.input = bb
        assert(bb != None)
        return bb      

    def _remove_comment(self, line):
        index = line.find(';')
        if index == -1:
            index1 = line.find('/*')
            if index1 != -1:
                index = index1

        return line[0:index].lstrip().rstrip()
    
    def _is_state(self, line):
        return line.startswith('STATE')
    
    def _is_process(self, line):
        return line.startswith("PROCESS") or line.startswith("MASTER PROCESS") 
    
    def _is_procedure(self, line):
        return line.startswith("PROCEDURE")

    def _is_end_of_state(self, line):
        return line.startswith('ENDSTATE')

    def _is_input(self, line):
        return line.startswith('INPUT')

    def _is_end_of_procd(self, line):
        return line.startswith('ENDPROCEDURE')
    
    def _is_end_of_process(self, line):
        return line.startswith('ENDPROCESS')

    def _is_decision(self, line):
        return line.startswith('WHILE') or line.startswith('DECISION')

    def _is_end_decision(self, line):
        return line.startswith('ENDWHILE') or line.startswith('ENDDECISION')
    
    def _is_elif(self, line):
        return re.match('.*\(?.*\)\:', line)
    
class Plm(Language):
    def __init__(self):
        Language.__init__(self)
        self.procd = None
        
    def _is_block_begin(self, linenum, line):
        if self._is_procedure(line):
            return True
    
    def _is_block_end(self, linenum, line):
        if self._is_end_of_procd(line):
            self.procd = None
            return True

    def _createBlock(self, fname, linenum, line):
        bb = Procd(fname, Plm.TYPE_PROCD, linenum, line)
        self.procd = bb
        assert(bb != None)
        return bb      

    
    def _is_procedure(self, line):
        ret = False
        li = line.split(':')
        if li and len(li) >=2  and ((li[1].lstrip().rstrip() == 'PROCEDURE') or (li[1].lstrip().rstrip() == 'FUNCTION')):
            ret = True
        return ret

    def _is_end_of_procd(self, line):
        ret = False
        li = line.split(' ')
        if li and len(li) >=2  and li[0].lstrip().rstrip() == 'END' :
            ret = True
        return ret

    def _is_decision(self, line):
        return line.upper().startswith('DO WHILE') or line.upper().startswith('IF') or line.upper().startswith('DO CASE')

    def _is_end_decision(self, line):
        return line.upper().startswith('FI') or line.upper().startswith('OD;')
    
    def _is_elif(self, line):
        return line.upper().startswith('ELSEIF') or line.upper().startswith('DO;')

class CodeBlocks(DictItem):
    def __init__(self, fname, cfilename, codes):
        self.fname = fname
        self.lan = Language()
        self.language = None
        self._parse_blocks(cfilename, codes)
        
    def _parse_blocks(self, cfilename, codes):
        bb = None
        
        self.language = self.lan._createAnalyzer(self.fname)

        f = open(cfilename, 'r')
        for line in open(cfilename):
            line = f.readline()
            line = line.lstrip().rstrip()

            try:
                linenum = line.split("|")[0]
                line = line.split("|")[1]
            except:
                print line, linenum
                assert(False)
            line = self.language._strip_line(line)
            '''
            if self.language._is_block_begin(linenum, line):
                if bb != None:
                    self[bb._get_key()] = bb
                bb = self.language._createBlock(self.fname, linenum, line)
            elif self.language._is_block_end(linenum, line):
                if bb != None:
                    self[bb._get_key()] = bb
                bb = None
            elif bb != None:
                bb._parse_decision(self.language, line)
            '''
            if codes != None:
                codes._examine_dup(self.fname, linenum, line)

            if 'Cpp' == self.language.__class__.__name__:
                self.language._insert_last_line(line)

        f.close()
        
    def _print_blocks(self, fn):
        if fn == '':
            log_fp = sys.stdout
        else:
            log_fp = open(fn, 'a+')
        for bb in self:
            if self[bb]._get_type() == Sdl.TYPE_INPUT:
                sep = ''
            elif self[bb]._get_type() == Sdl.TYPE_STATE:
                sep = '\t'
            else:
                sep = '\t\t'
            
            print >>log_fp, self[bb].lineno + '\t' + self[bb]._get_key() + '\t' + sep, self[bb]._get_cc(), '\t', self[bb]._get_lines()
            



def __count_cc_and_display_for_one_file(fname, cfile, codes, fn):
    bbs = CodeBlocks(fname, cfile, codes)
    bbs._print_blocks(fn)

def __max_width(codes):
    max_width = 0
    dups = codes.dups
    for bb in dups.keys():
        block = dups._get_male(bb)._get_block()
        for index in xrange(len(block)):
            width = len(block[index][2]) 
            if max_width < width:
                max_width = width
    return max_width

def __max_width_block(block):
    max_width = 0
    for bb in block:
        width = len(bb[2]) 
        if max_width < width:
            max_width = width
    return max_width

def __display_duplic(codes, fn=''):
    if fn == '':
        log_fp = sys.stdout
    else:
        if os.path.exists(fn):
            os.remove(fn)
        log_fp = open(fn, 'a+')
    dups = codes.dups
#    max_width = __max_width(codes)
#    form = "%d" % max_width 
#    formtitle = '%s\t'+'%-'+form+'s'
#    form = '%-'+form+'s'
    print >>log_fp
    print >>log_fp,  '================================================================================'
    print >>log_fp,  'DUPLICATION: %d' % (codes.dupsize)
    i = 0
    for bb in dups.keys():
        i = i + 1
        print >>log_fp, 'No. %d' % i
        print >>log_fp, '****FILENAME********LINE*************************FILENAME********LINE***********'
        block = dups._get_male(bb)._get_block()
        blockf = dups._get_female(bb)._get_block()
        max_width = __max_width_block(block)
        form = "%d" % max_width 
        formtitle = '%s\t'+'%-'+form+'s'
        form = '%-'+form+'s'

        for index in xrange(len(block)):
            if index == 0:
                form1 = "%d" % (max_width - len(block[index][0]) - len( block[index][1]))
                formtitle = '%s\t'+'%-'+form1+'s'
                print >>log_fp, formtitle % (block[index][0],  block[index][1]),
                print >>log_fp, blockf[index][0], blockf[index][1]
                print >>log_fp, '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
                
            print >>log_fp, form % block[index][2], 
            print >>log_fp, blockf[index][2]
        print >>log_fp, '*********************************DUPLICATION************************************'

        print >>log_fp

def __get_line_from_cleanline(line):
    index = line.find("|")
    if index != -1:
        li = line[index+1:].lstrip()
    else:
        li = line
    return ' '+li

def __is_end_of_statement(line):
    ret = False
    operators = ['}', '{', '=', ',', '(', '<>', 'OR', 'AND']
    for opr in operators:
        l = len(opr) + 1
#        print 'opr',line[-l:-1]
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
#        tmp = __get_line_from_cleanline(li)
#        if tmp.strip() == '{' or tmp.strip() == '}':
#            continue
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

def _file_type(filename):
    index = filename.find('.')
    while (index != -1):
        filename = filename[index+1:]
        index = filename.find('.')
    return filename

def is_codefile(name):
    if name.lower().endswith(('.c', '.sdl', '.p38', '.cpp')):
        return True

def make_mocks(files, codefile, fname='', dupfile=''):
    codes = Duplication('hashcmp', 10, 10) # hashcmp 10 9
    fn = None
    filenum = 0
    for filename in files:
        if not is_codefile(filename):
            continue
        fn = os.path.basename(filename)
        filenum = filenum + 1
        print filenum, ':', filename
        comms = org_Comments_test()
        cleanlines = comms._remove_comments(filename)
        cleanlines = __combine_lines(cleanlines)
        __print_list_to_another_file(cleanlines, codefile)
        __count_cc_and_display_for_one_file(fn, codefile, codes, fname)
    if fn:
        __display_duplic(codes, dupfile+'.'+_file_type(fn))
    return

def test_is_elif():
    bb = Block('any state', Sdl.TYPE_INPUT, 'adafd')
    for line in ['(a+b):=', 'daf):', '/*adfasdf*/ (T):/*adfadsf*/', '(0):    /*adfadfadf*/', '(UNIT_TYPE_T):', '(>10):', '(\=10):']:
        print line, bb._is_elif(line)   

def make_up_name(path, names):
    full_names = []
    for name in names:
        name = path + '/' + name
        full_names.append(name)
    return full_names

def ignore_files(name):
    file_name = os.path.basename(name)
    if file_name.startswith('.'):
        return True


def ignore_dirs(name):
    dir_name = os.path.basename(name)
    if dir_name in ('tst', 'build'):
        return True
    elif dir_name.startswith('.'):
        return True
    elif name.endswith('SS_LNXfu/src/examples'):
        return True

def list_all_files(path,  files):
    names = os.listdir(path)
    full_names = make_up_name(path, names)
    for name in full_names:
        if os.path.isfile(name) and not ignore_files(name):
            files.append(name)
        elif os.path.isdir(name) and not ignore_dirs(name): 
            list_all_files(name, files)
            
    return files

def search2(list, value):  
    low = 0   
    high = len(list) - 1
    index = 0
       
    while(low <= high):  
        mid = (low + high)/2  
        midval = list[mid]  
      
        if midval < value:  
            low = mid + 1
            index = low   
        elif midval > value:  
            high = mid - 1
            index = mid
        else:    
            return -1, mid     
    return index, -1  

if __name__ == "__main__":
    path = r'T:\cleancode\2015\top9\fac3d5838e-master-58e5a352a1dd4104135174f7a8cef5d8f9d9c198\src'
#    path = r'D:\files\useful_tools\sardne\coach\Cyclomatic_Complexity\c_src'
    codefile = './codes.log'
    dupfile = './duplication'
    files = []
    from time import clock
    print 'start to analyze codes in folder:%s' % path
    import cProfile
    import time
    print 'start at:', time.strftime("%d/%m/%Y %H:%M:%S")
    start=clock()
    files = list_all_files(path, files)
    print len(files), 'files in the folder' 
#    print files
    cProfile.run("make_mocks(files, codefile, '%s.cc.log'% os.path.basename(path), dupfile)")
#    make_mocks(files, codefile, '%s.cc.log'% os.path.basename(path), dupfile)
    finish=clock()
    print (finish-start), 'sec'
    print 'end at:', time.strftime("%d/%m/%Y %H:%M:%S")