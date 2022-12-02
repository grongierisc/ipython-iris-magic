from sqlalchemy import create_engine
import intersystems_iris

from IPython.core.magic import (Magics, magics_class, cell_magic, line_magic)
from IPython.display import display,HTML

_ROUTINE = """
ROUTINE ExecCode

Run(cmd)  
        Set tInitIO = $IO
        // we MUST use variable called %Stream that is used by a 
        // mnemonic space created by our routine
        set %Stream=##class(%Stream.TmpCharacter).%New()
        use tInitIO::("^"_$zname)
        do ##class(%Library.Device).ReDirectIO(1)
        // call routine that we want to redirect
        x cmd
        If ##class(%Library.Device).ReDirectIO(0) Use tInitIO
        do %Stream.Rewind()
        // show result
        set res=%Stream.Read()
        // result: Hi there!
        q res

redirects()
#; Public entry points for redirection
wstr(s) Do %Stream.Write(s) Quit
wchr(a) Do %Stream.Write($char(a)) Quit
wnl Do %Stream.Write($char(13,10)) Quit
wff Do %Stream.Write($char(13,10,13,10)) Quit
wtab(n) New chars Set $piece(chars," ",n+1)="" Do %Stream.Write(chars) Quit
rstr(len,time) Quit ""
rchr(time) Quit ""
"""

@magics_class
class IrisMagic(Magics):
    """IRIS Magic"""

    conn = None
    iris = None

    _CONNECTION_ERROR = """
                Please use the line magic to create a connection</br>
                Format: %%iris iris://(username):(password)@(host):(port)/(namespace)</br>
                Example: %%iris iris://superuser:SYS@localhost:1972/USER</br>
                """

    @line_magic('iris')
    def iris_line(self, line):
        """Run the line block of Iris code"""
        self.create_connection(line)

    @cell_magic
    def iris(self, line, cell):
        """
        An iris magic
        It can interpret iris code (ObjectScript)
        Returns the result of the code execution
        """
        # check requirements
        # if line is not empty, it means that the user is trying to create a connection
        if line:
            line = line.strip()
            self.create_connection(line)
        # if line is not empty and the connection is not created, try to create it
        if not self.conn:
            display(HTML(self._CONNECTION_ERROR))
            return

        # merge lines into one delimited by spaces
        cell = ' '.join(cell.splitlines()).lstrip()
        rsp = ""
        try:
            # execute the code
            rsp = self.iris.functionString("Run","ExecCode",cell)
        except Exception as err: # pylint: disable=broad-except
            display(HTML(err))
        # display the result
        if rsp:
            display(HTML(rsp))

    def create_connection(self, connection_string):
        """Create a connection to IRIS"""
        # if a connection is already created, close it
        if self.conn:
            display(HTML("Closing the connection"))
            display(HTML("You cannot access to the variables of the previous connection"))
            self.conn.close()
            self.conn = None
        if not connection_string.startswith('iris://'):
            raise Exception("Invalid connection string")
        # create the slqalchemy engine
        try:
            self.conn = create_engine(connection_string).raw_connection()
        except Exception: # pylint: disable=broad-except
            raise Exception("Can't create a connection to IRIS")
        # create the iris object
        try:
            self.iris = intersystems_iris.createIRIS(self.conn)
        except Exception: # pylint: disable=broad-except
            raise Exception("Can't create a connection to IRIS")
        # create the routine
        try:
            self.create_routine()
        except Exception: # pylint: disable=broad-except
            raise Exception("Can't create the routine")

    def create_routine(self):
        """Create the routine to execute the code"""
        # check if the routine exists
        if self.iris.classMethodBoolean("%Routine","Exists","ExecCode"):
            self.iris.classMethodBoolean("%Routine","Delete","ExecCode")
        # create it
        routine = self.iris.classMethodObject("%Routine","%New","ExecCode")
        # for each line in ExecCode.mac
        # add it to the routine
        for line in _ROUTINE.splitlines():
            routine.invokeVoid("WriteLine",line)
        # save the routine
        routine.invokeVoid("Save")
        # compile the routine
        routine.invokeVoid("Compile")
        # check if the routine is compiled
        if not self.iris.classMethodBoolean("%Routine","Exists","ExecCode"):
            raise Exception("Can't compile the routine")
