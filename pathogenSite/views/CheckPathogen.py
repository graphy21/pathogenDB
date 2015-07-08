import os
import json
import sys
import sqlite3
import MySQLdb
from collections import OrderedDict

PATHOGEN_DB_HOST = "147.46.65.202"
USER = "chunlab"
PASSWORD = "tprbs8153"
"""
PATHOGEN_DB_HOST = "127.0.0.1"
USER = "graphy21"
PASSWORD = "1234"
"""

CUTOFF_HIT1 = 0.97
CUTOFF_GAP = 0  # diff between hit1_sim, hit2_sim 

PATH_DATA = '/data/home/graphy21/pipeline/pathogenPipeline/data/taxonomy'
MICROBIOME_CLASSIFICATION_FILE = os.path.join(PATH_DATA,\
		'taxfulltree.txt')
ACC2NAME_FILE = os.path.join(PATH_DATA, 'acc2name.tsv')
PATHOGEN_ID = {
		'0': 'NA',
		'1': 'Not Pathogen',
		'2': 'Not Known',
		'3': 'Pathogen',
		'4': 'Opportunistic Pathogen',
}
RANK = {
		'root' : '0',
		'domain' : '0',
		'kingdom' : '1',
		'subkingdom' : '2',
		'phylum' : '3',
		'subphylum' : '4',
		'class' : '5',
		'subclass' : '6',
		'order' : '7',
		'suborder' : '8',
		'family' : '9',
		'subfamily' : '10',
		'genus' : '11',
		'species' : '12',
		'subspecies' : '13',
		'strain' : '14',
}
RANK_REV = {value:key for key,value in RANK.items() if key != 'root'}
RANK_ORDER = ['domain', 'kingdom', 'subkingdom', 'phylum', 'subphylum', 
		'class', 'subclass', 'order', 'suborder', 'family', 'subfamily', 
		'genus', 'species']



class CLCparser:
	def __init__(self, file_):
		self.clc_file = file_
		self.conn = sqlite3.connect(self.clc_file)
		self.cursor = self.conn.cursor()

	def __del__(self):
		self.conn.commit()
		self.conn.close()

	def get_tables(self):
		"""
		return table names as a list
		"""
		query = "select name from sqlite_master where type= 'table';"
		records = self.cursor.execute(query).fetchall()
		return [record[0] for record in records]

	def get_row_count(self, table):
		"""
		return int
		"""
		query = "select count() from {}".format(table)
		return self.cursor.execute(query).fetchone()[0]

	def schema_fields(self, schema):
		import re
		m = re.search(r"CREATE\s+TABLE\s+(\S+)\s*\(([\s\S]+)\)", schema, re.M)
		if m is None: raise ValueError("Unable to parse schema")
		return [x.split()[0].strip() for x in m.group(2).split(",")]

	def get_table_fields(self, table):
		"""
		return table field as a list
		"""
		query = "select sql from sqlite_master where type='table' "+\
				"and name='{}'".format(table)
		record = self.cursor.execute(query).fetchone()
		if record is None: return []
		return self.schema_fields(record[0])

	def get_record(self, table, return_count=None):
		"""
		then tuple of tuple.
		"""
		if return_count is not None:
			query = "select * from {0} limit {1}".format(table, return_count)
		else:
			query = "select * from {0}".format(table)
		results = self.cursor.execute(query)
		return results.fetchall()

	def get_field(self, table, field, return_count=None):
		"""
		iterator will be returned.
		"""
		if return_count is not None:
			query = "select {0} from {1} limit {2}".\
					format(field, table, return_count)
		else:
			query = "select {0} from {1}".format(field, table)
		results = self.cursor.execute(query)
		return results.fetchall()

	def get_field_with_where(self, table, field, where_field, where_value):
		"""
		return tuple of tuple.
		"""
		query = "select {0} from {1} where {2}='{3}'".format(field, table, 
				where_field, where_value)
		return self.cursor.execute(query).fetchall()


class MySQLdbParser:
	def __init__(self, host, user, passwd, dbname):
		self.host = host
		self.user = user
		self.passwd = passwd
		self.dbname = dbname
		self.db = MySQLdb.connection(db=self.dbname, user=self.user, 
				passwd=self.passwd, host=host)
		self.db.set_character_set('utf8')

	def __del__(self):
		self.db.close()

	def execute_query(self, query):
		"""
		return tuples of tuples. such as ((rec1.1, rec1.2), (rec2.1, rec2.2))
		"""
		self.db.query(query)
		result = self.db.use_result()
		records = result.fetch_row(maxrows=0)
		return records
	
	def get_record(self, table):
		query = "select * from {}".format(table)
		return self.execute_query(query)

	def get_record_with_where(self, table, where_field, where_value):
		query = "select * from {0} where {1}='{2}'".\
				format(table, where_field, where_value)
		return self.execute_query(query)

	def get_record_with_where_phrase(self, table, where_phrase):
		query = "select * from {0} where {1}".format(table, where_phrase)
		return self.execute_query(query)

	def get_field_with_where(self, table, field, where_field, where_value):
		query = "select {0} from {1} where {2}='{3}'".\
				format(field, table, where_field, where_value)
		return self.execute_query(query)


class TaxonomyNode:
	def __init__(self, name, rank, parent_node):
		"""
		rank is "string" such as "domain", "kingdom".
		"""
		self.name = name
		self.rank = rank
		self.parent_node = parent_node
		self.children = []
	
	def set_children(self, child_node):
		self.children.append(child_node)


def get_parent_info(node, end_rank, data={}):
	rank = node.rank
	name = node.name
	if (end_rank not in RANK_ORDER):
		raise ValueError('end_rank is not RANK')
	if int(RANK[rank]) < int(RANK[end_rank]):
		raise ValueError("node's rank is upper than end_rank")
	data[rank] = node.name
	if node.rank == end_rank:
		return data
	get_parent_info(node.parent_node, end_rank, data)
	return data
	



class TaxonomyTree:
	def __init__(self, file_):
		self.file_ = file_
		self.nodes_list = []
		self.nodes_index = {}
		self.parseFile()
	
	def parseFile(self):
		with open(self.file_) as f:
			line = f.readline() # skip title
			line = f.readline()
			name, depth, parent = line.strip().split('|')
			root_node = TaxonomyNode(name, 'root', '')
			self.nodes_list.append(root_node)
			self.nodes_index[name] = root_node
			line = f.readline()
			while line:
				sp = line.strip().split('|')
				if len(sp) != 3:
					break
				name, depth, parent = sp
				parent_node = self.nodes_list[int(parent)]
				node = TaxonomyNode(name, RANK_REV[depth], parent_node)
				self.nodes_list.append(node)
				self.nodes_index[name] = node
				parent_node.set_children(node)
				line = f.readline()

	def get_nodes(self):
		return self.nodes_list

	def get_nodes_index(self):
		return self.nodes_index
	

class MicrobiomeClassificationTree:
	def __init__(self, file_):
		self.file_ = file_
		self.tree = TaxonomyTree(self.file_)
		self.nodes_list = self.tree.get_nodes()
		self.nodes_index = self.tree.get_nodes_index()

	def get_rank(self, name):
		node = self.nodes_index.get(name)
		return (node.rank if node else None)

	def get_parent_info(self, name):
		node = self.nodes_index.get(name)
		parent_node = node.parent_node
		return (parent_node.name, parent_node.rank)
	
	def get_name(self, id):
		if type(id) != int:
			id = int(id)
		return self.nodes_list[id].name

	def get_node_by_name(self, name):
		return self.nodes_index[name]

	def get_node_by_id(self, id):
		return self.nodes_list[id]


class AccNameConverter:
	def __init__(self):
		self.acc2name = {}
		self.name2acc = {}
		self.populate_acc2name()
		self.populate_name2acc()
	
	def populate_acc2name(self):
		with open(ACC2NAME_FILE) as f:
			line = f.readline()
			while line:
				sp = line.strip().split('\t')
				self.acc2name[sp[0]] = sp[1]
				line = f.readline()

	def populate_name2acc(self):
		for key,value in self.acc2name.items():
			self.name2acc[value] = key

	def get_name(self, acc):
		return self.acc2name.get(acc)
		
	def get_acc(self, name):
		return self.name2acc.get(name)


class Reporter:
	"""
	The name in "taxonomyfulltree.txt" is species name standard. 
	"""
	def __init__(self, clc_file):
		self.clc_file = clc_file
		self.cp = CLCparser(self.clc_file)
		self.sp = MySQLdbParser(PATHOGEN_DB_HOST, USER, PASSWORD, 'ssu_prok')
		self.pp = MySQLdbParser(PATHOGEN_DB_HOST, USER, PASSWORD, 'pathogen')
		self.mc = MicrobiomeClassificationTree(MICROBIOME_CLASSIFICATION_FILE)
		self.converter = AccNameConverter()

		self.assigned_node = []

		self.clc_total_read_count = self.cp.get_row_count('raw_read')
		self.micro_dist = {} # {'genus': {'name1':count}, 'species':..}
		self.pathogen_info = {}
		self.tax_group = {} # {'species1': 'representative_name'}
		self.tax_group_info = {} # {'representative_name': 'species1, species2'}
		self.log = {}

		self.populate_tax_group()
		self.populate_pathogen_by_profile_mc()
		#self.populate_pathogen_by_assign()
	
	def populate_tax_group(self):
		"""
		populate "tax_group", "tax_group_info" variables.
		"""
		tax_groups = self.sp.get_record('tax_group')
		for tax_group in tax_groups:
			representative = tax_group[1]
			species = tax_group[2].split('|')
			self.tax_group_info[representative] = ', '.join(species)
			for comp in species:
				self.tax_group[comp] = representative

	def populate_pathogen_by_profile_mc(self):
		log_pathogen = 0
		log_species = 0
		log_filter = 0
		records = self.cp.get_record('profile_mc')
		for record in records: 
			uid, count = record
			node = self.mc.get_node_by_id(uid)
			name = node.name
			rank = node.rank

			try:
				self.micro_dist[rank][name] = count
			except KeyError:
				self.micro_dist[rank] = {name : count}
			# check species
			if rank != 'species':
				continue
			log_species += count
			# check minimum count
			if count < 2:
				continue
			log_filter += count
			# check tax group
			rep_name = name
			is_group = False
			if name.strip().split()[-1] == 'group':
				is_group = True
				rep_name = ' '.join(name.strip().split()[:-1])
			# get_pathogen_info
			pathogen_record = self.pp.get_record_with_where('nomen_with_acc', 
					'name', rep_name)
			if not pathogen_record:
				continue
			log_pathogen += count
			pathogen_record = pathogen_record[0]
			# make data
			informations = {
				'is_group': is_group,
				'species': name,
				'basonym': pathogen_record[9],
				'taxonomy_group': self.tax_group_info.get(rep_name),
				'pathogen_human': pathogen_record[25],
				'pathogen_animal': pathogen_record[26],
				'pathogen_plant': pathogen_record[27],
				'pathogen_disease_kor': pathogen_record[32],
				'pathogen_disease': pathogen_record[33],
				'pathogen_route_kor': pathogen_record[34],
				'pathogen_route': pathogen_record[35],
				'pathogen_symptom_kor': pathogen_record[36],
				'pathogen_symptom': pathogen_record[37],
				'pathogen_prognosis_kor': pathogen_record[38],
				'pathogen_prognosis': pathogen_record[39],
				'pathogen_treatment_kor': pathogen_record[40],
				'pathogen_treatment': pathogen_record[41],
				'pathogen_link': "http://en.wikipedia.org/", #pathogen_record[]
				}
			self.pathogen_info[name] = informations
			#print 'pathogen', name, count
		
		self.log = {'log_pathogen': log_pathogen, 'log_species': log_species,
				'log_filter': log_filter}

	def populate_pathogen_by_assign(self):
		log_assign_count = 0
		log_confirmed = 0
		log_pathogen = 0

		records = self.cp.get_record('assign')
		for record in records:
			confirmed = None 
			acc = record[4]
			hit1_sim = record[5]
			hit2_sim = record[8]
			sequence_uid = record[0]
			# get read_count
			count = 1
			if sequence_uid < 0:
				contig_uid = -(sequence_uid)
				count = self.cp.get_field_with_where('contig', 
						'read_count', 'contig_uid', contig_uid)[0][0]
			log_assign_count += count
			# check confirmed
			if not ((hit1_sim >= CUTOFF_HIT1) and\
					((hit1_sim - hit2_sim) > CUTOFF_GAP)):
				continue
			log_confirmed += count
			# check tax group
			name = self.converter.get_name(acc)
			rep_name = self.tax_group.get(name)
			is_group = True
			if not rep_name:
				rep_name = name
				is_group = False
			# check pathogen
			pathogen_record = self.pp.get_record_with_where('nomen_with_acc', 
					'name', rep_name)
			if not pathogen_record:
				continue
			pathogen_record = pathogen_record[0]
			log_pathogen += count
			# make data
			informations = {
				'is_group': is_group,
				'species': name,
				'basonym': pathogen_record[9],
				'taxonomy_group': self.tax_group_info.get(rep_name),
				'pathogen_human': pathogen_record[25],
				'pathogen_animal': pathogen_record[26],
				'pathogen_plant': pathogen_record[27],
				'pathogen_disease_kor': pathogen_record[32],
				'pathogen_disease': pathogen_record[33],
				'pathogen_route_kor': pathogen_record[34],
				'pathogen_route': pathogen_record[35],
				'pathogen_symptom_kor': pathogen_record[36],
				'pathogen_symptom': pathogen_record[37],
				'pathogen_prognosis_kor': pathogen_record[38],
				'pathogen_prognosis': pathogen_record[39],
				'pathogen_treatment_kor': pathogen_record[40],
				'pathogen_treatment': pathogen_record[41],
				'pathogen_link': "http://en.wikipedia.org/", #pathogen_record[]
				}
			self.pathogen_info[rep_name] = informations

		self.log = {'log_assign_count': log_assign_count, 
				'log_confirmed': log_confirmed,
				'log_pathogen': log_pathogen,}

	def get_clc_file(self):
		return self.clc_file

	def get_log(self):
		return self.log

	def change_format(self, data, format):
		if format == 'json':
			return json.dumps(data)
		elif format == 'python':
			return data

	def get_total_summary(self, format='python', from_rank='species', 
			end_rank='genus'):
		total_summary = [
				[{"label":"From", "type":"string"},
				{"label":"to", "type":"string"},
				{"label":"read count", "type":"number"}]
			]
		pass
		return self.change_format(total_summary, format)

	def get_micro_dist(self, from_rank='species', end_rank='genus', 
			format='python'):
		total_data = []
		all_kinds = self.micro_dist[from_rank]
		for name in all_kinds:
			data = {}
			count = all_kinds[name]
			node = self.mc.get_node_by_name(name)
			data = get_parent_info(node, end_rank, data)
			data['count'] = count
			pathogen_info = self.pathogen_info.get(name)
			if pathogen_info:
				data['pathogen_human'] = pathogen_info['pathogen_human']
				data['pathogen_animal'] = pathogen_info['pathogen_animal']
				data['pathogen_plant'] = pathogen_info['pathogen_plant']
				data['is_pathogen'] = 'Pathogen' 
			else:                  
				data['pathogen_human'] = 0
				data['pathogen_animal'] = 0
				data['pathogen_plant'] = 0
				data['is_pathogen'] = 'Non Pathogen'
			total_data.append(data)
		return self.change_format(total_data, format)

	def get_pathogen_info(self, format='python'):
		pass

	def check_rank_count(self):
		for rank in self.micro_dist:
			total_kind = len(self.micro_dist[rank].keys())
			total_count = sum([self.micro_dist[rank][k] for k in\
					self.micro_dist[rank]])
			#print rank, total_kind, total_count



def main(clc_file, output_prefix):
	reporter = Reporter(clc_file)
	print '1111', reporter.get_log()



if __name__ == '__main__':
	if len(sys.argv) != 3:
		sys.exit('python this.py [clc_file] [output_prefix]\n')
	main(sys.argv[1], sys.argv[2])
