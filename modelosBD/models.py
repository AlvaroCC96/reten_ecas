from django.db import models

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class AlumnoAsistencia(models.Model):
    año = models.IntegerField(null=False)
    semestre = models.IntegerField(null=False)
    rut = models.CharField(max_length=8, null=False)
    dv = models.CharField(max_length=1, null=False)
    curso = models.CharField(max_length=6, null=False)
    fecha = models.DateField(null=False)
    cod_asig = models.CharField(max_length=8, null=False)
    cod_pro = models.IntegerField(null=False)
    presente = models.IntegerField(null=True)
    sesion = models.IntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'dbo.tb_alumnos_asistencia'
        app_label = 'asistencia'

class AlumnoNotas(models.Model):
    año = models.IntegerField(null=False)
    semestre = models.IntegerField(null=False)
    cod_asig = models.CharField(max_length=8, null=False)
    curso = models.CharField(max_length=6, null=False)
    rut = models.CharField(max_length=8, null=False)
    dv = models.CharField(max_length=1, null=False)
    c1 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    c2 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    c3 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    c4 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    c5 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    c6 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    c7 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    c8 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    c9 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    c10 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    c11 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    c12 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    c13 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    c14 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    c15 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    cp = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    nt = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    nc = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    d1 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    d2 = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    np = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    situacion = models.CharField(max_length=15, null=True)
    porc_asis = models.IntegerField(null=True)
    estado = models.CharField(max_length=10, null=True)

    class Meta:
        managed = False
        db_table = 'dbo.tb_alumnos_notas'
        app_label = 'notas'
        
class Asignatura(models.Model):
    cod_asig = models.CharField(max_length=10, null=False, primary_key=True)
    cod_asig_des = models.CharField(max_length=60, null=True)
    horas_cla = models.IntegerField(null=True)
    horas_ayu = models.IntegerField(null=True)
    diurno = models.CharField(max_length=1, null=True)
    vespertino = models.CharField(max_length=1, null=True)
    fecha_ult = models.DateTimeField(null=True)
    usuario = models.CharField(max_length=10, null=True)
    prueba = models.IntegerField(null=True)
    cod_asig_des_2 = models.CharField(max_length=25, null=True)

    class Meta:
        managed = False
        db_table = 'dbo.tb_asignaturas'

class Criterio(models.Model):
    id = models.AutoField(primary_key=True)
    nom_criterio = models.CharField(max_length=30, null=False)
    des_criterio = models.CharField(max_length=80, null=False)

    class Meta:
        managed = False
        db_table = 'dbo.tbr_criterios'

class DatoCriterio(models.Model):
    id = models.AutoField(primary_key=True)
    año = models.IntegerField(null=False)
    semestre = models.IntegerField(null=False)
    x = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    des_x = models.CharField(max_length=80, null=True)
    y = models.DecimalField(max_digits=5, decimal_places=1, null=True)
    des_y = models.CharField(max_length=80, null=True)
    fecha_ini = models.CharField(max_length=10, null=True)
    fecha_fin = models.CharField(max_length=10, null=True)
    activo = models.IntegerField(null=False)
    fecha_ult = models.DateTimeField(null=False)
    usuario_ult = models.CharField(max_length=10, null=False)

    class Meta:
        managed = False
        db_table = 'dbo.tbr_data_criterios'

class Modulo(models.Model):
    id_mod = models.AutoField(primary_key=True)
    titulo_modulo = models.CharField(max_length=30, null=False)
    desc_modulo = models.CharField(max_length=80, null=True)

    class Meta:
        managed = False
        db_table = 'dbo.tbr_modulos'

class Usuario(models.Model):
    usuario = models.CharField(primary_key=True, max_length=20)
    persona = models.CharField(max_length=80, null=False)
    cargo = models.CharField(max_length=15, null=False)
    fecha_ini = models.DateTimeField(null=True)
    fecha_fin = models.DateTimeField(null=True)
    activo = models.IntegerField(null=False)
    fecha_ult = models.DateTimeField(null=False)
    usuario_cre = models.CharField(max_length=20, null=False)

    class Meta:
        managed = False
        db_table = 'dbo.tbr_usuarios'

class UsuarioAcceso(models.Model):
    usuario = models.CharField(primary_key=True, max_length=20)
    id_mod = models.IntegerField(null=False)
    activo = models.IntegerField(null=False)
    fecha_ult = models.DateTimeField(null=False)
    usuario_cre = models.CharField(max_length=20, null=False)

    class Meta:
        managed = False
        db_table = 'dbo.tbr_usuarios_acceso'