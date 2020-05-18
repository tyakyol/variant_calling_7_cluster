def bwa_index(fa, amb, ann, bwt, pac, sa):
    '''
    Template for genome indexing.
    '''
    inputs = [fa]
    outputs = [amb, ann, bwt, pac, sa]
    options = {
        'cores': 8,
        'memory': '16g',
        'walltime': '48:00:00'
    }
    spec = '''
bwa index {fa}
    '''.format(fa=fa)
    return inputs, outputs, options, spec


def bwa_map(fa, fq1, fq2, output):
    '''
    Template for mapping short reads to the genome.
    '''
    inputs = [fa, fq1, fq2,
              '{}.amb'.format(fa),
              '{}.ann'.format(fa),
              '{}.bwt'.format(fa),
              '{}.pac'.format(fa),
              '{}.sa'.format(fa)]
    outputs = [output]
    options = {
        'cores': 12,
        'memory': '16g',
        'walltime': '96:00:00'
    }
    spec = '''
bwa mem {fa} {fq1} {fq2} | samtools view -Sb > {output}
'''.format(fa=fa, fq1=fq1, fq2=fq2, output=output)
    return inputs, outputs, options, spec


def samtools_sort(mapped, sorted_):
    '''
    Template for sorting the mapped reads.
    '''
    inputs = [mapped]
    outputs = [sorted_]
    options = {
        'cores': 8,
        'memory': '8g',
        'walltime': '96:00:00'
    }
    spec = '''
samtools sort {mapped} > {sorted_}
    '''.format(mapped=mapped, sorted_=sorted_)
    return inputs, outputs, options, spec


def samtools_index(bam, bai):
    '''
    Template for indexing the sorted reads.
    '''
    inputs = [bam]
    outputs = [bai]
    options = {
        'cores': 4,
        'memory': '8g',
        'walltime': '96:00:00'
    }
    spec = '''
samtools index {bam} {bai}
    '''.format(bam=bam, bai=bai)
    return inputs, outputs, options, spec


def bam_list(bam, bl):
    '''
    Template for generating the bam file list.
    '''
    inputs = []
    for b in bam:
        inputs.append(b)
    outputs = [bl]
    options = {
        'cores': 1,
        'memory': '4g',
        'walltime': '48:00:00'
    }
    spec = '''
ls results/sorted*.bam > {bl}
    '''.format(bl=bl)
    return inputs, outputs, options, spec


def bcftools_call(fa, bamlist, output):
    '''
    Template for variant calling.
    '''
    inputs = [fa, bamlist]
    outputs = [output]
    options = {
        'cores': 12,
        'memory': '16g',
        'walltime': '96:00:00'
    }
    spec = '''
bcftools mpileup -Ou -f {fa} -b {bamlist} |
bcftools call -mv > {output}
    '''.format(fa=fa, bamlist=bamlist, output=output)
    return inputs, outputs, options, spec
