from wtforms import StringField, PasswordField, BooleanField, RadioField, SelectField
from wtforms.validators import InputRequired, EqualTo, Length, Email
from flask_wtf import FlaskForm


class SignupForm(FlaskForm):
    """User Signup Form."""

    email = StringField(
        'Email',
        validators=[
            InputRequired(),
            Email(message=('Please enter a valid email address.')),
        ],
        render_kw={
            "required": True,
            "autocomplete": "off",
            "placeholder": "name@address.com"
        },
    )
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            Length(min=6, message=('Please choose a stronger password.')),
            EqualTo('confirm', message='The passwords must match'),
        ],
        render_kw={
            "placeholder": "Please enter your password",
            "required": True,
        },
    )
    confirm = PasswordField(
        'Confirm Your Password',
        render_kw={
            "placeholder": "Please repeat the password",
            "required": True,
        },
    )


class LoginForm(FlaskForm):
    """User Login Form."""

    email = StringField(
        'Email',
        [
            InputRequired(),
            Email('Please enter a valid email address.')
        ],
        render_kw={
            "placeholder": "Email address",
            "required": True,
        },
    )
    password = PasswordField(
        'Password',
        [InputRequired()],
        render_kw={
            "placeholder": "Password",
            "for": "inputPassword",
        },
    )

    remember_me = BooleanField(
        'Remember Me',
    )


class AddAccountForm(FlaskForm):
    """User Signup Form."""

    name = StringField(
        'Name',
        validators=[
            InputRequired(),
        ],
        render_kw={
            "required": True,
            "autocomplete": "off",
            "placeholder": "Name your account"
        },
    )

    access_key = StringField(
        'Access Key',
        validators=[
            InputRequired(),
        ],
        render_kw={
            "required": True,
            "autocomplete": "off",
        },
    )

    secret_key = StringField(
        'Secret Key',
        validators=[
            InputRequired(),
        ],
        render_kw={
            "required": True,
            "autocomplete": "off",
        },
    )


class CreateInstanceForm(FlaskForm):
    port_22 = BooleanField(
        'SSH',
        render_kw={
            "checked": True,
            "autocomplete": "off",
        },
    )
    port_80 = BooleanField('HTTP')