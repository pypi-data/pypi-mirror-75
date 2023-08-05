#cython: language_level=3

cimport cython
from obitools3.dms.view.view cimport Line
from obitools3.utils cimport bytes2str_object, str2bytes, tobytes
from obitools3.dms.column.column cimport Column_line, Column_multi_elts


cdef class TabFormat:
    
    def __init__(self, header=True, bytes NAString=b"NA", bytes sep=b"\t"):
        self.header = header
        self.first_line = True
        self.NAString = NAString
        self.sep = sep
        
    @cython.boundscheck(False)    
    def __call__(self, object data):
        
        line = []
        
        if self.first_line:
            self.tags = [k for k in data.keys()]
        
        for k in self.tags:
            
            if self.header and self.first_line:
                if isinstance(data.view[k], Column_multi_elts):
                    for k2 in data.view[k].keys():
                        line.append(tobytes(k)+b':'+tobytes(k2))
                else:
                    line.append(tobytes(k))
            else:
                value = data[k]
                if isinstance(data.view[k], Column_multi_elts):
                    if value is None:  # all keys at None
                        for k2 in data.view[k].keys(): # TODO could be much more efficient
                            line.append(self.NAString)
                    else:
                        for k2 in data.view[k].keys(): # TODO could be much more efficient
                            if value[k2] is not None:
                                line.append(str2bytes(str(bytes2str_object(value[k2]))))  # genius programming
                            else:
                                line.append(self.NAString)
                else:
                    if value is not None:
                        line.append(str2bytes(str(bytes2str_object(value))))
                    else:
                        line.append(self.NAString)
                  	
        if self.first_line:
            self.first_line = False
      		
        return self.sep.join(value for value in line)
