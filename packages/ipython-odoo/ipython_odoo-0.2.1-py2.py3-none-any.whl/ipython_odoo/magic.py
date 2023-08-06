import sys

from IPython.core.magic import Magics, magics_class, line_magic, cell_magic, line_cell_magic

from ipython_odoo.connect import sweeten
from .tracer import Tracer
from .hierarchy import get_model_attrs, prepare_model_attrs, print_model_attrs
from .tables import print_recorset
from .procurement_rules import print_warehouse_rules


@magics_class
class MyMagics(Magics):

    @line_magic
    def sugar(self, line):
        sweeten(self.shell.user_ns)

    @line_magic
    def t(self, line):
        """records_table"""
        print_recorset(line, self.shell.user_ns)

    @line_magic
    def d(self, line):
        """records_table"""
        print_recorset(line, self.shell.user_ns, diff=True)

    @line_magic
    def h(self, line):
        if '.' in line:
            records_var_name, model_attr_name = line.split('.')
        else:
            records_var_name = line
            model_attr_name = ''

        records = eval(records_var_name, self.shell.user_ns)

        attrs = get_model_attrs(records, model_attr_name)
        prepare_model_attrs(attrs)
        print_model_attrs(attrs)

    @line_magic
    def trace(self, line):
        with Tracer():
            return eval(line, self.shell.user_ns)

    @line_magic
    def rules(self, line):
        print_warehouse_rules(line, self.shell.user_ns)
