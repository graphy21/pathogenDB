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


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class CoordGenusArchaea(models.Model):
    genus = models.CharField(primary_key=True, max_length=100)
    phylum = models.CharField(max_length=100)
    acc = models.CharField(max_length=100, blank=True, null=True)
    coord_x = models.FloatField(blank=True, null=True)
    coord_y = models.FloatField(blank=True, null=True)
    coord_z = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coord_genus_archaea'


class CoordGenusBacteria(models.Model):
    genus = models.CharField(primary_key=True, max_length=100)
    phylum = models.CharField(max_length=100)
    acc = models.CharField(max_length=100, blank=True, null=True)
    coord_x = models.FloatField(blank=True, null=True)
    coord_y = models.FloatField(blank=True, null=True)
    coord_z = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'coord_genus_bacteria'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    user = models.ForeignKey(AuthUser)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Exclude(models.Model):
    acc = models.CharField(primary_key=True, max_length=100)
    created_by = models.CharField(max_length=100)
    stamp_create = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'exclude'


class GeneReca(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    strain = models.CharField(max_length=100, blank=True, null=True)
    strain_type = models.IntegerField()
    status = models.IntegerField()
    length = models.IntegerField()
    acc = models.CharField(unique=True, max_length=50)
    genome_project_acc = models.CharField(max_length=50, blank=True, null=True)
    taxonomy = models.TextField()
    sequence = models.TextField()

    class Meta:
        managed = False
        db_table = 'gene_recA'


class GeneRpob(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    strain = models.CharField(max_length=100, blank=True, null=True)
    strain_type = models.IntegerField()
    status = models.IntegerField()
    length = models.IntegerField()
    acc = models.CharField(unique=True, max_length=50)
    genome_project_acc = models.CharField(max_length=50, blank=True, null=True)
    taxonomy = models.TextField()
    sequence = models.TextField()

    class Meta:
        managed = False
        db_table = 'gene_rpoB'


class Genus(models.Model):
    name = models.CharField(primary_key=True, max_length=200)

    class Meta:
        managed = False
        db_table = 'genus'


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
    genome_size_type_strain = models.IntegerField()
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


class NomenGenomeProperty(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=250)
    genome_strain_count = models.IntegerField()
    genome_size_mean = models.IntegerField()
    genome_acc_type_strain = models.CharField(max_length=50, blank=True, null=True)
    genome_size_type_strain = models.IntegerField()
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

    class Meta:
        managed = False
        db_table = 'nomen_genome_property'


class PairSim(models.Model):
    seq1_uid = models.IntegerField()
    seq2_uid = models.IntegerField()
    similarity = models.FloatField()
    uplink_uid = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pair_sim'


class PreDb(models.Model):
    acc = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=250, blank=True, null=True)
    taxonomy = models.TextField(blank=True, null=True)
    sequence = models.TextField()
    size = models.IntegerField()
    is_excluded = models.IntegerField()
    chimera = models.IntegerField()
    match_acc = models.CharField(max_length=30, blank=True, null=True)
    match_sim = models.FloatField()
    completeness = models.FloatField()
    lack_begin = models.IntegerField()
    lack_end = models.IntegerField()
    ambigous_bases = models.IntegerField()
    is_trimmed = models.IntegerField()
    acc_ver = models.CharField(max_length=30, blank=True, null=True)
    gi = models.IntegerField()
    type = models.IntegerField()
    strain = models.CharField(max_length=250, blank=True, null=True)
    tax_id = models.IntegerField()
    mark1 = models.IntegerField(blank=True, null=True)
    mark2 = models.IntegerField(blank=True, null=True)
    auto_assign = models.IntegerField()
    full_length = models.IntegerField()
    match_tax = models.TextField(blank=True, null=True)
    match_acc_half1 = models.CharField(max_length=30, blank=True, null=True)
    match_sim_half1 = models.FloatField()
    match_acc_half2 = models.CharField(max_length=30, blank=True, null=True)
    match_sim_half2 = models.FloatField()

    class Meta:
        managed = False
        db_table = 'pre_db'


class Seq(models.Model):
    uid = models.AutoField(primary_key=True)
    acc = models.CharField(unique=True, max_length=50)
    acc_ver = models.CharField(max_length=50, blank=True, null=True)
    gi = models.IntegerField()
    tax_id = models.IntegerField()
    name = models.CharField(max_length=200)
    name_formated = models.CharField(max_length=250, blank=True, null=True)
    strain = models.CharField(max_length=200, blank=True, null=True)
    status = models.IntegerField()
    location = models.IntegerField()
    candidatus = models.IntegerField()
    sequence = models.TextField()
    aligned_seq = models.TextField(blank=True, null=True)
    tax = models.TextField(blank=True, null=True)
    tax_ncbi = models.TextField(blank=True, null=True)
    tax_other = models.TextField(blank=True, null=True)
    rep = models.IntegerField(blank=True, null=True)
    intron = models.IntegerField()
    improved = models.IntegerField()
    method = models.IntegerField()
    length = models.IntegerField()
    mark1 = models.IntegerField()
    mark2 = models.IntegerField()
    chimera = models.IntegerField()
    completeness = models.FloatField()
    lack_begin = models.IntegerField()
    lack_end = models.IntegerField()
    ambigous_bases = models.IntegerField()
    genus = models.CharField(max_length=250, blank=True, null=True)
    tag = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    hit_acc = models.CharField(max_length=50, blank=True, null=True)
    hit_sim = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seq'


class SeqComplete(models.Model):
    uid = models.AutoField(primary_key=True)
    acc = models.CharField(unique=True, max_length=50)
    sequence = models.TextField()

    class Meta:
        managed = False
        db_table = 'seq_complete'


class SeqHit(models.Model):
    uid = models.AutoField(primary_key=True)
    seq_acc = models.CharField(max_length=50)
    hit_acc = models.CharField(max_length=50)
    hit_sim = models.FloatField()

    class Meta:
        managed = False
        db_table = 'seq_hit'


class Stats(models.Model):
    uid = models.IntegerField(primary_key=True)
    release_date = models.DateField()
    stamp_update = models.DateTimeField(blank=True, null=True)
    n_citation_eztaxon_all = models.IntegerField()
    n_seq_total = models.IntegerField()
    n_nomen_prok_species_valid = models.IntegerField()
    n_nomen_prok_species_invalid = models.IntegerField()
    n_nomen_prok_species_candidatus = models.IntegerField()
    n_nomen_prok_species_phylotype = models.IntegerField()
    n_nomen_prok_species_non_phylotype = models.IntegerField()
    n_bacteria = models.IntegerField()
    n_archaea = models.IntegerField()
    n_eukarya = models.IntegerField()
    n_cultured_prok = models.IntegerField()
    n_uncultured_prok = models.IntegerField()
    n_nomen_prok_total = models.IntegerField()
    n_nomen_prok_species = models.IntegerField()
    n_nomen_bact_species_valid = models.IntegerField()
    n_nomen_arch_species_valid = models.IntegerField()
    n_nomen_bact_species_invalid = models.IntegerField()
    n_nomen_arch_species_invalid = models.IntegerField()
    n_nomen_bact_species_candidatus = models.IntegerField()
    n_nomen_arch_species_candidatus = models.IntegerField()
    n_nomen_bact_species_phylotype = models.IntegerField()
    n_nomen_arch_species_phylotype = models.IntegerField()
    n_nomen_bact_species_valid_16s = models.IntegerField()
    n_nomen_bact_species_valid_16s_type = models.IntegerField()
    n_nomen_arch_species_valid_16s = models.IntegerField()
    n_nomen_arch_species_valid_16s_type = models.IntegerField()
    n_nomen_bact_species_valid_genome = models.IntegerField()
    n_nomen_bact_species_valid_genome_type = models.IntegerField()
    n_nomen_arch_species_valid_genome = models.IntegerField()
    n_nomen_arch_species_valid_genome_type = models.IntegerField()
    n_nomen_species_in_press = models.IntegerField()
    n_prok_genome_shotgun = models.IntegerField()
    n_prok_metagenome_shotgun = models.IntegerField()
    n_citation_eztaxon = models.IntegerField()
    n_citation_eztaxon_e = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'stats'


class StatsNomenYear(models.Model):
    year = models.IntegerField(primary_key=True)
    count = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stats_nomen_year'


class StatsTaxonomyComposition(models.Model):
    phylum = models.CharField(primary_key=True, max_length=200)
    domain = models.CharField(max_length=200)
    count = models.IntegerField()
    ratio = models.FloatField()

    class Meta:
        managed = False
        db_table = 'stats_taxonomy_composition'


class TaxGroup(models.Model):
    uid = models.AutoField(primary_key=True)
    group_name = models.CharField(unique=True, max_length=250)
    tax_list = models.TextField()
    additional_info = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tax_group'


class TaxGroup20140701Ver(models.Model):
    uid = models.AutoField(primary_key=True)
    group_name = models.CharField(unique=True, max_length=250)
    tax_list = models.TextField()

    class Meta:
        managed = False
        db_table = 'tax_group_20140701_ver'


class TaxNode(models.Model):
    uid = models.AutoField(primary_key=True)
    rank = models.IntegerField()
    name = models.CharField(unique=True, max_length=100)
    uplink = models.CharField(max_length=100)
    extra = models.CharField(max_length=250, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    taxonomy = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tax_node'


class Version(models.Model):
    present_version = models.CharField(primary_key=True, max_length=50)
    released_version = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'version'


class Waiting(models.Model):
    uid = models.AutoField(primary_key=True)
    status = models.IntegerField()
    name = models.CharField(unique=True, max_length=250)
    authors = models.CharField(max_length=250)
    strain = models.CharField(max_length=250)
    acc = models.CharField(unique=True, max_length=50)
    acc_ver = models.CharField(max_length=50, blank=True, null=True)
    gi = models.IntegerField(blank=True, null=True)
    ncbi_taxid = models.IntegerField(blank=True, null=True)
    reference = models.CharField(max_length=250, blank=True, null=True)
    sequence = models.TextField(blank=True, null=True)
    match_acc1 = models.CharField(max_length=100, blank=True, null=True)
    match_sim1 = models.FloatField(blank=True, null=True)
    match_acc2 = models.CharField(max_length=100, blank=True, null=True)
    match_sim2 = models.FloatField(blank=True, null=True)
    match_acc3 = models.CharField(max_length=100, blank=True, null=True)
    match_sim3 = models.FloatField(blank=True, null=True)
    match_acc4 = models.CharField(max_length=100, blank=True, null=True)
    match_sim4 = models.FloatField(blank=True, null=True)
    match_acc5 = models.CharField(max_length=100, blank=True, null=True)
    match_sim5 = models.FloatField(blank=True, null=True)
    match_short_acc1 = models.CharField(max_length=100, blank=True, null=True)
    match_short_sim1 = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'waiting'
