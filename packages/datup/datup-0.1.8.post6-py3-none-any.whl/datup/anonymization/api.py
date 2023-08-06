'''
The api take the io methods and send it to the root datup folder
'''

from datup.anonymization.data_io_anonymization import (
    data_in,
    data_out,
    variables_pii,
    concatenar,
    concatenar_id,
    organizar,
    profiling,
    normalize,
    observaciones,
    organizar_observaciones,
    eliminar_duplicados
)

from datup.anonymization.masking import (anonimizacion)
from datup.anonymization.elimination import (eliminacion)
