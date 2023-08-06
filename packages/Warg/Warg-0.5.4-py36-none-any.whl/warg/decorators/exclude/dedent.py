#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Christian Heider Nielsen'
__doc__ = r'''

           Created on 03/03/2020
           '''

import textwrap


def create_snippet():
  code_snippet = """int main(int argc, char* argv[]) {
  return 0;
}"""
  print(code_snippet)
  pass


def create_snippet_c():
  '''
  textwrap.dedent remove common preeceding whitespaces

  :return:
  '''
  code_snippet = textwrap.dedent("""\
        int main(int argc, char* argv[]) {
            return 0;
        }
    """)
  print(code_snippet)
  pass


create_snippet()
create_snippet_c()
