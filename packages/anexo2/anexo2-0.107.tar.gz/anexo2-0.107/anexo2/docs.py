import os
from jinja2 import Template, FileSystemLoader, Environment
# validacion con cerberus https://docs.python-cerberus.org/en/stable/usage.html
from cerberus import Validator

class Anexo2:
    """ Generacion del Anexo II """

    here = os.path.dirname(os.path.realpath(__file__))
    templates_folder = os.path.join(here, 'templates')

    errors = {}  # errores al procesar los datos {campo: error}

    def __init__(self, data):
        self.validator = Validator(self.get_schema())
        self.data = data
        loader = FileSystemLoader(self.templates_folder)
        self.jinja_environment = Environment(loader=loader)

    def get_html(self, template_name='anexo2', save_path=None):
        """
        recibe los datos a "dibujar", graba el HTML (si se lo pide)
        y devuelve:
            None si hay errores
            el código HTML si está todo OK
        TODO generar PDF: https://github.com/fdemmer/django-weasyprint
        """
        data = self.data
        
        res, errors = self.validate_data(data=data)
        if not res:
            self.errors = errors
            return None
        
        data = self.post_process_data(data=data)

        template = self.jinja_environment.get_template(f'{template_name}.html')
        html = template.render(**data)
        if save_path is not None:
            f = open(save_path, 'w')
            f.write(html)
            f.close()

        return html

    def validate_data(self, data):
        # validate
        r = self.validator.validate(data)
        return r, self.validator.errors
    
    def _str_to_boxes(self, txt, total_boxes, fill_with=''):
        # fit a text in a group of boxes
        if type(txt) != str:
            txt = str(txt)
        
        # if len(txt) > total_boxes:
        #    raise Exception('{txt} no entra en {total_boxes} boxes')
            
        ret = [fill_with for r in range(total_boxes - len(txt))]
        ret += list(txt)
        
        return ret
        
    def post_process_data(self, data):
        # improve data for render template

        # prepare edad in three parts to fix in -> EDAD: [][][]
        edad = data.get('beneficiario', {}).get('edad', None)
        data['beneficiario']['__edad'] = self._str_to_boxes(txt=edad, total_boxes=3)
        
        rnos = data['obra_social']['codigo_rnos']
        data['obra_social']['__codigo_rnos'] = self._str_to_boxes(txt=rnos, total_boxes=6)
        
        noss = data['obra_social']['nro_carnet_obra_social']
        data['obra_social']['__nro_carnet_obra_social'] = self._str_to_boxes(txt=noss, total_boxes=17)

        fed = data['obra_social']['fecha_de_emision']['dia']
        data['obra_social']['__fed'] = self._str_to_boxes(txt=fed, total_boxes=2, fill_with='0')

        fem = data['obra_social']['fecha_de_emision']['mes']
        data['obra_social']['__fem'] = self._str_to_boxes(txt=fem, total_boxes=2, fill_with='0')

        fea = data['obra_social']['fecha_de_emision']['anio']
        data['obra_social']['__fea'] = self._str_to_boxes(txt=fea, total_boxes=4, fill_with='')

        fvm = data['obra_social']['fecha_de_vencimiento']['mes']
        data['obra_social']['__fvm'] = self._str_to_boxes(txt=fvm, total_boxes=2, fill_with='0')

        fva = data['obra_social']['fecha_de_vencimiento']['anio']
        data['obra_social']['__fva'] = self._str_to_boxes(txt=fva, total_boxes=4, fill_with='')
        
        ursm = data['empresa']['ultimo_recibo_de_sueldo']['mes']
        data['empresa']['__ursm'] = self._str_to_boxes(txt=ursm, total_boxes=2, fill_with='0')

        ursa = data['empresa']['ultimo_recibo_de_sueldo']['anio']
        data['empresa']['__ursa'] = self._str_to_boxes(txt=ursa, total_boxes=4, fill_with='')

        

        return data

    def get_schema(self):
        schema = {
            'dia': {'type': 'integer', 'min': 1, 'max': 31},
            'mes': {'type': 'integer', 'min': 1, 'max': 12},
            'anio': {'type': 'integer', 'min': 2019, 'max': 2030},
            'hospital': {
                'type': 'dict',
                'schema': {
                    'nombre': {'type': 'string'},
                    # HPGD = Hospitales Públicos de Gestión Descentralizada
                    'codigo_hpgd': {'type': 'string'}
                    }
                },
            'beneficiario': {
                'type': 'dict',
                'schema': {
                    'apellido_y_nombres': {'type': 'string'},
                    'tipo_dni': {'type': 'string', 'allowed': ['DNI', 'LE', 'LC']}, 
                    'dni': {'type': 'string'},
                    'tipo_beneficiario': {'type': 'string', 'allowed': ['titular', 'no titular', 'adherente']},
                    'parentesco': {'type': 'string', 'allowed': ['conyuge', 'hijo', 'otro']},
                    'sexo': {'type': 'string', 'allowed': ['F', 'M']},
                    'edad': {'type': 'integer', 'min': 0, 'max': 110}
                    }
                },
            'atencion': {
                'type': 'dict',
                'schema': {
                    'tipo': {'type': 'string', 'allowed': ['consulta', 'practica', 'internacion']},
                    'profesional': {
                        'type': 'dict',
                        'schema': {
                            'apellido_y_nombres': {'type': 'string'},
                            'matricula_profesional': {'type': 'string'},
                        },
                    },
                    'especialidad': {'type': 'string'},
                    'codigos_N_HPGD': {'type': 'list'},
                    'fecha': {
                        'type': 'dict',
                        'schema': {
                            'dia': {'type': 'integer', 'min': 1, 'max': 31},
                            'mes': {'type': 'integer', 'min': 1, 'max': 12},
                            'anio': {'type': 'integer', 'min': 2019, 'max': 2030}
                            }
                        },
                    'diagnostico_ingreso_cie10': {
                        'type': 'dict',
                        'schema': {
                            'principal': {'type': 'string'}, 
                            'otros': {'type': 'list'}
                            }
                        }
                    }
                },
            'obra_social': {
                'type': 'dict',
                'schema': {
                    'codigo_rnos': {'type': 'string'},
                    'nombre': {'type': 'string'},
                    'nro_carnet_obra_social': {'type': 'string'},
                    'fecha_de_emision': {
                        'type': 'dict',
                        'schema': {
                            'dia': {'type': 'integer', 'min': 1, 'max': 31},
                            'mes': {'type': 'integer', 'min': 1, 'max': 12},
                            'anio': {'type': 'integer', 'min': 1970, 'max': 2030}
                            }
                        },
                    'fecha_de_vencimiento': {
                        'type': 'dict',
                        'schema': {
                            'dia': {'type': 'integer', 'min': 1, 'max': 31},
                            'mes': {'type': 'integer', 'min': 1, 'max': 12},
                            'anio': {'type': 'integer', 'min': 2019, 'max': 2030}
                            }
                        },
                    }
                },
            'empresa': {
                'type': 'dict',
                'schema': {
                    'nombre': {'type': 'string'},
                    'direccion': {'type': 'string'},
                    'ultimo_recibo_de_sueldo': {
                        'type': 'dict',
                        'schema': {
                            'dia': {'type': 'integer', 'min': 1, 'max': 31},
                            'mes': {'type': 'integer', 'min': 1, 'max': 12},
                            'anio': {'type': 'integer', 'min': 1970, 'max': 2030}
                            }
                        },
                    'cuit': {'type': 'string'}
                    }
                }
        }

        return schema

if __name__ == '__main__':

    data = {'dia': 3,
            'mes': 9,
            'anio': 2020,
            'hospital': {
                'nombre': 'HOSPITAL SAN ROQUE',  # https://www.sssalud.gob.ar/index.php?page=bus_hosp&cat=consultas
                'codigo_hpgd': '4321323'
                },
            'beneficiario': {
                'apellido_y_nombres': 'Juan Perez',
                'tipo_dni': 'LE',  # DNI | LE | LC
                'dni': '34100900',
                'tipo_beneficiario': 'titular',  # | no titular | adherente
                'parentesco': 'conyuge',  # hijo | otro
                'sexo': 'M',  # | F
                'edad': 38,
                },
            'atencion': {
                'tipo': 'consulta',  # | practica | internacion
                'profesional': {
                    'apellido_y_nombres': 'Adolfo Martínez',
                    'matricula_profesional': '10542',
                },
                'especialidad': 'Va un texto al parecer largo, quizas sea del nomenclador',
                'codigos_N_HPGD': ['AA01', 'AA02', 'AA06', 'AA07'],  # no se de donde son estos códigos
                'fecha': {'dia': 3, 'mes': 9, 'anio': 2019},
                'diagnostico_ingreso_cie10': {'principal': 'W020', 'otros': ['w021', 'A189']}
                },
            'obra_social': {
                'codigo_rnos': '800501',
                'nombre': 'OBRA SOCIAL ACEROS PARANA',
                'nro_carnet_obra_social': '12345678901234567890',
                'fecha_de_emision': {'dia': 11, 'mes': 9, 'anio': 2009},
                'fecha_de_vencimiento': {'dia': 11, 'mes': 9, 'anio': 2029}
                },
            'empresa': {
                'nombre': 'Telescopios Hubble',
                'direccion': 'Av Astronómica s/n',
                'ultimo_recibo_de_sueldo': {'mes': 7, 'anio': 2017},
                'cuit': '31-91203043-8'
                }
        }

    a2 = Anexo2(data=data)
    save_to = os.path.join(a2.templates_folder, 'res.html')
    res = a2.get_html(save_path=save_to)
    if res is None:
        print('ERRORES al procesar pedido')
        for field, error in a2.errors.items():
            print(f' - {field}: {error}')
    else:
        print(f'Procesado correctamente y grabado en {save_to}')
