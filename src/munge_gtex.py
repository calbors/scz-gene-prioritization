import vcf
import numpy as np
import xarray as xa

filename = 'foo'
vcf_reader = vcf.Reader(filename=filename)

def read_lines(filename):
    with open(samples_filename, 'r') as fp:
        lines = fp.readlines()

    return [line.rstrip() for line in lines]

class Dataset:
    def __init__(self, filename, typed=True, samples=None):
        self._filename = filename
        self._typed = True

        if samples is None:
            samples = []
            vcf_reader = vcf.Reader(filename)
            record = next(self._vcf_reader)

            for call in record:
                samples.append(call.sample)

        self._samples = samples

    def fetch(self, chrom, start, stop):
        vcf_reader = vcf.Reader(self._filename)

        for record in vcf_reader.fetch(f'chr{chrom}', start, stop):
            x = []

            for sample in self._samples:
                call = record.genotype(sample)

                if self._typed:
                    # GT are e.g. '0/1'
                    gt = 0

                    for i in call.data.GT.split('/'):
                        gt += int(i)

                    x.append(gt)
                else:
                    pl = call.data.PL
                    x.append(pl)

            x = np.array(x)


