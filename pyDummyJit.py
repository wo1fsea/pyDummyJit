# -*- coding: utf-8 -*-
"""----------------------------------------------------------------------------
Author:
	Huang Quanyong
	gzhuangquanyong@corp.netease.com
Date:
	2018/9/4
Description:
	pyDummyJit
----------------------------------------------------------------------------"""

import ast
import types
import inspect
import pprint
from textwrap import dedent


class Visitor(ast.NodeVisitor):
	def visit_Module(self, node):
		raise NotImplementedError

	def visit_Name(self, node):
		raise NotImplementedError

	def visit_Num(self, node):
		raise NotImplementedError

	def visit_Bool(self, node):
		raise NotImplementedError

	def visit_Call(self, node):
		raise NotImplementedError

	def visit_BinOp(self, node):
		raise NotImplementedError

	def visit_Assign(self, node):
		raise NotImplementedError

	def visit_FunctionDef(self, node):
		raise NotImplementedError

	def visit_Pass(self, node):
		raise NotImplementedError

	def visit_Lambda(self, node):
		raise NotImplementedError

	def visit_Return(self, node):
		raise NotImplementedError

	def visit_Attribute(self, node):
		raise NotImplementedError

	def visit_Subscript(self, node):
		raise NotImplementedError

	def visit_For(self, node):
		raise NotImplementedError

	def visit_AugAssign(self, node):
		raise NotImplementedError

	def generic_visit(self, node):
		raise NotImplementedError


def ast2tree(node, include_attrs=True):
	def _transform(node):
		if isinstance(node, ast.AST):
			fields = ((a, _transform(b)) for a, b in ast.iter_fields(node))
			if include_attrs:
				attrs = ((a, _transform(getattr(node, a))) for a in node._attributes if hasattr(node, a))
				return node.__class__.__name__, dict(fields), dict(attrs)
			return node.__class__.__name__, dict(fields)
		elif isinstance(node, list):
			return [_transform(x) for x in node]
		elif isinstance(node, str):
			return repr(node)
		return node

	if not isinstance(node, ast.AST):
		raise TypeError('expected AST, got %r' % node.__class__.__name__)
	return _transform(node)


def pformat_ast(node, include_attrs=False, **kws):
	return pprint.pformat(ast2tree(node, include_attrs), **kws)


def get_source(source):
	if isinstance(source, types.ModuleType):
		source = inspect.getsource(source)
	if isinstance(source, types.FunctionType):
		source = inspect.getsource(source)
	if isinstance(source, types.LambdaType):
		source = inspect.getsource(source)
	elif isinstance(source, str):
		source = source
	else:
		raise NotImplementedError

	return dedent(source)


def get_ast(source):
	return ast.parse(get_source(source))


def jit(obj):
	print(pformat_ast(get_ast(obj)))
	return obj


@jit
def A(p: int) -> (int, int):
	d = 100 + 100 + 100
