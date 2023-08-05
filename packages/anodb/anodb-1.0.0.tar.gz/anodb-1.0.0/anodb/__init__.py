#
# This marvelous code is Public Domain.
#

import typing
import logging
import anosql as sql # type: ignore


class DB:
	"""Hides database connection and queries in here.

	The class provides the commit, rollback and close methods,
	and SQL execution methods from anosql.
	"""

	def __init__(self, db: str, conn: str, queries: str, auto_reconnect=True, debug=False):
		"""DB constructor

		- db: database engine, `sqlite` or `postgres`
		- conn: connection string
		- queries: file holding queries for `anosql`
		"""
		logging.info(f"creating DB for {db}")
        # database connection
		self._db = 'sqlite3' if db in ('sqlite3', 'sqlite') else \
			'psycopg2' if db in ('pg', 'postgres', 'postgresql', 'psycopg2') else \
			None
		if self._db is None:
			raise Exception(f"database {db} is not supported")
		self._conn_str = conn
		self._queries_file = queries
		self._debug = debug
		self._auto_reconnect = auto_reconnect
		self._conn = self._connect()
		self._reconn = False
		self._count = {}
        # SQL queries
		self._queries = sql.from_path(queries, self._db)
		# forward queries with inserted database connection
		# self.some_query(args) -> self._queries.some_query(self._conn, args)
		from functools import partial
		for q in self._queries.available_queries:
			setattr(self, q, partial(self._call_query, q))
			self._count[q] = 0

	def _call_query(self, query, *args, **kwargs): 
		"""Forward method call to anosql query

		On connection failure, it will try to reconnect on the next call
		if auto_reconnect was specified.

		This may or may not be a good idea, but it should be: the failure
		raises an exception which should abort the current request, so that
		the next call should be on a different request.
		"""
		if self._debug:
			logging.debug(f"DB y: {query}({args}, {kwargs})")
		if self._reconn and self._auto_reconnect:
			self._reconnect()
		try:
			self._count[query] += 1
			return getattr(self._queries, query)(self._conn, *args, **kwargs)
		except Exception as error:
			logging.info(f"DB {self._db} query {query} failed: {error}")
			# coldly rollback on any error
			try:
				self._conn.rollback()
			except Exception as rolerr:
				logging.warning(f"DB {self._db} rollback failed: {rolerr}")
			# detect a connection error for psycopg2, to attempt a reconnection
			# should more cases be handled?
			if hasattr(self._conn, 'closed') and self._conn.closed == 2 and self._auto_reconnect:
				self._reconn = True
			raise error

	def _connect(self):
		"""Create a database connection."""
		logging.info(f"DB {self._db}: connecting")
		if self._db == 'sqlite3':
			import sqlite3 as db
			return db.connect(self._conn_str, check_same_thread=False)
		elif self._db == 'psycopg2':
			import psycopg2 as db # type: ignore
			return db.connect(self._conn_str)
		else:
			# note: anosql currently supports sqlite & postgres
			raise Exception(f"unexpected db {self._db}")

	def _reconnect(self):
		"""Try to reconnect to database."""
		logging.info(f"DB {self._db}: reconnecting")
		if self._conn is not None:
			# attempt at closing but ignore errors
			try:
				self._conn.close()
			except Exception as error:
				logging.error(f"DB {self._db} close: {error}")
		self._conn = self._connect()
		self._reconn = False

	def connect(self):
		"""Create database connection if needed."""
		if self._conn is None:
			self._conn = self._connect()

	def commit(self):
		"""Commit database transaction."""
		self._conn.commit()

	def rollback(self):
		"""Rollback database transaction."""
		self._conn.rollback()

	def close(self):
		"""Close underlying database connection."""
		self._conn.close()
		self._conn = None

	def __str__(self):
		return f"connection to {self._db} database ({self._conn_str})"
