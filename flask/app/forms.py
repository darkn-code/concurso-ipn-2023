from flask_wtf import FlaskForm
from wtforms.fields import StringField, DateField,PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Enviar')


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha de Nacimiento', format='%Y-%m-%d', validators=[DataRequired()])
    correo_electronico = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Enviar')
