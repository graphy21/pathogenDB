from django.db import models



class FastaFile(models.Model):
	name = models.CharField(max_length=50)
	description = models.TextField()
	attachment = models.FileField(upload_to='fasta_files')


class BlastResult(models.Model):
	description = models.TextField()
	attachment = models.FileField(upload_to='blast_results')


class BlastLog(models.Model):
	execution_date = models.DateTimeField('blast execution date')
	blast_result = models.ForeignKey(BlastResult)
