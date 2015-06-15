# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class CLCSample(models.Model):
	uid = models.AutoField(primary_key=True)
	name = models.CharField(unique=False, max_length=250)
	owner = models.ForeignKey(User)
	upload_date = models.DateTimeField(auto_now_add=True)
	clc_file = models.FileField(upload_to='samples')
	

class Nomen(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=250)
    name_kor = models.CharField(max_length=250, blank=True, null=True)
    rank = models.IntegerField()
    status = models.IntegerField()
    authors = models.CharField(max_length=250, blank=True, null=True)
    type_taxon = models.CharField(max_length=250, blank=True, null=True)
    is_type = models.IntegerField()
    basonym = models.TextField(blank=True, null=True)
    taxonomy = models.TextField(blank=True, null=True)
    stamp_insert = models.DateTimeField()
    stamp_update = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    ncbi_taxid = models.IntegerField()
    reference = models.CharField(max_length=250, blank=True, null=True)
    vlist = models.IntegerField(blank=True, null=True)
    wiki_kor = models.TextField(blank=True, null=True)
    wiki_kor_created_by = models.CharField(max_length=50, blank=True, null=True)
    wiki_kor_updated_by = models.CharField(max_length=50, blank=True, null=True)
    wiki_eng = models.TextField(blank=True, null=True)
    wiki_eng_created_by = models.CharField(max_length=50, blank=True, null=True)
    wiki_eng_updated_by = models.CharField(max_length=50, blank=True, null=True)
    wiki_ref = models.TextField(blank=True, null=True)
    pathogen_human = models.IntegerField()
    pathogen_animal = models.IntegerField()
    pathogen_plant = models.IntegerField()
    pathogen_classification = models.IntegerField()
    pathogen_supervision = models.IntegerField()
    pathogen_eng = models.TextField(blank=True, null=True)
    pathogen_kor = models.TextField(blank=True, null=True)
    pathogen_disease_kor = models.TextField(blank=True, null=True)
    pathogen_disease_eng = models.TextField(blank=True, null=True)
    pathogen_route_kor = models.TextField(blank=True, null=True)
    pathogen_route_eng = models.TextField(blank=True, null=True)
    pathogen_symptom_kor = models.TextField(blank=True, null=True)
    pathogen_symptom_eng = models.TextField(blank=True, null=True)
    pathogen_prognosis_kor = models.TextField(blank=True, null=True)
    pathogen_prognosis_eng = models.TextField(blank=True, null=True)
    pathogen_treatment_kor = models.TextField(blank=True, null=True)
    pathogen_treatment_eng = models.TextField(blank=True, null=True)
    other_information_kor = models.TextField(blank=True, null=True)
    other_information_eng = models.TextField(blank=True, null=True)
    source_kor = models.TextField(blank=True, null=True)
    source_eng = models.TextField(blank=True, null=True)
    gc_ratio = models.CharField(max_length=50, blank=True, null=True)
    cell_size = models.CharField(max_length=50, blank=True, null=True)
    growth_temp = models.CharField(max_length=100, blank=True, null=True)
    gram_stain = models.IntegerField()
    morphology = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    pathogen_link = models.TextField(blank=True, null=True)
    genome_strain_count = models.IntegerField()
    genome_size_mean = models.IntegerField()
    genome_acc_type_strain = models.CharField(max_length=50, blank=True, null=True)
    genome_size_type_strain = models.IntegerField(blank=True, null=True)
    genome_size_median = models.IntegerField()
    genome_size_sd = models.IntegerField()
    genome_size_min = models.IntegerField()
    genome_size_max = models.IntegerField()
    genome_gc_type_strain = models.FloatField()
    genome_gc_mean = models.FloatField()
    genome_gc_median = models.FloatField()
    genome_gc_sd = models.FloatField()
    genome_gc_min = models.FloatField()
    genome_gc_max = models.FloatField()
    check_edit_list = models.CharField(max_length=50)
    check_add_list = models.CharField(max_length=50)

    class Meta:
		managed = False
		db_table = 'nomen'


class NomenCopy(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=250)
    name_kor = models.CharField(max_length=250, blank=True, null=True)
    rank = models.IntegerField()
    status = models.IntegerField()
    authors = models.CharField(max_length=250, blank=True, null=True)
    type_taxon = models.CharField(max_length=250, blank=True, null=True)
    is_type = models.IntegerField()
    basonym = models.TextField(blank=True, null=True)
    taxonomy = models.TextField(blank=True, null=True)
    stamp_insert = models.DateTimeField()
    stamp_update = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100, blank=True, null=True)
    ncbi_taxid = models.IntegerField()
    reference = models.CharField(max_length=250, blank=True, null=True)
    vlist = models.IntegerField(blank=True, null=True)
    wiki_kor = models.TextField(blank=True, null=True)
    wiki_kor_created_by = models.CharField(max_length=50, blank=True, null=True)
    wiki_kor_updated_by = models.CharField(max_length=50, blank=True, null=True)
    wiki_eng = models.TextField(blank=True, null=True)
    wiki_eng_created_by = models.CharField(max_length=50, blank=True, null=True)
    wiki_eng_updated_by = models.CharField(max_length=50, blank=True, null=True)
    wiki_ref = models.TextField(blank=True, null=True)
    pathogen_human = models.IntegerField()
    pathogen_animal = models.IntegerField()
    pathogen_plant = models.IntegerField()
    pathogen_classification = models.IntegerField()
    pathogen_eng = models.TextField(blank=True, null=True)
    pathogen_kor = models.TextField(blank=True, null=True)
    pathogen_disease_kor = models.TextField(blank=True, null=True)
    pathogen_disease_eng = models.TextField(blank=True, null=True)
    pathogen_route_kor = models.TextField(blank=True, null=True)
    pathogen_route_eng = models.TextField(blank=True, null=True)
    pathogen_symptom_kor = models.TextField(blank=True, null=True)
    pathogen_symptom_eng = models.TextField(blank=True, null=True)
    pathogen_prognosis_kor = models.TextField(blank=True, null=True)
    pathogen_prognosis_eng = models.TextField(blank=True, null=True)
    pathogen_treatment_kor = models.TextField(blank=True, null=True)
    pathogen_treatment_eng = models.TextField(blank=True, null=True)
    other_information_kor = models.TextField(blank=True, null=True)
    other_information_eng = models.TextField(blank=True, null=True)
    source_kor = models.TextField(blank=True, null=True)
    source_eng = models.TextField(blank=True, null=True)
    gc_ratio = models.CharField(max_length=50, blank=True, null=True)
    cell_size = models.CharField(max_length=50, blank=True, null=True)
    growth_temp = models.CharField(max_length=100, blank=True, null=True)
    gram_stain = models.IntegerField()
    morphology = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    pathogen_link = models.TextField(blank=True, null=True)
    genome_strain_count = models.IntegerField()
    genome_size_mean = models.IntegerField()
    genome_size_median = models.IntegerField()
    genome_size_sd = models.IntegerField()
    genome_size_min = models.IntegerField()
    genome_size_max = models.IntegerField()
    genome_gc_mean = models.FloatField()
    genome_gc_median = models.FloatField()
    genome_gc_sd = models.FloatField()
    genome_gc_min = models.FloatField()
    genome_gc_max = models.FloatField()
    check_edit_list = models.CharField(max_length=50)
    check_add_list = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'nomen_copy'


class NomenFile(models.Model):
    uid = models.AutoField(primary_key=True)
    f_parent_uid = models.IntegerField()
    f_attachment = models.CharField(max_length=200)
    f_file_name = models.CharField(max_length=200)
    f_link = models.CharField(max_length=300)
    f_comment = models.CharField(max_length=500)
    f_type = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'nomen_file'


class PathogenDisease(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=250)
    name_kor = models.CharField(max_length=250)
    rank = models.IntegerField()
    status = models.IntegerField()
    authors = models.CharField(max_length=250)
    type_taxon = models.CharField(max_length=250)
    is_type = models.IntegerField()
    basonym = models.TextField()
    stamp_insert = models.DateTimeField()
    stamp_update = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)
    ncbi_taxid = models.IntegerField()
    reference = models.CharField(max_length=250)
    vlist = models.IntegerField()
    wiki_kor = models.TextField()
    wiki_kor_created_by = models.CharField(max_length=50)
    wiki_kor_updated_by = models.CharField(max_length=50)
    wiki_eng = models.TextField()
    wiki_eng_created_by = models.CharField(max_length=50)
    wiki_eng_updated_by = models.CharField(max_length=50)
    wiki_ref = models.TextField()
    pathogen_human = models.IntegerField()
    pathogen_animal = models.IntegerField()
    pathogen_plant = models.IntegerField()
    pathogen_classification = models.IntegerField()
    pathogen_species = models.CharField(max_length=300)
    pathogen_eng = models.TextField()
    pathogen_kor = models.TextField()
    pathogen_disease_kor = models.TextField()
    pathogen_disease_eng = models.TextField()
    pathogen_route_kor = models.TextField()
    pathogen_route_eng = models.TextField()
    pathogen_symptom_kor = models.TextField()
    pathogen_symptom_eng = models.TextField()
    pathogen_prognosis_kor = models.TextField()
    pathogen_prognosis_eng = models.TextField()
    pathogen_treatment_kor = models.TextField()
    pathogen_treatment_eng = models.TextField()
    other_information_kor = models.TextField()
    other_information_eng = models.TextField()
    source_kor = models.TextField()
    source_eng = models.TextField()
    gc_ratio = models.CharField(max_length=50)
    cell_size = models.CharField(max_length=50)
    growth_temp = models.CharField(max_length=100)
    gram_stain = models.IntegerField()
    morphology = models.TextField()
    comment = models.TextField()
    pathogen_link = models.TextField()
    superkingdom = models.CharField(max_length=50)
    genome_strain_count = models.IntegerField()
    genome_size_mean = models.IntegerField()
    genome_size_median = models.IntegerField()
    genome_size_sd = models.IntegerField()
    genome_size_min = models.IntegerField()
    genome_size_max = models.IntegerField()
    genome_gc_mean = models.FloatField()
    genome_gc_median = models.FloatField()
    genome_gc_sd = models.FloatField()
    genome_gc_min = models.FloatField()
    genome_gc_max = models.FloatField()
    check_edit_list = models.CharField(max_length=50)
    check_add_list = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'pathogen_disease'


class PathogenDiseaseFile(models.Model):
    uid = models.AutoField(primary_key=True)
    f_parent_uid = models.IntegerField()
    f_attachment = models.CharField(max_length=200)
    f_file_name = models.CharField(max_length=200)
    f_link = models.CharField(max_length=300)
    f_comment = models.CharField(max_length=500)
    f_type = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'pathogen_disease_file'


class PathogenPlantBase(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250)
    is_checked = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'pathogen_plant_base'


class PathogenSamples(models.Model):
    uid = models.AutoField(primary_key=True)
    sample_uid = models.IntegerField()
    sample_filename = models.CharField(max_length=200)
    species_name = models.CharField(max_length=200)
    cnt_read = models.IntegerField()
    sum_cnt_read = models.IntegerField()
    hit_1_name = models.CharField(max_length=200)
    avg_sim = models.FloatField()
    hit_2_name = models.CharField(max_length=200)
    avg_sim_2 = models.FloatField()
    gap_1_to_2 = models.FloatField()
    avg_sim_all = models.FloatField()
    pathogen_human = models.CharField(max_length=1)
    pathogen_animal = models.CharField(max_length=1)
    pathogen_plant = models.CharField(max_length=1)
    pathogen_class = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'pathogen_samples'


class PathogenSamples4(models.Model):
    uid = models.AutoField(primary_key=True)
    sample_uid = models.IntegerField()
    sample_filename = models.CharField(max_length=200)
    species_name = models.CharField(max_length=200)
    cnt_read = models.IntegerField()
    sum_cnt_read = models.IntegerField()
    avg_sim = models.FloatField()
    avg_sim_all = models.FloatField()
    pathogen_human = models.CharField(max_length=1)
    pathogen_animal = models.CharField(max_length=1)
    pathogen_plant = models.CharField(max_length=1)
    pathogen_class = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'pathogen_samples_4'


class PathogenSamples5(models.Model):
    uid = models.AutoField(primary_key=True)
    sample_uid = models.IntegerField()
    sample_filename = models.CharField(max_length=200)
    species_name = models.CharField(max_length=200)
    cnt_read = models.IntegerField()
    sum_cnt_read = models.IntegerField()
    avg_sim = models.FloatField()
    avg_sim_2 = models.FloatField()
    gap_1_to_2 = models.FloatField()
    avg_sim_all = models.FloatField()
    pathogen_human = models.CharField(max_length=1)
    pathogen_animal = models.CharField(max_length=1)
    pathogen_plant = models.CharField(max_length=1)
    pathogen_class = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'pathogen_samples_5'


class PathogenSamplesSubinfo(models.Model):
    uid = models.AutoField(primary_key=True)
    samples_filename = models.CharField(max_length=50)
    sum_cnt_read_per_file = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pathogen_samples_subinfo'


class PathogenSampling(models.Model):
    uid = models.AutoField(primary_key=True)
    clc_name = models.CharField(max_length=50)
    read_count = models.SmallIntegerField()
    l_seq = models.SmallIntegerField()
    name_1 = models.CharField(max_length=50)
    name_2 = models.CharField(max_length=50)
    name_3 = models.CharField(max_length=50)
    name_4 = models.CharField(max_length=50)
    name_5 = models.CharField(max_length=50)
    sim_1 = models.FloatField()
    sim_2 = models.FloatField()
    sim_3 = models.FloatField()
    sim_4 = models.FloatField()
    sim_5 = models.FloatField()
    gap_12 = models.FloatField()
    gap_13 = models.FloatField()
    gap_14 = models.FloatField()
    gap_15 = models.FloatField()

    class Meta:
        managed = False
        db_table = 'pathogen_sampling'


class PathogenTaxGroup(models.Model):
    uid = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=250)
    species_name = models.CharField(max_length=250)
    pathogen_human = models.IntegerField()
    pathogen_animal = models.IntegerField()
    pathogen_plant = models.IntegerField()
    pathogen_desc = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'pathogen_tax_group'


class PathogenTest(models.Model):
    uid = models.AutoField(primary_key=True)
    f_sampling_host = models.CharField(max_length=100)
    f_sampling_location = models.CharField(max_length=100)
    f_sampling_tag = models.CharField(max_length=100)
    f_date = models.CharField(max_length=10)
    f_country = models.CharField(max_length=200)
    f_description = models.TextField()
    f_clc_filename = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'pathogen_test'


class PathogenVirus(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=250)
    name_kor = models.CharField(max_length=250, blank=True, null=True)
    name_family = models.CharField(max_length=250, blank=True, null=True)
    name_family_kor = models.CharField(max_length=250, blank=True, null=True)
    rank = models.IntegerField()
    status = models.IntegerField()
    authors = models.CharField(max_length=250, blank=True, null=True)
    type_taxon = models.CharField(max_length=250, blank=True, null=True)
    is_type = models.IntegerField()
    basonym = models.TextField(blank=True, null=True)
    stamp_insert = models.DateTimeField()
    stamp_update = models.DateTimeField()
    created_by = models.CharField(max_length=100)
    updated_by = models.CharField(max_length=100)
    ncbi_taxid = models.IntegerField()
    reference = models.CharField(max_length=250, blank=True, null=True)
    vlist = models.IntegerField(blank=True, null=True)
    wiki_kor = models.TextField(blank=True, null=True)
    wiki_kor_created_by = models.CharField(max_length=50, blank=True, null=True)
    wiki_kor_updated_by = models.CharField(max_length=50, blank=True, null=True)
    wiki_eng = models.TextField(blank=True, null=True)
    wiki_eng_created_by = models.CharField(max_length=50, blank=True, null=True)
    wiki_eng_updated_by = models.CharField(max_length=50, blank=True, null=True)
    wiki_ref = models.TextField(blank=True, null=True)
    pathogen_human = models.IntegerField()
    pathogen_animal = models.IntegerField()
    pathogen_plant = models.IntegerField()
    pathogen_baltimore = models.IntegerField()
    pathogen_supervision = models.IntegerField()
    pathogen_eng = models.TextField(blank=True, null=True)
    pathogen_kor = models.TextField(blank=True, null=True)
    pathogen_disease_kor = models.TextField(blank=True, null=True)
    pathogen_disease_eng = models.TextField(blank=True, null=True)
    pathogen_route_kor = models.TextField(blank=True, null=True)
    pathogen_route_eng = models.TextField(blank=True, null=True)
    pathogen_symptom_kor = models.TextField(blank=True, null=True)
    pathogen_symptom_eng = models.TextField(blank=True, null=True)
    pathogen_prognosis_kor = models.TextField(blank=True, null=True)
    pathogen_prognosis_eng = models.TextField(blank=True, null=True)
    pathogen_treatment_kor = models.TextField(blank=True, null=True)
    pathogen_treatment_eng = models.TextField(blank=True, null=True)
    other_information_kor = models.TextField(blank=True, null=True)
    other_information_eng = models.TextField(blank=True, null=True)
    source_kor = models.TextField(blank=True, null=True)
    source_eng = models.TextField(blank=True, null=True)
    gc_ratio = models.CharField(max_length=50, blank=True, null=True)
    cell_size = models.CharField(max_length=50, blank=True, null=True)
    growth_temp = models.CharField(max_length=100, blank=True, null=True)
    gram_stain = models.IntegerField()
    morphology = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    pathogen_link = models.TextField()
    superkingdom = models.CharField(max_length=50, blank=True, null=True)
    genome_strain_count = models.IntegerField()
    genome_size_mean = models.IntegerField()
    genome_size_median = models.IntegerField()
    genome_size_sd = models.IntegerField()
    genome_size_min = models.IntegerField()
    genome_size_max = models.IntegerField()
    genome_gc_mean = models.FloatField()
    genome_gc_median = models.FloatField()
    genome_gc_sd = models.FloatField()
    genome_gc_min = models.FloatField()
    genome_gc_max = models.FloatField()
    check_edit_list = models.CharField(max_length=50)
    check_add_list = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'pathogen_virus'


class PathogenVirusFile(models.Model):
    uid = models.AutoField(primary_key=True)
    f_parent_uid = models.IntegerField()
    f_attachment = models.CharField(max_length=200)
    f_file_name = models.CharField(max_length=200)
    f_link = models.CharField(max_length=300)
    f_comment = models.CharField(max_length=500)
    f_type = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'pathogen_virus_file'


class Reference(models.Model):
    uid = models.AutoField(primary_key=True)
    acc = models.CharField(unique=True, max_length=20)
    stamp_update = models.DateTimeField(blank=True, null=True)
    stamp_insert = models.DateTimeField()
    year = models.CharField(max_length=30, blank=True, null=True)
    month = models.CharField(max_length=30, blank=True, null=True)
    pub_date = models.DateField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    journal = models.CharField(max_length=250, blank=True, null=True)
    authors = models.TextField(blank=True, null=True)
    editors = models.CharField(max_length=250, blank=True, null=True)
    vol = models.CharField(max_length=250, blank=True, null=True)
    issue = models.CharField(max_length=50, blank=True, null=True)
    pages = models.CharField(max_length=50, blank=True, null=True)
    book_title = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    publisher = models.CharField(max_length=250, blank=True, null=True)
    edition = models.CharField(max_length=50, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    pubstat = models.CharField(max_length=20, blank=True, null=True)
    summary_kor = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reference'


class TblLogPathogen(models.Model):
    uid = models.AutoField(primary_key=True)
    f_user_email = models.CharField(max_length=200)
    f_apply_date = models.DateTimeField()
    f_db = models.CharField(max_length=50)
    f_type = models.CharField(max_length=50)
    f_id = models.CharField(max_length=50)
    f_field = models.CharField(max_length=50, blank=True, null=True)
    f_value = models.TextField(blank=True, null=True)
    f_new_value = models.TextField(blank=True, null=True)
    f_update = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'tbl_log_pathogen'


class User(models.Model):
    email = models.CharField(primary_key=True, max_length=100)
    password = models.CharField(max_length=100)
    country = models.CharField(max_length=101)
    iplogin = models.IntegerField(blank=True, null=True)
    notify = models.IntegerField(blank=True, null=True)
    user_level = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    affiliation = models.CharField(max_length=200, blank=True, null=True)
    stamp_update = models.DateTimeField()
    stamp_insert = models.DateTimeField()
    initials = models.CharField(max_length=30, blank=True, null=True)
    ip = models.CharField(max_length=250, blank=True, null=True)
    ip_login = models.IntegerField()
    database = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
