from gwf import Workflow
from templates import *
import glob

files1 = sorted(glob.glob('../../InRoot/Backup/data/01_20200402_137_LjAcessions_fastq/*_R1.fastq'))
files2 = sorted(glob.glob('../../InRoot/Backup/data/01_20200402_137_LjAcessions_fastq/*_R2.fastq'))
files = list(zip(files1, files2))
rg = '../../InRoot/Backup/data/02_20200402_Gifu1.2_ref_data/LjGifu1.1_pseudomol.fa'

gwf = Workflow()

gwf.target_from_template('bwaIndex',
                         bwa_index(fa=rg,
                                   amb=rg+'.amb',
                                   ann=rg+'.ann',
                                   bwt=rg+'.bwt',
                                   pac=rg+'.pac',
                                   sa=rg+'.sa'))

bam_files = []
bai_files = []

for i in range(len(files)):
        gwf.target_from_template('bwaMapping_{}'.format(files[i][0][59:65]),
                                 bwa_map(fa=rg,
                                         fq1=files[i][0],
                                         fq2=files[i][1],
                                         output='results/mapped_{}.bam'.format(
                                             files[i][0][59:65])
                                         ))

        gwf.target_from_template('samtoolsSort_{}'.format(files[i][0][59:65]),
                                 samtools_sort(
                                     mapped='results/mapped_{}.bam'.format(
                                         files[i][0][59:65]),
                                     sorted_='results/sorted_{}.bam'.format(
                                         files[i][0][59:65])
                                     ))

        gwf.target_from_template('samtoolsIndex_{}'.format(files[i][0][59:65]),
                                 samtools_index(
                                     bam='results/sorted_{}.bam'.format(
                                         files[i][0][59:65]),
                                     bai='results/sorted_{}.bam.bai'.format(
                                         files[i][0][59:65])
                                     ))

        bam_files.append('results/sorted_{}.bam'.format(files[i][0][59:65]))
        bai_files.append('results/sorted_{}.bam.bai'.format(files[i][0][59:65]))

gwf.target_from_template('bamList',
                         bam_list(bam=bam_files,
                                  bl='results/bam_list.txt'
                                  ))

gwf.target_from_template('bcftoolsCall',
                         bcftools_call(fa=rg,
                                       bamlist='results/bam_list.txt',
                                       bai=bai_files,
                                       output='results/20200531_raw_variants.vcf'
                                        ))
                                        
gwf.target_from_template('bgzip',
                          bgzip(vcf='results/20200531_raw_variants.vcf',
                                gz='results/20200531_raw_variants.vcf.gz'
                                ))

gwf.target_from_template('tabix',
                         tabix(gz='results/20200531_raw_variants.vcf.gz',
                               tbi='results/20200531_raw_variants.vcf.gz.tbi'
                               ))
