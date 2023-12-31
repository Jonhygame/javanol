class Step(Enum):
    LEXICO = 0
    SINTACTICO = 1
    SEMANTICO = 2

class Main:
    input_file = None
    output_file = None
    output_table = False
    output_ast = False
    step = None

    def print_help (self, arg0):
        print("Uso: % s -i entrada.es -o salida.es [-t] [-a]" % arg0)
        print("     % s -i entrada.es -o salida.es [-l|-p|-s]" % arg0)
        print("     % s -h" % arg0)

    def main(self, argv):
        try:
            opts, args = getopt.getopt(argv[1:], "hi:o:lpsta", [
                "input=", "output=", "lex", "parse", "semantic", "table", "ast"
            ])
        except getopt.GetoptError as err:
            print(err)
            print_help(argv[0]);
            sys.exit(2)

        for o, a in opts:
            if o == "-h":
                self.print_help (argv[0])
            elif o in ("-i", "--input"):
                self.input_file = a
            elif o in ("-o", "--output"):
                self.output_file = a
            elif o in ("-t", "--table"):
                self.output_table = True
            elif o in ("-a", "--ast"):
                self.output_ast = True
            elif o in ("-l", "--lex"):
                self.step = Step.LEXICO
            elif o in ("-p", "--parse"):
                self.step = Step.SINTACTICO
            elif o in ("-s", "--semantic"):
                self.step = Step.SEMANTICO
            else:
                assert False, "opción desconocida"

        if self.input_file and self.output_file:
            table_file = self.input_file + '.tab'
            ast_file = self.input_file + '.ast'
            delete_tab = not self.step and not self.output_table and not os.path.exists(table_file)
            delete_ast = not self.step and not self.output_ast and not os.path.exists(ast_file)
            try:
                if self.step == Step.LEXICO:
                    sys.exit(Lexer(self.input_file).inicio())
                elif self.step == Step.SINTACTICO:
                    sys.exit(Parser(self.input_file).inicio())
                elif self.step == Step.SEMANTICO:
                    print("NOT IMPLEMENTED")
                    sys.exit(1)
                else:
                    if Lexer(self.input_file).inicio() != 0:
                        raise Exception("Error léxico")
                    if Parser(self.input_file).inicio() != 0:
                        raise Exception("Error sintáctico")
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                sys.exit(1)
            if delete_tab:
                os.remove(table_file)
            if delete_ast:
                os.remove(ast_file)
        else:
            self.print_help(argv[0])
            sys.exit(2)

if __name__ == "__main__":
    Main().main(sys.argv)
