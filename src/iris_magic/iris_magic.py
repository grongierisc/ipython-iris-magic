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

    @line_magic
    def iris(self, line): # pylint: disable=function-redefined,method-hidden
        """Run the cell block of Iris code"""
        if self.conn is None:
            self.create_connection(line)

    @cell_magic
    def iris(self, line, cell): # pylint: disable=function-redefined,method-hidden
        """
        An iris magic
        It can interpret iris code (ObjectScript)
        Returns the result of the code execution
        """
        # check is the line is not empty and if it is a connection string
        if line and not self.conn:
            self.create_connection(line)

        if not self.conn:
            display(HTML("""No connection to IRIS\n
                Please use the line magic to create a connection\n
                Fromat: %%iris iris://<<username>>:<<password>>@<<host>>:<<port>>/<<namespace>>\n
                Example: %%iris iris://superuser:SYS@localhost:1972/USER\n
                """))
            return

        # merge lines into one delimited by spaces
        cell = ' '.join(cell.splitlines()).lstrip()
        rsp = ""
        # f = io.StringIO()
        # with redirect_stdout(f):
            ##class(%Studio.General).Execute()
            ##class(ObjectScript.Kernel.CodeExecutor).CodeResult(,)
            ##self.iris.classMethodVoid("ObjectScript.Kernel.CodeExecutor","CodeResult",cell,"cos")
            # self.iris.classMethodVoid("%Library.Device","ReDirectIO",1)
            # self.iris.classMethodVoid("%Studio.General","Execute",cell)
        rsp = self.iris.functionString("Run","ExecCode",cell)
            # rsp = f.getvalue()

        display(HTML(rsp))

    def create_connection(self, connection_string):
        """Create a connection to IRIS"""
        try:
            if not connection_string.startswith('iris://'):
                display(HTML("""No connection to IRIS\n
                Please use the line magic to create a connection\n
                Fromat: %%iris iris://<<username>>:<<password>>@<<host>>:<<port>>/<<namespace>>\n
                Example: %%iris iris://superuser:SYS@localhost:1972/USER\n
                """))
                return
            engine = create_engine(connection_string)
            self.conn = engine.raw_connection()
            self.iris = intersystems_iris.createIRIS(self.conn)
            self.create_routine()
        except Exception as experr: # pylint: disable=broad-except
            display(HTML(experr))

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
