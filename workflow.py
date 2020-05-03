from gwf import Workflow
from templates import *
import glob

files1 = sorted(glob.glob('data/*_R1.fastq'))
files2 = sorted(glob.glob('data/*_R2.fastq'))
files = list(zip(files1, files2))
rg = 'data/refGen.fa'

gwf = Workflow()

gwf.target_from_template('bwaIndex',
                         bwa_index(fa=rg,
                                   amb=rg + '.amb',
                                   ann=rg + '.ann',
                                   bwt=rg + '.bwt',
                                   pac=rg + '.pac',
                                   sa=rg + '.sa'))

bam_files = []

for i in range(len(files)):
        gwf.target_from_template('bwaMapping_{}'.format(files[i][0][11:16]),
                                 bwa_map(fa=rg,
                                         fq1=files[i][0],
                                         fq2=files[i][1],
                                         output='results/mapped_{}.bam'.format(
                                             files[i][0][11:16])
                                         ))

        gwf.target_from_template('samtoolsSort_{}'.format(files[i][0][11:16]),
                                 samtools_sort(
                                     mapped='results/mapped_{}.bam'.format(
                                         files[i][0][11:16]),
                                     sorted_='results/sorted_{}.bam'.format(
                                         files[i][0][11:16])
                                     ))

        gwf.target_from_template('samtoolsIndex_{}'.format(files[i][0][11:16]),
                                 samtools_index(
                                     bam='results/sorted_{}.bam'.format(
                                         files[i][0][11:16]),
                                     bai='results/sorted_{}.bam.bai'.format(
                                         files[i][0][11:16])
                                     ))

        bam_files.append('results/sorted_{}.bam'.format(files[i][0][11:16]))

gwf.target_from_template('bamList',
                         bam_list(bam=bam_files,
                                  bl='results/bam_list.txt'
                                  ))

gwf.target_from_template('bcftoolsCall',
                         bcftools_call(fa=rg,
                                       bamlist='results/bam_list.txt',
                                       output='results/calls.vcf'
                                        ))
