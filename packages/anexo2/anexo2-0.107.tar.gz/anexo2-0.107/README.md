[![Build Status](https://travis-ci.org/cluster311/Anexo2.svg?branch=master)](https://travis-ci.org/cluster311/Anexo2)

# Anexo II
Generación para impresión del "Comprobante de Atención de Beneficiarios de Obras Sociales" (Conocido como Anexo II).  
Según [Resolucion 487/2002](http://servicios.infoleg.gob.ar/infolegInternet/anexos/75000-79999/77280/texact.htm).  

```
Art. 2° — Los Hospitales Públicos de Gestión Descentralizada deberán 
  cumplimentar el "Comprobante de Atención de Beneficiarios de Obras Sociales", 
  que se agrega como Anexo II, que pasa a formar parte integrante de la presente 
  Resolución, con carácter de Declaración Jurada, firmado por el médico actuante 
  o Jefe del Servicio, con sello y número de matrícula, y el responsable 
  administrativo del Hospital, con sello, cargo y aclaración de firma, 
  con la correspondiente suscripción o firma del beneficiario, 
  familiar o responsable.
```
Documento original usado de base [acá](originales/Anexo-II-RESOLUCION-487-2002.gif).  

## Herramienta desarrollada

Este instrumento toma un diccionario con datos y genera un HTML listo para imprimir, firmar y sellar. 

## Muestra

![anexo II](imgs/muestra_anexo_ii.png)

## Instalacion 

[![pypi link](imgs/pypi.svg)](https://pypi.org/project/anexo2/)

```
pip install anexo2
```


## Uso

```python
hospital = {'nombre': 'HOSPITAL SAN ROQUE',  # https://www.sssalud.gob.ar/index.php?page=bus_hosp&cat=consultas
            'codigo_hpgd': '4321323'}
            
beneficiario = {'apellido_y_nombres': 'Juan Perez',
                'tipo_dni': 'DNI',  # | LE | LC
                'dni': '34100900',
                'tipo_beneficiario': 'titular',  # | no titular | adherente
                'parentesco': 'conyuge',  # hijo | otro
                'sexo': 'M',  # | F
                'edad': 88}
atencion = {'tipo': 'consulta',  # | practica | internacion
            'especialidad': 'Va un texto al parecer largo, quizas sea del nomenclador',
            'codigos_N_HPGD': ['AA01', 'AA02', 'AA06', 'AA07'],  # no se de donde son estos códigos
            'fecha': {'dia': 3, 'mes': 9, 'anio': 2019},
            'diagnostico_ingreso_cie10': {'principal': 'W020', 'otros': ['w021', 'A189']}}
obra_social = {'codigo_rnos': '800501',
               'nombre': 'OBRA SOCIAL ACEROS PARANA',
               'nro_carnet_obra_social': '9134818283929101',
               'fecha_de_emision': {'dia': 11, 'mes': 9, 'anio': 2009},
               'fecha_de_vencimiento': {'dia': 11, 'mes': 9, 'anio': 2029}}
empresa = {'nombre': 'Telescopios Hubble',
           'direccion': 'Av Astronómica s/n',
           'ultimo_recibo_de_sueldo': {'mes': 7, 'anio': 2019},
           'cuit': '31-91203043-8'}

data = {'dia': 3,
        'mes': 9,
        'anio': 2019,
        'hospital': hospital,
        'beneficiario': beneficiario,
        'atencion': atencion,
        'obra_social': obra_social,
        'empresa': empresa
        }

from anexo2.docs import Anexo2
anx = Anexo2(data=data)
save_to = 'path.html'
res = anx.get_html(save_path=save_to)
if res is None:
    print('ERRORES al procesar pedido')
    for field, error in anx.errors.items():
        print(f' - {field}: {error}')
else:
    print(f'Procesado correctamente y grabado en {save_to}')
```

## Validación de los datos
Internamente se usa la librería [cerberus](https://docs.python-cerberus.org/en/stable/validation-rules.html) para validar los datos.  
**Ninguno de los campos es requerido** y los que estén ausentes no se completarán en el html.  

Aquí se puede ver el esquema de validación: 

```python
from anexo2.docs import Anexo2
anx = Anexo2(data={})
anx.get_schema()
```

```
{
	'dia': {
		'type': 'integer',
		'min': 1,
		'max': 31
	},
	'mes': {
		'type': 'integer',
		'min': 1,
		'max': 12
	},
	'anio': {
		'type': 'integer',
		'min': 2019,
		'max': 2030
	},
	'hospital': {
		'type': 'dict',
		'schema': {
			'nombre': {
				'type': 'string'
			},
			'codigo_hpgd': {
				'type': 'string'
			}
		}
	},
	'beneficiario': {
		'type': 'dict',
		'schema': {
			'apellido_y_nombres': {
				'type': 'string'
			},
			'tipo_dni': {
				'type': 'string',
				'allowed': ['DNI', 'LE', 'LC']
			},
			'dni': {
				'type': 'string'
			},
			'tipo_beneficiario': {
				'type': 'string',
				'allowed': ['titular', 'no titular', 'adherente']
			},
			'parentesco': {
				'type': 'string',
				'allowed': ['conyuge', 'hijo', 'otro']
			},
			'sexo': {
				'type': 'string',
				'allowed': ['F', 'M']
			},
			'edad': {
				'type': 'integer',
				'min': 0,
				'max': 110
			}
		}
	},
	'atencion': {
		'type': 'dict',
		'schema': {
			'tipo': {
				'type': 'string',
				'allowed': ['consulta', 'practica', 'internacion']
			},
			'especialidad': {
				'type': 'string'
			},
			'codigos_N_HPGD': {
				'type': 'list'
			},
			'fecha': {
				'type': 'dict',
				'schema': {
					'dia': {
						'type': 'integer',
						'min': 1,
						'max': 31
					},
					'mes': {
						'type': 'integer',
						'min': 1,
						'max': 12
					},
					'anio': {
						'type': 'integer',
						'min': 2019,
						'max': 2030
					}
				}
			},
			'diagnostico_ingreso_cie10': {
				'type': 'dict',
				'schema': {
					'principal': {
						'type': 'string'
					},
					'otros': {
						'type': 'list'
					}
				}
			}
		}
	},
	'obra_social': {
		'type': 'dict',
		'schema': {
			'codigo_rnos': {
				'type': 'string'
			},
			'nombre': {
				'type': 'string'
			},
			'nro_carnet_obra_social': {
				'type': 'string'
			},
			'fecha_de_emision': {
				'type': 'dict',
				'schema': {
					'dia': {
						'type': 'integer',
						'min': 1,
						'max': 31
					},
					'mes': {
						'type': 'integer',
						'min': 1,
						'max': 12
					},
					'anio': {
						'type': 'integer',
						'min': 1970,
						'max': 2030
					}
				}
			},
			'fecha_de_vencimiento': {
				'type': 'dict',
				'schema': {
					'dia': {
						'type': 'integer',
						'min': 1,
						'max': 31
					},
					'mes': {
						'type': 'integer',
						'min': 1,
						'max': 12
					},
					'anio': {
						'type': 'integer',
						'min': 2019,
						'max': 2030
					}
				}
			}
		}
	},
	'empresa': {
		'type': 'dict',
		'schema': {
			'nombre': {
				'type': 'string'
			},
			'direccion': {
				'type': 'string'
			},
			'ultimo_recibo_de_sueldo': {
				'type': 'dict',
				'schema': {
					'dia': {
						'type': 'integer',
						'min': 1,
						'max': 31
					},
					'mes': {
						'type': 'integer',
						'min': 1,
						'max': 12
					},
					'anio': {
						'type': 'integer',
						'min': 1970,
						'max': 2030
					}
				}
			},
			'cuit': {
				'type': 'string'
			}
		}
	}
}
```
