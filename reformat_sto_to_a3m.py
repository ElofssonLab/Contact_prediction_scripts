import os,sys
from collections import defaultdict


def parse(inputfile, outputfile):
    #os.system('vmtouch -qt {} &'.format(inputfile))

    input_ = open(inputfile)
    output = open(outputfile, 'w')

    data = defaultdict(list)
    reference_seq = []

    for line in input_:
        line = line.strip()
        if line and not line.startswith('#'):
            header, sequence = line.split()
            break

    while True:
        reference_seq.extend((s for s in sequence if s != '-'))
        index = [True if s != '-' else False for s in sequence]
        for line in input_:
            line = line.strip()
            if not line:
                break
            if not line.startswith('#'):
                try:
                    name, seq = line.split()
                    data[name].extend(s if i else s.lower() for s, i in zip(seq, index) if i or s != '-')
                except ValueError:
                    # End of file
                    pass

        try:
            header, sequence = input_.next().split()
        except StopIteration:
            break

    input_.close()
    #os.system('vmtouch -qe {} &'.format(inputfile))

    # Write to file
    output.write(''.join(('>', header, '\n')))
    output.write(''.join(reference_seq))
    output.write('\n')

    for name, seq in data.iteritems():
        output.write(''.join(('>', name, '\n')))
        output.write(''.join(seq))
        output.write('\n')
    output.close()


def assert_equal_a3m(ref_file, check_file):
    new = dict()
    ref = dict()

    check = open(check_file)
    for line in check:
        new[line.strip()] = check.next().strip()
    _this = []
    _head = None
    for line in ref_file:
        if line.startswith('>'):
            sequence = ''.join(_this)
            ref[_head] = sequence

            _head = line.strip()
            _this = []
        else:
            _this.append(line.strip())
    ref[_head] = ''.join(_this)
    del ref[None]

    for ky in ref.keys():
        assert ref[ky] == new[ky]

if __name__ == '__main__':
    import time
    t0 = time.time()
    parse(sys.argv[1], sys.argv[2])
    
    #parse('benchmark/sequence.fa.sto', 'benchmark/output.a3m')
    #print time.time() - t0
    #assert_equal_a3m('benchmark/sequence.fa.a3m','benchmark/output.a3m')

    #parse('data/sequence.fa.sto', 'data/temp.a3m')
    #assert_equal_a3m('data/sequence.fa.a3m', 'data/temp.a3m')
