from acora import AcoraBuilder
import pdb

class logSearch():


    def match_lines(self,s, *keywords):
        '''
        Searching for the specific keywords
 
        @param s  The Filename.
        @param Keywords  The List which contains two keywords (index 0 - is primary key and index 1 is the parameter).
        
        @returns Lines where the keywords present.
        '''
       
        builder = AcoraBuilder('\r', '\n', *keywords)
        ac = builder.build()
       
        line_start = 0
        matches = False
        for kw, pos in ac.finditer(s):
            if kw in '\r\n':
                if matches:
                    yield s[line_start:pos]
                    matches = False
                line_start = pos + 1
            else:
                matches = True
        if matches:
            yield s[line_start:]

    
    def keywordSearch(self, logFileName, *keywordToSearch):
        
        '''
        Passing the File and keywords to search to Match_lines()
 
        @param logFileName  The Filepath or the String.
        @param Keywords  The List which contains two keywords (index 0 - is primary key and index 1 is the parameter).
        
        @returns Latest line if there are more than one matching.
        
        '''
        
        n = [] 
        j = self.match_lines(logFileName, keywordToSearch[0])
        
        for line in j:
            
            k = self.match_lines(line,keywordToSearch[1])
           
            for next in k:
                n.append(next)
        print "*************************************************************"
        print "Matched Value is:", n
        
        print "*************************************************************"   
        return n   
              
