class Plato(models.Model):
    _name = 'restaurante.plato'
    _rec_name ='nombre'

    nombre = fields.Char()
    precio = fields.Integer()