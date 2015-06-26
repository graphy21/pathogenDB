"""
This script parses CLC community analysis result file to add pathogen 
information and makes MS office result file.
"""
import os
import sys
import sqlite3
import MySQLdb
from collections import OrderedDict

#from DocxMaker import DocxMaker
#from PlotMaker import piePlot

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
		return self.nodes_list[name]


class Reporter:
	def __init__(self, clc_file):
		self.clc_file = clc_file
		self.cp = CLCparser(self.clc_file)
		self.sp = MySQLdbParser(PATHOGEN_DB_HOST, USER, PASSWORD, 'ssu_prok')
		self.pp = MySQLdbParser(PATHOGEN_DB_HOST, USER, PASSWORD, 'pathogen')
		self.mc = MicrobiomeClassificationTree(MICROBIOME_CLASSIFICATION_FILE)

		self.assigned_node = []

		self.clc_total_read_count = 0
		self.micro_dist = {}
		self.tax_group = {}
		self.tax_group_info = {}
		self.processing_log = {}

		self.populate_microbiome_distribution()
		self.populate_tax_group()
		#self.populate_pathogen()
	
	def populate_microbiome_distribution(self):
		"""
		populates "clc_total_read_count", "micro_dist" variable
		"""
		records = self.cp.get_record('profile_mc')
		for record in records:
			uid, count = record
			name = self.mc.get_name(uid)
			rank = self.mc.get_rank(name)
			try:
				self.micro_dist[rank][name] = count
			except:
				self.micro_dist[rank] = {name: count}
		self.clc_total_read_count = self.cp.get_row_count('raw_read')

	def populate_tax_group(self):
		"""
		populate "tax_group", "tax_group_info"
		"""
		tax_groups = self.sp.get_record('tax_group')
		for tax_group in tax_groups:
			representative = tax_group[1]
			species = tax_group[2].split('|')
			self.tax_group_info[representative] = ', '.join(species)
			for comp in species:
				self.tax_group[comp] = representative

	def populate_pathogen(self):
		pass
		log_assign_count = 0
		log_confirmed = 0
		log_having_name = 0
		log_pathogen = 0

		records = self.cp.get_record('assign')
		for record in records:
			confirmed = None 
			acc = record[4]
			hit1_sim = record[5]
			hit2_sim = record[8]
			sequence_uid = record[0]
			# get read_count
			read_count = 1
			if sequence_uid < 0:
				contig_uid = -(sequence_uid)
				read_count = self.cp.get_field_with_where('contig', 
						'read_count', 'contig_uid', contig_uid)[0][0]
			log_assign_count += read_count
			# check confirmed
			if not ((hit1_sim >= CUTOFF_HIT1) and\
					((hit1_sim - hit2_sim) > CUTOFF_GAP)):
				continue
			log_confirmed += read_count
			# get name
			name_record = self.sp.get_record_with_where('seq', 'acc', acc)
			if (not name_record) or (not name_record[0][5]):
				continue
			log_having_name += read_count
			name = name_record[0][5]
			# check tax group
			group_name = self.tax_group.get(name)
			is_group = True
			if not group_name:
				group_name = name
				is_group = False
			# check pathogen
			pathogen_record = self.pp.get_record_with_where('nomen', 'name', 
					group_name)
			if not pathogen_record:
				continue
			log_pathogen += read_count
			# make data
			informations = {
				'is_group': is_group,
				'species': pathogen_record[1],
				'basonym': pathogen_record[8],
				'taxonomy_group': tax_group_info_all.get(group_name),
				'pathogen_human': pathogen_record[24],
				'pathogen_animal': pathogen_record[25],
				'pathogen_plant': pathogen_record[26],
				'pathogen_disease_kor': pathogen_record[31],
				'pathogen_disease': pathogen_record[32],
				'pathogen_route_kor': pathogen_record[33],
				'pathogen_route': pathogen_record[34],
				'pathogen_symptom_kor': pathogen_record[35],
				'pathogen_symptom': pathogen_record[36],
				'pathogen_prognosis_kor': pathogen_record[37],
				'pathogen_prognosis': pathogen_record[38],
				'pathogen_treatment_kor': pathogen_record[39],
				'pathogen_treatment': pathogen_record[40],
				'pathogen_link': "http://en.wikipedia.org/", #pathogen_record[]
				}
			try:
				pathogen_count_human[informations['pathogen_human']][nomen]\
						+= read_count
			except:
				try:
					pathogen_count_human[informations['pathogen_human']][nomen]\
							= read_count
				except:
					pathogen_count_human[informations['pathogen_human']] =\
							{nomen: read_count}
			try:
				pathogen_count_animal[informations['pathogen_animal']][nomen]\
						+= read_count
			except:
				try:
					pathogen_count_animal[informations['pathogen_animal']]\
							[nomen] = read_count
				except:
					pathogen_count_animal[informations['pathogen_animal']] =\
							{nomen: read_count}
			try:
				pathogen_count_plant[informations['pathogen_plant']][nomen]\
						+= read_count
			except:
				try:
					pathogen_count_plant[informations['pathogen_plant']][nomen]\
							= read_count
				except:
					pathogen_count_plant[informations['pathogen_plant']] =\
							{nomen: read_count}
			pathogen_info[nomen] = informations

		print 'RAW_READ COUNT  :: ', total_read_count
		print 'ASSIGN_COUNT    :: ', check_assign_count
		print 'FILTERED COUNT (confirmed)          :: ', check_confirmed
		print 'FILTERED COUNT (pathogen_record)    :: ', check_pathogen_record
		print 'FILTERED COUNT (ssu_prok->pathogen) :: ', check_sp2pp
		print 'PASSED COUNT    :: ', check_pathogen


	def get_clc_file(self):
		return self.clc_file


def make_pathogen_portion_data(pathogen_count):
	portion_data = {}
	for key in pathogen_count:
		count = 0
		for nomen in pathogen_count[key]:
			count += pathogen_count[key][nomen]
		portion_data[PATHOGEN_ID[key]] = count
	return portion_data
	


def make_pathogen_list_data(pathogen_data, total_count, organism):
	pathogen_list_header =\
			[['Pathogen Name', 'Read Count', 'Percentage', 'Pathogen']]
	pathogen_list = []
	for i in ['3', '4']:
		data = pathogen_data.get(i)
		pathogen = PATHOGEN_ID[i]
		if data:
			for name in data:
				read_count = data[name]
				percent = float(read_count)/total_count*100
				row = [name, str(read_count), '{:.1f}%'.format(percent),\
						pathogen]
				pathogen_list.append(row)
	pathogen_list.sort(key=lambda x: -int(x[1]))
	pathogen_list = pathogen_list_header + pathogen_list
	return pathogen_list


def extract_pathogen_list(*args):
	pathogen_list = []
	for pathogen_list_organism in args:
		if len(pathogen_list_organism) > 1:
			for i in range(1, len(pathogen_list_organism)):
				pathogen_list.append(pathogen_list_organism[i][0])
	return pathogen_list


def make_pathogen_table_data(pathogen_info):
	species = pathogen_info['species'] if pathogen_info['species'] else ''
	if pathogen_info['is_group'] and species:
		species = '[GROUP] ' + species
	basonym = pathogen_info['basonym'].replace('|',', ') if\
			pathogen_info['basonym'] else ''
	taxonomy_group = pathogen_info['taxonomy_group'] if\
			pathogen_info['taxonomy_group'] else ''
	pathogen_human = PATHOGEN_ID[pathogen_info['pathogen_human']]
	pathogen_animal = PATHOGEN_ID[pathogen_info['pathogen_animal']]
	pathogen_plant = PATHOGEN_ID[pathogen_info['pathogen_plant']]
	table_data = [
			['Species', species],
			['Basonym', basonym],
			['Taxonomy Group', taxonomy_group],
			['Pathogen Human', pathogen_human],
			['Pathogen Animal', pathogen_animal],
			['Pathogen Plant', pathogen_plant],
	]
	return table_data




def main(clc_file, output_file):
	"""
	"""
	micro_dist_genus = {}
	micro_dist_species = {}
	total_read_count = 0
	pathogen_info = {}
	tax_group_info = {}
	tax_group_info_all = {}
	pathogen_count_human = {} # {1: {'nomen':'read_count'}, 2: .., 3:.., 4:..}
	pathogen_count_animal = {}
	pathogen_count_plant = {}
	run_count = 1

	## read count check variables
	check_cp2sp = 0
	check_sp2pp = 0
	check_pathogen = 0
	check_confirmed = 0
	check_assign_count = 0 ## should be removed

	## make necessary objects
	cp = CLCparser(clc_file)
	pp = MySQLdbParser(PATHOGEN_DB_HOST, USER, PASSWORD, 'pathogen')
	sp = MySQLdbParser(PATHOGEN_DB_HOST, USER, PASSWORD, 'ssu_prok')
	mc = MicrobiomeClassificationTree(MICROBIOME_CLASSIFICATION_FILE)
	dm = DocxMaker(DOCX_TEMPLATE, output_file)

	## get tax_group information
	tax_groups = sp.get_record('tax_group')
	for tax_group in tax_groups:
		representative = tax_group[1]
		species = tax_group[2].split('|')
		tax_group_info_all[representative] = ', '.join(species)
		for comp in species:
			tax_group_info[comp] = representative

	## total microbiome distribution
	records = cp.get_record('profile_mc')
	for record in records:
		uid, count = record; uid = str(uid)
		rank = mc.get_rank(uid) 
		if rank == RANK['genus']:
			micro_dist_genus[mc.get_name(uid)] = count
		elif rank == RANK['species']:
			micro_dist_species[mc.get_name(uid)] = count
	total_read_count = cp.get_row_count('raw_read')

	## get pathogen information
	records = cp.get_record('assign')
	for record in records:
		confirmed = None 
		hit1_sim = record[5]
		hit2_sim = record[8]
		sequence_uid = record[0]
		# get read_count
		read_count = 1
		if sequence_uid < 0:
			contig_uid = -(sequence_uid)
			read_count = cp.get_field_with_where('contig', 'read_count', 
					'contig_uid', contig_uid)[0][0]
		check_assign_count += read_count ## should be removed
		# get confirmed
		if (hit1_sim >= CUTOFF_HIT1) and ((hit1_sim - hit2_sim) > CUTOFF_GAP):
				confirmed = True
		else:
			check_confirmed += read_count
			continue
		# get nomen
		hit1_acc = record[4]
		nomen_record = sp.get_record_with_where('seq', 'acc', hit1_acc)
		if (not nomen_record) or (not nomen_record[0][5]):
			check_cp2sp += read_count
		# get pathogen information from pathogen DB
		if nomen_record and nomen_record[0][5]: # check clc to ssu_prok.seq
			nomen = nomen_record[0][5]
			is_group = False
			if tax_group_info.get(nomen): # change name to tax_group
				nomen = tax_group_info.get(nomen)
				is_group = True
			pathogen_record = pp.get_record_with_where('nomen', 'name', nomen)
			if not pathogen_record:
				check_sp2pp += read_count
			if pathogen_record: # check ssu_prok.seq.name to pathogen.nomen.name
				pathogen_record = pathogen_record[0]
				check_pathogen += read_count
			else:
				continue
			informations = {
				'is_group': is_group,
				'species': pathogen_record[1],
				'basonym': pathogen_record[8],
				'taxonomy_group': tax_group_info_all.get(nomen),
				'pathogen_human': pathogen_record[24],
				'pathogen_animal': pathogen_record[25],
				'pathogen_plant': pathogen_record[26],
				'pathogen_disease_kor': pathogen_record[31],
				'pathogen_disease': pathogen_record[32],
				'pathogen_route_kor': pathogen_record[33],
				'pathogen_route': pathogen_record[34],
				'pathogen_symptom_kor': pathogen_record[35],
				'pathogen_symptom': pathogen_record[36],
				'pathogen_prognosis_kor': pathogen_record[37],
				'pathogen_prognosis': pathogen_record[38],
				'pathogen_treatment_kor': pathogen_record[39],
				'pathogen_treatment': pathogen_record[40],
				'pathogen_link': "http://en.wikipedia.org/", #pathogen_record[]
			}
			try:
				pathogen_count_human[informations['pathogen_human']][nomen]\
						+= read_count
			except:
				try:
					pathogen_count_human[informations['pathogen_human']][nomen]\
							= read_count
				except:
					pathogen_count_human[informations['pathogen_human']] =\
							{nomen: read_count}
			try:
				pathogen_count_animal[informations['pathogen_animal']][nomen]\
						+= read_count
			except:
				try:
					pathogen_count_animal[informations['pathogen_animal']]\
							[nomen] = read_count
				except:
					pathogen_count_animal[informations['pathogen_animal']] =\
							{nomen: read_count}
			try:
				pathogen_count_plant[informations['pathogen_plant']][nomen]\
						+= read_count
			except:
				try:
					pathogen_count_plant[informations['pathogen_plant']][nomen]\
							= read_count
				except:
					pathogen_count_plant[informations['pathogen_plant']] =\
							{nomen: read_count}
			pathogen_info[nomen] = informations

	print 'RAW_READ COUNT  :: ', total_read_count
	print 'ASSIGN_COUNT    :: ', check_assign_count
	print 'FILTERED COUNT (confirmed)          :: ', check_confirmed
	print 'FILTERED COUNT (clc->ssu_prok)      :: ', check_cp2sp
	print 'FILTERED COUNT (ssu_prok->pathogen) :: ', check_sp2pp
	print 'PASSED COUNT    :: ', check_pathogen
	#print 'human', pathogen_count_human, pathogen_count_human.keys()
	#print 'animal', pathogen_count_animal, pathogen_count_animal.keys()
	#print 'plant', pathogen_count_plant, pathogen_count_plant.keys()

	## make report
	# title & sample information
	dm.add_heading('Pathogen Detection Report')
	dm.add_paragraph('Sample Name :  {0}\n\nSource :       {1}\n\n'\
			'Date :         {2}'.format('sample','source','date'))
	# total microbiome distribution
	dm.add_heading('Total Microbiome Distribution (genus)', level=1)
	imgdata = piePlot(micro_dist_genus, total_read_count, .03)
	dm.add_picture(imgdata)
	dm.add_heading('Total Microbiome Distribution (species)', level=1)
	imgdata = piePlot(micro_dist_species, total_read_count, .03,)
	dm.add_picture(imgdata)
	# pathogen portion
	portion_data = make_pathogen_portion_data(pathogen_count_human)
	dm.add_heading('Pathogen Portion (human)', level=1)
	imgdata = piePlot(portion_data)
	dm.add_picture(imgdata)
	portion_data = make_pathogen_portion_data(pathogen_count_animal)
	dm.add_heading('Pathogen Portion (animal)', level=1)
	imgdata = piePlot(portion_data)
	dm.add_picture(imgdata)
	portion_data = make_pathogen_portion_data(pathogen_count_plant)
	dm.add_heading('Pathogen Portion (plant)', level=1)
	imgdata = piePlot(portion_data)
	dm.add_picture(imgdata)
	# pathogen list
	pathogen_list_data_human = make_pathogen_list_data(pathogen_count_human,\
			total_read_count, 'Human')
	dm.add_heading('Pathogen List (Human)', level=1)
	dm.add_pathogen_table(pathogen_list_data_human, 'ColorfulList-Accent1')
	pathogen_list_data_animal = make_pathogen_list_data(pathogen_count_animal,\
			total_read_count, 'Animal')
	dm.add_heading('Pathogen List (Animal)', level=1)
	dm.add_pathogen_table(pathogen_list_data_animal, 'ColorfulList-Accent1')
	pathogen_list_data_plant = make_pathogen_list_data(pathogen_count_plant,\
			total_read_count, 'Plant')
	dm.add_heading('Pathogen List (Plant)', level=1)
	dm.add_pathogen_table(pathogen_list_data_plant, 'ColorfulList-Accent1')	
	# pathogen distribution
	#dm.add_heading('Pathogen Distribution', level=1)

	# pathogen species information
	dm.add_heading('Pathogen Species information', level=1)
	pathogen_list = extract_pathogen_list(pathogen_list_data_human, 
			pathogen_list_data_animal, pathogen_list_data_plant)
	for pathogen in pathogen_list:
		pathogen_table_data = make_pathogen_table_data(pathogen_info[pathogen])
		dm.add_species_table(pathogen_table_data, 'ColorfulList-Accent6')
		dm.add_heading('Pathogen Disease', level=3)
		dm.add_paragraph(pathogen_info[pathogen]['pathogen_disease'],
				check_italic=True)
		dm.add_paragraph(pathogen_info[pathogen]['pathogen_disease_kor'],
				check_italic=True)
		dm.add_heading('Pathogen Route', level=3)
		dm.add_paragraph(pathogen_info[pathogen]['pathogen_route'],
				check_italic=True)
		dm.add_paragraph(pathogen_info[pathogen]['pathogen_route_kor'],
				check_italic=True)
		dm.add_heading('Pathogen Symptom', level=3)
		dm.add_paragraph(pathogen_info[pathogen]['pathogen_symptom'],
				check_italic=True)
		dm.add_paragraph(pathogen_info[pathogen]['pathogen_symptom_kor'],
				check_italic=True)
		dm.add_heading('Pathogen Prognosis', level=3)
		dm.add_paragraph(pathogen_info[pathogen]['pathogen_prognosis'],
				check_italic=True)
		dm.add_paragraph(pathogen_info[pathogen]['pathogen_prognosis_kor'],
				check_italic=True)
		dm.add_heading('Pathogen Treatment', level=3)
		dm.add_paragraph(pathogen_info[pathogen]['pathogen_treatment'],
				check_italic=True)
		dm.add_paragraph(pathogen_info[pathogen]['pathogen_treatment_kor'],
				check_italic=True)






if __name__ == '__main__':
	if len(sys.argv) != 3:
		sys.exit('python this.py [clc file] [output file]\n\n')

	clc_file = sys.argv[1]
	output_file = sys.argv[2]

	main(clc_file, output_file)
