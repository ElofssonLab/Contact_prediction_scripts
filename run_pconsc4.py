import pconsc4
import sys

from pconsc4.utils import format_contacts_casp
from pconsc4.utils import format_ss3

# input
fasta = sys.argv[1]
alignment = sys.argv[2]

# output:
contact_pc4 = sys.argv[3]
ss_structure = sys.argv[4]
#predict contacs 
model = pconsc4.get_pconsc4()
result = pconsc4.predict_all(model, alignment)

#plot contact map
import matplotlib.pyplot as plt
plt.imshow(result['contacts']['cmap'], cmap='Purples')
plt.savefig('contact_map_B5Y0C2.png', dpi=300)

#define sequence
seq = ''.join(line.strip()
              for line in open(fasta)
              if not line.startswith('>'))
#write contact prediction 
with open(contact_pc4, 'w') as f:
  f.write(format_contacts_casp(result['contacts']['cmap'], seq, min_sep=5, full_precision=False))
#write secondary structure prediction
with open(ss_structure, 'w') as f:
  f.write(pconsc4.utils.format_ss3(result['ss']['ss3']))
