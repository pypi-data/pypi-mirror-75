# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Copyright 2020 Daniel Bakkelund
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

import sys
import re

class ArgSyntaxError(Exception):
    def __init__(self, msg):
        super(ArgSyntaxError, self).__init__('Command line argument syntax error - ' + msg)


class args:
    def __init__(self, opts='', kws={}, defaults={}, help={}):
        self._kwTypeMap = kws
        self._opts      = opts
        self._defaults  = defaults
        self._initOpts(opts)
        self._initAttributes()
        self._helpTexts = help
        assert set(help.keys()).issubset(kws.keys())
        
    def parse(self, argv=sys.argv[1:]):
        extr = re.compile(r'(^--(?P<key>\w+)([:](?P<val>.+))?$)|(^-(?P<opts>\w+)$)')

        keysToSet = set(self._kwTypeMap.keys()) - set(self._defaults.keys())

        for arg in argv:
            m = extr.match(arg)
            if not m:
                raise ArgSyntaxError('Illegal argument format: "' + arg + '"')

            if m.group('key') is not None:
                key = m.group('key')
                val = m.group('val')
                if not hasattr(self, key):
                    raise ArgSyntaxError('Unknown argument: "' + key + '"')
                self._setVal(key,val)
                if key in keysToSet:
                    keysToSet.remove(key)
            else: # opts
                opts = m.group('opts')
                assert opts is not None
                for c in opts:
                    if not hasattr(self, c):
                        raise ArgSyntaxError('Unknown option: "' + c + '"')
                    exp = 'self.' + c + ' = True'
                    exec(exp)

        if not len(keysToSet) == 0:
            raise ArgSyntaxError('Missing arguments: %s' % str(list(keysToSet)))

        return self

    def _setVal(self, key, val):
        '''
        Takes a key-value pair of strings and converts them to
        a member variable with the key as member variable name, 
        and the val as the value. The type is resolved using the
        kwTypeMap dictionary.
        '''
                
        typ = self._kwTypeMap[key]
        if typ is list:
            val = '[' + val + ']'
        elif typ is bool:
            val = '"' + self._toBool(val) + '"'
        elif val == 'None':
            typ = NoneInitializer
            val = '"None"'
        elif val is None:
            raise ArgSyntaxError('Empty argument: "--' + key + '"')
        else:
            val = '"' + val + '"'

        exp = 'self.' + key + '=' + typ.__name__ + '(' + val + ')'
        exec(exp)
                
    def _toBool(self, val):
        if val in ['True', 'true', 'T', '1', 'OK', 'ok', 'Y', 'y', 'Yes', 'yes']:
            return '1'
        if val in ['False', 'false', 'F', '0', 'N', 'n', 'No', 'no']:
            return ''
        raise ArgSyntaxError('Illegal boolean token: "' + val + '"')

    def _initOpts(self, opts):
        for o in self._opts:
            exec('self.' + o + ' = False')
            

    def _initAttributes(self):
        for key in self._kwTypeMap:
            if key in self._defaults:
                self._setVal(key, str(self._defaults[key]))
            else:
                exp = 'self.' + key + ' = None'
                exec(exp)

    def usage(self):
        result = self.spec()
        if self._helpTexts is not None:
            result += '\nDetailed instructions:\n'
            for k in self._helpTexts:
                result += self._getKwdFormatLine(k) + ' :\n'
                result += self._getHelpText(k)
                result += '\n'*2
        return result

    def spec(self):
        result =  'Usage: [--<key>[:value]] [-opts]\n'

        result += 'Options:'
        for o in self._opts:
            result += ' -' + o
        result += '\n'

        result += 'Keys:\n'
        for k in self._kwTypeMap:
            result += self._getKwdFormatLine(k) + '\n'

        return result

    def _getKwdFormatLine(self,k):
        result = '   --' + k
        t = self._kwTypeMap[k]
        if t is not None:
            result += ':<' + t.__name__ + '>'
        if k in self._defaults:
            result += ' [default:' + str(self._defaults[k]) + ']'  
        return result

    def _getHelpText(self,k):
        lw  = 75
        ind = ' '*5
        raw = self._helpTexts[k]
        txt = ind
        ll  = 0
        for m in re.finditer(r'([^ \n]*)( |\n|$)', raw):
           tok,sep = (m.group(1),m.group(2))
           txt += tok
           ll  += len(tok)
           if sep == '\n':
               txt += '\n' + ind
               ll  = 0
           elif sep == ' ':
               if ll > lw:
                   txt += '\n' + ind
                   ll = 0
               else:
                   txt += ' '
                   ll  += 1

        return txt

    def __str__(self):
        result = 'args{'
        for o in self._opts:
            result += o + '=' + str(getattr(self,o)) + ','
            
        for k in self._kwTypeMap:
            result += k + '=' + str(getattr(self,k)) + ','

        return result[:-1] + '}'

        

def NoneInitializer(dah):
    assert dah == 'None'
    return None
    
